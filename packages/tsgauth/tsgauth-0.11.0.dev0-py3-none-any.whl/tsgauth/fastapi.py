import tsgauth.oidcauth
import authlib
import requests
from pydantic_settings import BaseSettings
from urllib.parse import urlencode   
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request, APIRouter, FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Annotated
from aiocache import Cache
import uuid
import abc

"""
collection of functions for use with fastapi
note: this is the authors first time using fastapi, so there may be better ways to do this.
      this package will evolve in the future as experience is gained

It is expected that the only thing a user needs from this is the JWTBearerClaims class and the setup_app function
            
author Sam Harper (STFC-RAL, 2022)


"""

router = APIRouter(prefix="/auth")

class Settings(BaseSettings):
    oidc_client_id: str = ""
    oidc_client_secret: Optional[str] = None
    oidc_issuer: str = "https://auth.cern.ch/auth/realms/cern"
    oidc_jwks_uri: str = "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs"
    oidc_auth_uri: str = "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/auth"
    oidc_logout_uri: str = "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/logout"
    oidc_token_uri: str = "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/token"
    oidc_session_claims_lifetime: int = 28800  # 8 hours, only used for private tokens
    oidc_allow_token_request: bool = False  # whether the server can request a token from the auth server if it doesn't have one
settings = Settings()

class MissingAuthException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SessionAuthBase(abc.ABC):
    """
    Base class for the session auth store

    Aims to handle user authentication when session based. So if a token is not passed in to the request,
    it will managed getting the claim the application wishes for the user.

    This is usually involves obtaining a token from the SSO server with session based on a session cookie but doesnt have to be

    Due to how its used, multiple instances of this class may be created per request so the state should be only set in the __init__ func
    
    Design notes:
    There was some debate about whether to have the methods as classmethods or instance methods given the limited ability for this
    class to have a state. Eventually instance methods were chosen as those can be overriden as classmethods safely but not the
    other way around. This also allows for a subclass to have a state set in the __init__ method if needed

    """
    
    @abc.abstractmethod
    async def claims(self,request: Request) -> Dict[str, Any]:
        """
        gets the claims
        :param request: the request object
        :returns: the claims in a dictionary
        """
        pass
    
    @abc.abstractmethod
    async def store(self,request: Request, auth_response_data : Dict[str, Any]) -> None:
        """
        stores the auth data
        :param request: the request object
        :param auth_response_data: the response data from the auth server containing the auth info
        """
        pass
    
    @abc.abstractmethod
    async def clear(self,request: Request) -> None:
        """
        clears any auth data from the session and associated caches
        :param request: the request object
        """
        pass

    async def token_request_allowed(self,request : Request) -> bool:
        """
        checks if the token request is allowed
        for example the classes may have an internal counter to limit the number of requests to stop an infinite loop of
        requests to the auth server

        :returns: True if allowed, False if not
        """
        return settings.oidc_allow_token_request

    async def auth_attempt(self,request: Request) -> None:
        """
        registers an auth attempt, throwing a HTTPException if not allowed ideally with the reason
        """
        pass

