#!/bin/bash

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t lostpass ${BASE}/lostpass
docker service update --force --update-order start-first lostpass_lostpass