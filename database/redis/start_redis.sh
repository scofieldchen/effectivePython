#!/bin/bash

# 用docker启动redis

docker container run -d --rm --name redis -p 6379:6379 redis