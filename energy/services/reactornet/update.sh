#!/bin/bash

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t reactornet_server ${BASE}/reactornet_server
docker service update --force --update-order start-first reactornet_server
