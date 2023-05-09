#!/bin/bash

echo "This will cause some downtime, are you sure you want to continue? Press enter to continue or CTRL+C to cancel"
read ACCEPT

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))
mkdir -p /cs/data/cryptoscope

docker build -t cryptoscope_website ${BASE}/cryptoscope_website
docker stack rm cryptoscope  || true
while docker network inspect cryptoscope_default >/dev/null 2>&1 ; do sleep 1; done
docker stack deploy --compose-file ${BASE}/docker-compose.yml cryptoscope 
${BASE}/wait-for-it.sh localhost:8080 -t 90
