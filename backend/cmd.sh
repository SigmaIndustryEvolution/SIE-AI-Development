# /bin/sh

docker exec -it $(docker ps -a -q) /bin/bash
