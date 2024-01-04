#! /bin/sh

set -e

PIDS=$(docker ps -a -q)

if [ ! -z "$PIDS" ]
then
	docker stop $(docker ps -a -q)
	docker rm $(docker ps -a -q)
fi
docker build -t safari-lab .
docker run -d --restart=always -p 8080:8080 safari-lab
sleep 1
docker logs $(docker ps -a -q) -f
