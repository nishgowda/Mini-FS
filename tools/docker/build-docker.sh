#!/bin/bash

docker build -f Dockerfile.master  -t kittenfs:master .
docker build -f Dockerfile.worker  -t kittenfs:worker .
