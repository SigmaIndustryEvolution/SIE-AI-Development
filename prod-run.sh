#! /bin/sh

git pull
docker-compose build --build-arg CONFIG="nginx-proxy-prod.conf"
docker-compose up -d 
