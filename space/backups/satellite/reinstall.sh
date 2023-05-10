#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t satellite ${BASE}/satellite
docker stack rm satellite || true
while docker network inspect satellite_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml satellite
${BASE}/wait-for-it.sh localhost:2222 -t 90
