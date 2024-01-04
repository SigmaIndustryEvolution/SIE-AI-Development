#! /bin/sh

git pull
docker-compose build --build-arg CONFIG="nginx-proxy.conf"
docker-compose up 
