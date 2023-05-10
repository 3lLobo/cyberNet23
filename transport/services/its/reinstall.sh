#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))
pip3 install -U textual

mkdir -p /cs/data/its
sudo touch /cs/data/its/database
pwgen 32 1 > ${BASE}/mongo-root
pwgen 32 1 > ${BASE}/mongo-its

#build docker container
docker build -t its ${BASE}/its
docker stack rm its || true
while docker network inspect its_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml its
${BASE}/wait-for-it.sh localhost:4000 -t 90
${BASE}/wait-for-it.sh localhost:27017 -t 90
echo "OK"
