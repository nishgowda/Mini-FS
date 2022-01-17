#!/bin/bash
MASTER=$1
WORKER=$2

docker exec $MASTER mkdir /tmp/cachedb
docker exec $MASTER mkdir /tmp/cachedb/master
docker exec $MASTER mkdir /tmp/cachedb/worker

docker exec $WORKER mkdir /tmp/cachedb
docker exec $WORKER mkdir /tmp/cachedb/master
docker exec $WORKER mkdir /tmp/cachedb/worker
