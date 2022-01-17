#!/bin/bash

# setup for running kittenfs on docker

# 1.) build containers
./tools/docker/build-docker.sh

# 2.) create network
docker network create kitten

# 3.) run containers now
docker run -d -p 3000:3000 --net kitten --name target-host kittenfs:master
docker run -d -p 3001:3001 --net kitten --name worker kittenfs:worker 

# 4.) add volumes for leveldb
./tools/docker/docker_volumes.sh target-host worker
