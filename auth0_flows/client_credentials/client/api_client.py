import os
from dotenv import load_dotenv
from pathlib import Path  # To find out the env file if it would be in a different location
import http.client
import json
import ssl
import os

AUTH0_API_CLIENT_ID = os.getenv("AUTH0_API_CLIENT_ID")
AUTH0_API_CLIENT_SECRET = os.getenv("AUTH0_API_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
SERVER_ENV = os.getenv("SERVER_ENV")
SERVER_PORT = os.getenv("SERVER_PORT")
APP_PORT = os.getenv("APP_PORT")
APP_SERVER = os.getenv("APP_SERVER")

load_dotenv()

# dotenv_path = Path('.env') DEFAULT LOCATION


def request_jwt_token_with_credentials():
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

    payload = {
        "client_id": AUTH0_API_CLIENT_ID,
        "client_secret": AUTH0_API_CLIENT_SECRET,
        "audience": f"{SERVER_ENV}:{SERVER_PORT}/test-one",
        # "grant_type": "client_credentials" means that the authorization is requested
        # through client_credentials: client_id & client_secret
        "grant_type": "client_credentials"

    }

    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    token = json.loads(data.decode("utf-8")).get('access_token')

    return token


def send_request_to_api(bearer_token):
    certificate_file = f"{os.getcwd()}/certs/localhost.crt"
    key_file = f"{os.getcwd()}/certs/localhost.key"
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain(certfile=certificate_file, keyfile=key_file)
    conn = http.client.HTTPSConnection(host=APP_SERVER, port=APP_PORT, context=context)
    headers = {
        'authorization': f"Bearer {bearer_token}"
    }

    conn.request(method="GET", url="/api/v1/protected", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


bearer_token_with_creds = request_jwt_token_with_credentials()
send_request_to_api(bearer_token_with_creds)
