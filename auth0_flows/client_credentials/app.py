from functools import wraps
from pathlib import Path
import http.client
import os
import ssl

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request
from flask import abort
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import json
from jose import jwt
from urllib.request import urlopen

app = Flask(__name__)

oauth = OAuth(app)
load_dotenv()
dotenv_path = Path('.env')  # DEFAULT_LOCATION

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
SERVER_ENV = os.getenv("SERVER_ENV")
SERVER_PORT = os.getenv("SERVER_PORT")
AUTH0_API_CLIENT_ID = os.getenv("AUTH0_API_CLIENT_ID")
AUTH0_API_CLIENT_SECRET = os.getenv("AUTH0_API_CLIENT_SECRET")
ALGORITHMS = ['RS256']
API_AUDIENCE = f'{SERVER_ENV}:{SERVER_PORT}/test-one'
API_BASE_URL = f'https://{AUTH0_DOMAIN}'

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_API_CLIENT_ID,
    client_secret=AUTH0_API_CLIENT_SECRET,
    api_base_url=f'{API_BASE_URL}',
    access_token_url=f'{API_BASE_URL}/oauth/token',
    authorize_url=f'{API_BASE_URL}/authorize',
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    # The request object could be accessed whenever we need it
    # It is not tied to a path/decorator of a particular API
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2:
        abort(401)
    if header_parts[0].lower() != 'bearer':
        abort(401)
    valid_token = auth_header.split(" ")[1]
    return valid_token


def requires_api_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        try:
            payload = verify_decode_jwt(jwt)
        except:
            abort(403)
        return f(payload, *args, **kwargs)

    return wrapper


@app.route('/api/v1/protected')
@requires_api_auth
def protected(jwt):
    return f'Oh happy day!'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0 FROM MY AUTH0 ACCOUNT
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # GET THE PUBLIC KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
        # Finally, verify!!!
        if rsa_key:
            try:
                # USE THE KEY TO VALIDATE THE JWT
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )

                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


# Note: On exporting the env variable FLASK_APP=app.py and the running the app with python -m flask run --reload
# the app runs on localhost:5000. It means the following configuration is not validated.
# To use the following configuration (https, port 443, etc) run the command `python app.py -h 0.0.0.0`
if __name__ == '__main__':
    certs_dir = Path('certs')
    port = int(os.getenv('APP_PORT', 443))
    app.secret_key = os.urandom(24)
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain(f'{certs_dir}/localhost.crt', f'{certs_dir}/localhost.key')
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context=ctx)
