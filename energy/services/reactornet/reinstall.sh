#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))
mkdir -p /cs/data/reactornet/server
mkdir -p /cs/data/reactornet/database
touch /cs/data/reactornet/database/database.sql
pwgen 32 1 > ${BASE}/postgres-root -root


docker build -t reactornet_server ${BASE}/reactornet_server
docker stack rm reactornet  || true
while docker network inspect reactornet_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml reactornet
${BASE}/wait-for-it.sh localhost:2222 -t 90
${BASE}/wait-for-it.sh localhost:5432 -t 90
