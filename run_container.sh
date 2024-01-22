#!/bin/sh

# remove existing
docker stop dynamodb-local
docker stop olxParser

docker rm dynamodb-local
docker rm olxParser

# get the containers ip at peer_network
subnet=172.18.0
nosql_ip="${subnet}.67"
olx_parser_ip="${subnet}.22"

docker system prune -f
docker network rm peer_network
docker network create --subnet="${subnet}.0/16" peer_network

docker create --name dynamodb-local --network peer_network --ip=${nosql_ip} -p 8000:8000 amazon/dynamodb-local:2.1.0
docker restart dynamodb-local

sleep 3

# fetch some secrets
COMPILETREE_ACCESS_KEY_ID=someaccesskeyid
COMPILETREE_SECRET_ACCESS_KEY=someaccesskeysecret

# set some environment variable
export AWS_ACCESS_KEY_ID=${COMPILETREE_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${COMPILETREE_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION=eu-central-1
DYNAMODB_PORT=8000
DYNAMODB_ENDPOINT_URL=http://localhost:${DYNAMODB_PORT}

docker build -t olxparser:latest .
docker run -d --name olxParser -e DYNAMODB_ENDPOINT=${nosql_ip} -e DYNAMODB_PORT=${DYNAMODB_PORT} -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} --network peer_network --ip=${olx_parser_ip} -p 9019:8080 olxparser:latest

# create LandItems table
echo "Creating table LandItems"
aws dynamodb create-table --table-name LandItems --key-schema AttributeName=id,KeyType=HASH --attribute-definitions AttributeName=id,AttributeType=S --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --endpoint-url ${DYNAMODB_ENDPOINT_URL}

# wait for LandItems table to be created
aws dynamodb wait table-exists --table-name LandItems --endpoint-url ${DYNAMODB_ENDPOINT_URL}
echo "Table LandItems created!"
