#!/bin/bash

mkdir -p $PWD/certs
openssl req -x509 -out $PWD/certs/localhost.crt \
        -keyout $PWD/certs/localhost.key \
        -newkey rsa:2048 \
        -nodes -sha256 \
        -subj '/CN=localhost' -extensions EXT \
        -config cert_config.cf
docker build . -t python-auth0-permissions
docker run -itp 10443:443 --rm --name python-auth0 \
       -v $PWD:/auth0 \
       -e AUTH0_CLIENT_ID=$AUTH0_CLIENT_ID \
       -e AUTH0_CLIENT_SECRET=$AUTH0_CLIENT_SECRET \
       -e AUTH0_DOMAIN=$AUTH0_DOMAIN \
       -e SERVER_ENV=$SERVER_ENV \
       -e SERVER_PORT=$SERVER_PORT \
       -e AUTH0_API_CLIENT_ID \
       -e AUTH0_API_CLIENT_SECRET \
       -e SERVER_PORT \
       -e APP_PORT \
       -e APP_SERVER \
       python-auth0