#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t lostpass ${BASE}/lostpass
docker stack rm lostpass || true
while docker network inspect lostpass_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml lostpass
${BASE}/wait-for-it.sh localhost:3005 -t 90