class SessionAuthMemoryStore(SessionAuthBase):
    cache = Cache(Cache.MEMORY)        
    class AuthData:
        def __init__(self, session_id : Optional[str] = None, auth_try_count : int = 0, **kwargs):
            self.session_id = session_id
            self.auth_try_count = auth_try_count
        def to_dict(self) -> Dict[str, Any]:
            return {"session_id": self.session_id, "auth_try_count": self.auth_try_count}
        def from_dict(self, data : Dict[str, Any]):
            self.session_id = data.get("session_id",None)
            self.auth_try_count = data.get("auth_try_count",0)
        
    @classmethod
    async def claims(cls,request: Request) -> Dict[str, Any]:
        auth_data = cls._get_auth_data(request)
        
        if auth_data.session_id is None:
            auth_data.session_id = str(uuid.uuid4())
            cls._set_auth_data(request, auth_data)
        if await cls.cache.exists(auth_data.session_id):
            access_token = await cls.cache.get(auth_data.session_id)
            try: 
                return get_validated_claims(access_token)    
            except HTTPException as e:
                if await cls.token_request_allowed(request) >= 3:
                    raise e
                    
        raise MissingAuthException(status_code=401, detail="No authentication credentials provided.")
    
    @classmethod
    async def store(cls,request: Request, auth_response_data : Dict[str, Any]) -> None:
      
        auth_data = cls._get_auth_data(request)
        await cls.cache.set(auth_data.session_id, auth_response_data["access_token"], ttl=settings.oidc_session_claims_lifetime)
        auth_data.auth_try_count = 0
        cls._set_auth_data(request, auth_data)

    @classmethod
    async def token_request_allowed(cls,request: Request) -> bool:
        return  settings.oidc_allow_token_request and cls._get_auth_data(request).auth_try_count < 3
    
    @classmethod
    async def auth_attempt(cls,request: Request) -> None:
        auth_data = cls._get_auth_data(request)
        auth_data.auth_try_count += 1        
        cls._set_auth_data(request, auth_data)
        if not await cls.token_request_allowed(request):
            await cls.clear(request)
            raise HTTPException(status_code=401, detail="Too many token reqeusts")

    @classmethod
    async def clear(cls,request: Request) -> None:
        auth_data = cls._get_auth_data(request)
        if auth_data.session_id:
            await cls.cache.delete(auth_data.session_id)
        cls._del_auth_data(request)
        
    
    @classmethod
    def _get_auth_data(cls,request:Request) -> AuthData:
        if not hasattr(request, "session"):
            raise HTTPException(status_code=500, detail="Session middleware not configured correctly")
        return cls.AuthData(**request.session.get("auth_data", {}))
    
    @classmethod
    def _set_auth_data(cls,request:Request, auth_data : AuthData) -> None:
        if not hasattr(request, "session"):
            raise HTTPException(status_code=500, detail="Session middleware not configured correctly")
        request.session["auth_data"] = auth_data.to_dict()

    @classmethod
    def _del_auth_data(cls,request:Request) -> None:
        if not hasattr(request, "session"):
            raise HTTPException(status_code=500, detail="Session middleware not configured correctly")
        if "auth_data" in request.session:
            del request.session["auth_data"]    

  
    

    
def get_auth_store() -> SessionAuthBase:
    return SessionAuthMemoryStore

class JWTBearerClaims(HTTPBearer):
    def __init__(self, validate_token :bool = True, require_aud : bool = True, auto_error: bool = False ,use_state: bool = True):
        """
        gets the decoded claims from the request header

        :param validate_token: whether or not to validate the token, if false it'll just return the claims
        :param require_aud: if True, the client id must be set to validate the audience if validate_token is also True
                            no effect if validate_token is False
        :auto_error: this is for the base class BearerAuth, if true it'll raise an exception if the token is not present
                     I would use this but it returns a 403 code rather than a 401 in this case which is incorrect :(
        :use_state: if true, the claims will be stored in the request.state.claims
        """        
        super(JWTBearerClaims, self).__init__(auto_error=auto_error)
        self.validate_token = validate_token
        self.require_aud = require_aud
        self.use_state = use_state

    async def __call__(self, request: Request, auth_store: SessionAuthBase = Depends(get_auth_store)):        
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerClaims, self).__call__(request)   
        if credentials:
            if not credentials.scheme == "Bearer":
                #do we want to redirect for this?
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            claims = get_validated_claims(credentials.credentials, self.validate_token, self.require_aud)            
            if self.use_state:
                request.state.claims = claims                
            return claims
        elif await auth_store.token_request_allowed(request):  
            claims =  await auth_store.claims(request)                 
            if self.use_state:
                request.state.claims = claims   
            return claims
        else:                        
            raise HTTPException(status_code=401, detail="No authentication credentials provided.")

