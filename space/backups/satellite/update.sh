#!/bin/bash

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t satellite ${BASE}/satellite
docker service update --force --update-order start-first satellite_satellite
