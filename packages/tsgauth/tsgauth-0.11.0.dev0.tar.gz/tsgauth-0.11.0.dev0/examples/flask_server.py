from flask import Flask, g, session, request, redirect, url_for
from urllib.parse import urlencode
import tsgauth


def create_app():
    """
    creates our toy flask app to test with
    """
    app = Flask(__name__)

    app.config.update({           
        'OIDC_ISSUER' : "https://auth.cern.ch/auth/realms/cern",
        'OIDC_JWKS_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs",
        'OIDC_AUTH_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/auth",
        'OIDC_LOGOUT_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/logout",
        'OIDC_CLIENT_ID' : "cms-tsg-frontend-client",        
        'OIDC_TOKEN_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/token",
        'OIDC_ALLOW_TOKEN_REQUEST' : True,
        'OIDC_REDIS_HOST' : "localhost", #change to your redis host if you are using redis as auth store
        'OIDC_REDIS_PORT' : 6379,
        'OIDC_AUTH_STORE' : "simplemem", #change this to redis to store it in the back end
    }) 
    app.secret_key = "test key change this in production"
    app.register_blueprint(tsgauth.flaskoidc.auth_blueprint)
    return app 


app = create_app()

@app.route('/unsecure')
def unsecure():
    return {"msg" : "unsecure endpoint"}
    

@app.route('/secure')
@tsgauth.flaskoidc.accept_token()
def secure():
    return {"msg" : f"welcome {g.oidc_token_info}"}

