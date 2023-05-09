#!/bin/bash

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t flowcontrol_server ${BASE}/flowcontrol_server
docker service update --force --update-order start-first flowcontrol_server
