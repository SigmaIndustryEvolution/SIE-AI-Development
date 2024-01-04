#! /bin/sh

set -e

docker run -d --restart=always -p 8080:8080 safari-lab
sleep 1
docker logs $(docker ps -a -q) -f
