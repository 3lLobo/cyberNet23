#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))
mkdir -p /cs/data/flowcontrol


docker build -t flowcontrol_server ${BASE}/flowcontrol_server
docker stack rm flowcontrol  || true
while docker network inspect flowcontrol_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml flowcontrol
${BASE}/wait-for-it.sh localhost:2223 -t 90
