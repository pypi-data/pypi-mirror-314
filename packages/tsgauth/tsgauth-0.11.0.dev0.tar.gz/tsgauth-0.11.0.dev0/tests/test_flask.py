from flask import Flask, g
import tsgauth

def create_app():
    """
    creates our toy flask app to test with
    """
    app = Flask(__name__)

    app.config.update({           
        'OIDC_ISSUER' : "https://auth.cern.ch/auth/realms/cern",
        'OIDC_JWKS_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs",
        'OIDC_CLIENT_ID' : "cms-tsg-frontend-testclient"        
    }) 
        
    @app.route('/unsecure')
    def unsecure():
        return {"msg" : "unsecure endpoint"}
    

    @app.route('/secure')
    @tsgauth.flaskoidc.accept_token()
    def secure():
        return {"msg" : f"welcome {g.oidc_token_info['sub']}"}

    return app 


def test_unsecure():
    """
    simple test to just check we started the flask server correctly
    """
    app = create_app()
    with app.test_client() as c:
        resp = c.get('/unsecure')
        assert resp.status_code == 200
        assert resp.json['msg'] == 'unsecure endpoint'

def test_secure_noauth():
    """
    test that we fail the auth when we dont pass in the correct authentication parameters
    """
    app = create_app()
    with app.test_client() as c:
        resp = c.get('/secure')
        assert resp.status_code == 401

def test_secure_auth():
    """
    test that we can authenticate and get the username back
    """
    app = create_app()
    auth = tsgauth.oidcauth.KerbAuth("cms-tsg-frontend-testclient")
    subject = tsgauth.oidcauth.parse_token(auth.token())["sub"]
    with app.test_client() as c:
        resp = c.get('/secure',**auth.authparams())
        assert resp.status_code == 200
        assert resp.json['msg'] == f'welcome {subject}'





if __name__ == "__main__":
    app = create_app()