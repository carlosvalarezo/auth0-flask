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


def get_auth0_api_token():
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

    payload = {
        "client_id":  AUTH0_API_CLIENT_ID,
        "client_secret": AUTH0_API_CLIENT_SECRET,
        "audience": f"{SERVER_ENV}:{SERVER_PORT}/test-one",
        "grant_type": "client_credentials"
    }

    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8")).get('access_token')


def send_request_to_api():
    certificate_file = f"{os.getcwd()}/certs/localhost.crt"
    key_file = f"{os.getcwd()}/certs/localhost.key"
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain(certfile=certificate_file, keyfile=key_file)
    conn = http.client.HTTPSConnection(host=APP_SERVER, port=APP_PORT, context=context)
    bearer_token = get_auth0_api_token()
    headers = {
        'authorization': f"Bearer {bearer_token}"
    }

    conn.request(method="GET", url="/api/v1/protected", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


send_request_to_api()
