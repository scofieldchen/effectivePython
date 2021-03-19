#!/bin/bash

docker container run -d --rm \
    --name postgres \
    -e POSTGRES_USER=test \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=test \
    -p 5432:5432 \
    postgres:9.6
