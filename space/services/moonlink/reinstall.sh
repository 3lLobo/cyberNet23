#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

# Install pip requirements so client.py can be used outside of the docker container.
pip3 install -r moonlink/requirements.txt

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t moonlink ${BASE}/moonlink
docker stack rm moonlink || true
while docker network inspect moonlink_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml moonlink
${BASE}/wait-for-it.sh localhost:3000 -t 90
