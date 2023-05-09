#!/bin/bash

set -euxo pipefail

BASE=$(readlink -f $(dirname "$(readlink -f $0)"))

docker build -t cryptoscope_website ${BASE}/cryptoscope_website
docker service update --force --update-order start-first cryptoscope_website
