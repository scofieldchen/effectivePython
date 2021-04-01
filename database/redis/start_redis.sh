#!/bin/bash

# 用docker启动redis
docker container run -d --rm --name redis -p 6379:6379 redis

# 如果要加上密码
# docker container run -d --rm --name redis -p 6379:6379 redis --requirepass 'password'