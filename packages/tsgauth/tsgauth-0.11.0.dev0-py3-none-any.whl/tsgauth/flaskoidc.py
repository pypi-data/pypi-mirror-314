import logging
import functools
import time
from authlib.oidc.core import UserInfo
from urllib.parse import urlencode    
import requests
from flask import current_app, request, jsonify, g, redirect, session , url_for, Blueprint
import tsgauth.oidcauth
import uuid
import redis
import json

"""
inspired by https://gitlab.cern.ch/authzsvc/docs/flask-oidc-api-example
to replace flask-oidc which is old and out of date (https://github.com/puiterwijk/flask-oidc)

Adds basic OpenID Connect authorisation to a flask server


decorate every endpoint you wish to protect with accept_token and the User info (if valid) will be in g.oidc_token_info

Can now handle session based auth (ie through a browser cookie) if that option is enabled 


TODO: handle the nonce better, but need to see a workflow example first


author Sam Harper (STFC-RAL, 2022)
"""

DEFAULT_CFG_PARAMS = {
   'OIDC_ISSUER' : "https://auth.cern.ch/auth/realms/cern",
   'OIDC_JWKS_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs",
   'OIDC_AUTH_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/auth",
   'OIDC_LOGOUT_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/logout",
   'OIDC_TOKEN_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/token",
   'OIDC_SESSION_CLAIMS_LIFETIME' : 28800, #8 hours
   'OIDC_ALLOW_TOKEN_REQUEST' : False, #whether the server can request a token from the auth server if it doesnt have one
   'OIDC_AUTH_STORE' : "simplemem", #simplemem or redis for the store (simplemem doesnt persist across restart/workers)
   'OIDC_REDIS_HOST' : "service/redis", #the redis uri for the redis store
   'OIDC_REDIS_PORT' : 6379, #the redis port for the redis store
}

class _SessionAuthStore:
    """
    A class to manage storing the auth claims server side
    Can have multiple backends, currently supports redis and simple memory cache
    """

    store = None
    @classmethod
    def init_store(cls):
        if cls.store is None:
            store_type = _get_cfg_param("OIDC_AUTH_STORE")
            if store_type == "redis":
                cls.store = redis.Redis(host=_get_cfg_param("OIDC_REDIS_HOST"), port=_get_cfg_param("OIDC_REDIS_PORT"),  decode_responses=True)
            elif store_type == "simplemem":
                cls.store = _SimpleMemCache()
        return cls.store!=None

    @classmethod
    def get(cls,session_id):
        if cls.init_store():
            data = cls.store.get(session_id)
            if data is not None:
                return json.loads(data)
        return None
        
    @classmethod
    def set(cls,session_id,data,lifetime):
        if cls.init_store():
            cls.store.set(session_id,json.dumps(data),ex=lifetime)
    
    @classmethod
    def delete(cls,session_id):
        if cls.init_store():
            return cls.store.delete(session_id)
        
        
class _SessionAuthData:
    """
    handles the session/cookie side auth data
    """
    def __init__(self, session_id = None, auth_try_count = 0, **kwargs):
        self.session_id = session_id
        self.auth_try_count = auth_try_count
    def to_dict(self):
        return {"session_id": self.session_id, "auth_try_count": self.auth_try_count}
    def from_dict(self, data):
        self.session_id = data.get("session_id",None)
        self.auth_try_count = data.get("auth_try_count",0)

class _SimpleMemCache:
    """
    this should be compatible with the redis client function signatures so is a drop in replacement
    """
    def __init__(self):
        self.cache = {}
    def get(self,key):
        entry = self.cache.get(key)
        if entry is not None:
            if entry["expiry"] is not None and entry["expiry"] < time.time():
                self.cache.pop(key,None)
                return None
            return entry["data"]
        else:
            return None
    def set(self,key,value,ex=None):
        expiry = time.time() + ex if ex is not None else None
        self.cache[key] = {"data": value, "expiry": expiry}
    def delete(self,key):
        if key in self.cache:
            del self.cache[key]
            return 1    
        else:
            return 0

def _get_session_auth_data():
    return _SessionAuthData(**session["auth_data"] if "auth_data" in session else {})

def _set_session_auth_data(auth_data):
    session["auth_data"] = auth_data.to_dict()


def _get_cfg_param(name):
    if name in DEFAULT_CFG_PARAMS.keys():
        return current_app.config.get(name,DEFAULT_CFG_PARAMS[name])
    else:
        return current_app.config.get(name)

if Blueprint is not None:
    auth_blueprint = Blueprint("auth", __name__)
    auth_callback_name = "auth_callback"
    auth_logout_name = "logout"
    auth_clear_session_auth_name = "clear_session_auth"

def get_token_from_header():
    """
    gets the token from the Authorization header

    :returns: the token or None if not found
    """
    try:
        auth_header = request.headers["Authorization"]
        return auth_header.split("Bearer")[1].strip()
    except Exception as e:
        return None
    
