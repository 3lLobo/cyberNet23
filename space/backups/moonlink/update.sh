#!/bin/bash

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t moonlink ${BASE}/moonlink
docker service update --force --update-order start-first moonlink_moonlink
