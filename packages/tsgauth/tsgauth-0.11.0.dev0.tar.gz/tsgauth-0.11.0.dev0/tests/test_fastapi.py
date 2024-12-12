from fastapi import FastAPI,Depends
from fastapi.testclient import TestClient
from tsgauth.fastapi import JWTBearerClaims
import tsgauth
import pytest

### test server setup
client_id = "cms-tsg-frontend-testclient"
client_id_wrong = "not_a_real_client"
auth = tsgauth.oidcauth.KerbAuth(client_id)

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("OIDC_CLIENT_ID",client_id)
    monkeypatch.setattr(tsgauth.fastapi.settings,"oidc_client_id",client_id)
    app = FastAPI()
    setup_app_endpoints(app)
    return TestClient(app)

def setup_app_endpoints(app):
    @app.get("/unsecure")
    async def unsecure():
        return {"msg": "unsecure endpoint"}

    @app.get("/secure")
    async def secure(claims = Depends(JWTBearerClaims())):
        return {"msg": f"welcome {claims['sub']}"}
    
    @app.get("/secure_noaud")
    async def secure(claims = Depends(JWTBearerClaims(require_aud=False))):
        return {"msg": f"welcome {claims['sub']}"}
    
    @app.get("/secure_noverify")
    async def secure(claims = Depends(JWTBearerClaims(validate_token=False))):
        return {"msg": f"welcome {claims['sub']}"}


### tests
def test_unsecure(client):
    """
    simple test to just check we started the fastapi server correctly
    """    
    resp = client.get('/unsecure')
    assert resp.status_code == 200
    assert resp.json()['msg'] == 'unsecure endpoint'

def test_secure_noauth(client):
    """
    test that we fail the auth when we dont pass in the correct authentication parameters
    """    
    resp = client.get('/secure')
    assert resp.status_code == 401

def test_secure_auth(client):
    """
    test that we can authenticate and get the username back
    """
    resp = client.get('/secure',**auth.authparams())
    subject = tsgauth.oidcauth.parse_token(auth.token())["sub"]
    assert resp.status_code == 200
    assert resp.json()['msg'] == f'welcome {subject}'

@pytest.mark.parametrize("client_id,require_aud,expected_status",[(None,True,500),("",True,500),(None,False,200),("",False,200)])
def test_secure_auth_no_client_id(client,monkeypatch,client_id,require_aud,expected_status):
    """
    tests that by default we require the client_id to be set
    """
    monkeypatch.setenv("OIDC_CLIENT_ID",client_id if client_id is not None else "")
    monkeypatch.setattr(tsgauth.fastapi.settings,"oidc_client_id",client_id)
    endpoint = "/secure" if require_aud else "/secure_noaud"
    resp = client.get(endpoint,**auth.authparams())
    assert resp.status_code == expected_status


def test_secure_wrong_aud(client,monkeypatch):
    """
    test that we reject tokens with the wrong auth
    """
    monkeypatch.setenv("OIDC_CLIENT_ID",client_id_wrong)
    monkeypatch.setattr(tsgauth.fastapi.settings,"oidc_client_id",client_id_wrong)
    resp = client.get('/secure',**auth.authparams())
    assert resp.status_code == 403
    assert resp.json()['detail'] == f'Invalid token audience, expects {client_id_wrong}'