def get_token_from_auth_server():
    """
    gets the token from the session

    :returns: the token or does a redirect to the auth server to get it if not found
    """

    auth_data = _get_session_auth_data()
    if auth_data.session_id is None:
        auth_data.session_id = str(uuid.uuid4())
    if auth_data.auth_try_count >= 3:
        auth_data.auth_try_count = 0
        session["auth_data"] = auth_data.to_dict()
        return jsonify({"status": "Computer said no too many times"}), 401
    auth_data.auth_try_count += 1
    session["auth_data"] = auth_data.to_dict()

    params = {
        "client_id" : _get_cfg_param('OIDC_CLIENT_ID'),
        "redirect_uri" : f"{request.host_url}/{auth_callback_name}",
        "response_type" : "code",
        "scope" : "openid email profile",
        "state" : request.url
    }
    
    auth_url = f"{_get_cfg_param('OIDC_AUTH_URI')}?{urlencode(params)}"    
    return redirect(auth_url)

def exchange_code_for_token(code):
    """Exchanges the authorization code for an access token."""
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': f"{request.host_url}/{auth_callback_name}",
        'client_id': _get_cfg_param('OIDC_CLIENT_ID'),   
        'client_secret': _get_cfg_param('OIDC_CLIENT_SECRET')    
    }
    response = requests.post(_get_cfg_param('OIDC_TOKEN_URI'), data=data)
    response.raise_for_status()
    return response.json()


def auth_callback():
    """Handles the callback from the OIDC provider after authentication."""
    if 'error' in request.args:
        return f"Error: {request.args['error']}"

    code = request.args.get('code')
    if not code:
        return "No code provided!"

    # Exchange the authorization code for an access token
    token_response = exchange_code_for_token(code)
    access_token = token_response.get('access_token')

    try:
        claims = _parse_token_flask(access_token,validate=True)
    except Exception as e:
        logging.error(f"Authentication error: {e}")
        get_token_from_auth_server()
    else:
        auth_data = _get_session_auth_data()
        _SessionAuthStore.set(auth_data.session_id,{"claims" : claims},_get_cfg_param("OIDC_SESSION_CLAIMS_LIFETIME"))
        return redirect(request.args.get('state') or url_for('/'))

def clear_session_auth():
    """
    clears the auth session but does not log the user out 
    """
    auth_data = _get_session_auth_data()
    if auth_data.session_id is not None:
        _SessionAuthStore.delete(auth_data.session_id)
    if 'auth_data' in session:
        del session['auth_data']
    return {"status": "cleared auth session, user still logged into SSO"}

def logout():
    """
    logs the user out, clearing the session and logging out of the OIDC provider
    """
    clear_session_auth()
    return redirect(_get_cfg_param('OIDC_LOGOUT_URI'))

if Blueprint is not None:
    auth_blueprint.add_url_rule(f"/{auth_callback_name}", auth_callback_name, auth_callback)
    auth_blueprint.add_url_rule(f"/{auth_logout_name}",auth_logout_name, logout)
    auth_blueprint.add_url_rule(f"/{auth_clear_session_auth_name}",auth_clear_session_auth_name, clear_session_auth)


def _parse_token_flask(token,validate):
    """
    parses a token (optionally validated) but retrieving the parameters from the flask app config

    :param token: the token to parse
    :param validate: validate the parsed token
    :returns: the parsed token as an authlib.oidc.core.IDToken
    :rtype: authlib.oidc.core.IDToken
    """
    return tsgauth.oidcauth.parse_token(token = token,
        jwks_url = _get_cfg_param('OIDC_JWKS_URI'),
        issuer = _get_cfg_param('OIDC_ISSUER'),
        client_id = _get_cfg_param('OIDC_CLIENT_ID'),
        validate=validate
    )            
    
def accept_token(require_token=True):
    """
    decorator for validation of the auth token

    puts the claims (if validated) into g.odic_token_info

    note UserInfo is just a dict which parses the keys of IDToken, ie its just the claims of the IDToken without the 
    rest of the methods

    :params require_token: if true , a valid token is required, otherwise is optional and method will succeed
    :returns: None
    """
    
    def decorator(func):
        @functools.wraps(func)
        def function_wrapper(*args, **kwargs):
            token = get_token_from_header()
            request_token = token is None and _get_cfg_param("OIDC_ALLOW_TOKEN_REQUEST") and require_token
            if request_token:
                auth_data = _get_session_auth_data()
                if auth_data.session_id is None:
                    auth_data.session_id = str(uuid.uuid4())
                    auth_data.auth_try_count = 0
                auth_response = _SessionAuthStore.get(auth_data.session_id)
                if auth_response is not None:                    
                    g.oidc_token_info = UserInfo(auth_response["claims"])                    
                    return func(*args, **kwargs)                         
                else:                
                    #go get the token and then come back
                    return get_token_from_auth_server()
            try:                
                claims = _parse_token_flask(token,validate=True)
                g.oidc_token_info = UserInfo(claims)                
            except Exception as e:
                g.oidc_token_info = None
                logging.error(f"Authentication error: {e}")
                if require_token == True:
                    return jsonify({"status": "Computer says no"}), 401
            
            return func(*args, **kwargs)
        function_wrapper.__name__ = func.__name__
        return function_wrapper
    return decorator