def get_validated_claims(token : str, validate: bool =True, require_aud: bool = True) -> Dict[str, Any]:
    """
    validates the token and returns the claims
    :param token: the token to validate
    :param validate: if True, the token will be validated
    :param require_aud: if True, the client id of the exected aud must be set if validate is True
    :returns: the claims
    :raises: HTTPException if the token is invalid
    """
    try:
        return _parse_token_fastapi(token, validate=validate, require_aud=require_aud)  
    except authlib.jose.errors.InvalidClaimError as e:
        if e.description == 'Invalid claim "aud"':
            raise HTTPException(status_code=403, detail=f"Invalid token audience, expects {settings.oidc_client_id}")
        else:
            raise HTTPException(status_code=403, detail="Invalid token")
    except HTTPException as e:
        raise e
    except Exception as e:            
        raise HTTPException(status_code=403, detail="Invalid token or expired token")
    

def add_auth_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(MissingAuthException)
    async def auth_exception_handler(request: Request, exc: MissingAuthException) -> RedirectResponse:
        return RedirectResponse(f"{request.url_for('get_token_from_auth_server')}?redirect_uri={request.url}")
    
def setup_app(app: FastAPI) -> None:
    app.include_router(router)
    add_auth_exception_handler(app)

def _parse_token_fastapi(token: str, validate: bool=True, require_aud:bool=True) -> Dict[str, Any]:
    """
    token parsing function for fastapi
    :param token: the token to parse
    :param validate: validate the token
    :param require_aud: require a client id to be set to validate the audience if validate = True
    :returns: the claims
    :raises: HTTPException if the token client_id is not set but require_aud is 
    """
    if require_aud and validate and not settings.oidc_client_id:
        raise HTTPException(status_code=500, detail="OIDC_CLIENT_ID not set but audience validation is set to required")

    return tsgauth.oidcauth.parse_token(token=token, 
                                        jwks_url=settings.oidc_jwks_uri,
                                        issuer=settings.oidc_issuer,
                                        client_id=settings.oidc_client_id,
                                        validate=validate)

def exchange_code_for_token(code: str, request: Request) -> Dict[str, Any]:
    """Exchanges an authorization code for an access token."""
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{request.url_for('auth_callback')}",
        "client_id": settings.oidc_client_id,
        "client_secret": settings.oidc_client_secret,
    }
    response = requests.post(settings.oidc_token_uri, data=data)
    response.raise_for_status()
    return response.json()


@router.get("/token_request",tags=["auth"])
async def get_token_from_auth_server(request: Request, redirect_uri : str,auth_store: SessionAuthBase = Depends(get_auth_store)) -> RedirectResponse:
    """Redirects to the authorization server to obtain a token."""
    
    await auth_store.auth_attempt(request)        
    params = {
        "client_id": settings.oidc_client_id,
        "redirect_uri": f"{request.url_for('auth_callback')}",
        "response_type": "code",
        "scope": "openid email profile",
        "state": str(redirect_uri),
    }
    auth_url = f"{settings.oidc_auth_uri}?{urlencode(params)}"
    return RedirectResponse(auth_url)



@router.get("/callback",tags=["auth"])
async def auth_callback(request: Request, auth_store : SessionAuthBase = Depends(get_auth_store)) -> RedirectResponse:
    """Handles the callback from the OIDC provider after authentication."""
    
    params = dict(request.query_params)
    if "error" in params:
        raise HTTPException(detail=f"error getting token from SSO: {params['error']}", status_code=400)

    code = params.get("code")
    if not code:
        raise HTTPException({"error getting token from SSO: no code provided"}, status_code=400)
    
    token_response = exchange_code_for_token(code, request)

    await auth_store.store(request, token_response)
    
    redirect_url = params.get("state") or "/"
    return RedirectResponse(redirect_url)

@router.get("/clear",tags=["auth"])
async def clear_session_auth(request: Request, auth_store: SessionAuthBase = Depends(get_auth_store)) -> JSONResponse:
    """
    clears the auth session but does not log the user out 
    """
    await auth_store.clear(request)
    return {"status": "cleared auth session, user still logged into SSO"}

@router.get("/logout",tags=["auth"])
async def logout(request: Request) -> RedirectResponse:
    """
    logs the user out, clearing the session and logging out of the OIDC provider
    """
    await clear_session_auth(request)
    return RedirectResponse(settings.oidc_logout_uri)