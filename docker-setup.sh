#!/bin/bash
num_workers=1
while test $# -gt 0; do
  case $1 in 
    -num_workers)
      shift
      num_workers=$1
      shift
      ;;
    -build)
      shift
      BUILD=1
      shift
      ;;
    -network)
      shift
      NETWORK=1
      shift
      ;;
    -volumes)
      shift
      VOLUMES=1
      shift
      ;;
    *)
      echo "$1 is not a flag"
      exit 1;
      ;;
  esac
done

# setup for running kittenfs on docker

if [ -z $BUILD ]; then
  echo "Not building containers..."
else
# 1.) build containers
  docker build -f Dockerfile.master  -t kittenfs:master .
  docker build -f Dockerfile.worker  -t kittenfs:worker .
fi

# 2.) create network
if [ -z $NETWORK ]; then
  echo "Not creating network..."
else
  docker network create kitten
fi

# create volumes
docker volume create --name mk
# 3.) run master container now
docker run -d -p 3000:3000 -e DOCKER=True -v mk:/tmp/cachedb --net kitten --name master kittenfs:master

if [ -z $VOLUMES ]; then
  echo "Not re-creating volumes"
else
  # 4.) create /tmp/cachedb on disk for leveldb storage
  docker exec master mkdir /tmp/cachedb
  docker exec master mkdir /tmp/cachedb/master
  docker exec master mkdir /tmp/cachedb/worker
fi
# 5.) run worker containers now
for i in $(seq 1 $num_workers);  do
  # for the number of workers, the port is incremented by 1 and we assign the same volumes
  # that we made for the master.
      docker run -d -p "300$i":"300$i" -e PORT="300$i" -e DOCKER=True -e MASTER=3000  -v mk:/tmp/cachedb/ --net kitten --name "worker_$i" kittenfs:worker 
done
