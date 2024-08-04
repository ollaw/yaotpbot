#!/bin/sh

awslocal dynamodb create-table \
    --table-name yaotpbot-table \
    --key-schema AttributeName=id,KeyType=HASH AttributeName=name,KeyType=RANGE \
    --attribute-definitions AttributeName=id,AttributeType=S AttributeName=name,AttributeType=S \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 