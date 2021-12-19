#!/bin/bash

mkdir -p $PWD/backend/src/certs
mkdir -p $PWD/frontend/certs
openssl req -x509 -out $PWD/backend/src/certs/localhost.crt \
        -keyout $PWD/backend/src/certs/localhost.key \
        -newkey rsa:2048 \
        -nodes -sha256 \
        -subj '/CN=localhost' -extensions EXT \
        -config $PWD/backend/src/cert_config.cf
cp $PWD/backend/src/certs/* $PWD/frontend/certs/
docker build . -t carlosvalarezo/coffee_shop_backend
#docker run -itp 10443:443 --rm --name coffee_shop_backend \
#       -v $PWD:/coffee_shop_backend \
#       -e AUTH0_CLIENT_ID=$AUTH0_CLIENT_ID \
#       -e AUTH0_CLIENT_SECRET=$AUTH0_CLIENT_SECRET \
#       -e AUTH0_DOMAIN=$AUTH0_DOMAIN \
#       -e SERVER_ENV=$SERVER_ENV \
#       -e SERVER_PORT=$SERVER_PORT \
#       -e AUTH0_API_CLIENT_ID \
#       -e AUTH0_API_CLIENT_SECRET \
#       -e SERVER_PORT \
#       -e APP_PORT \
#       -e APP_SERVER \
#       carlosvalarezo/coffee_shop_backend