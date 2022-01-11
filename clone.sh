#!/bin/bash
PREV=$1
WORKER=$2

# make directory and copy contents from previous worker
# mkdir /tmp/cachedb/worker/$WORKER
# assume that the new woker dir is already made
cp -a /tmp/cachedb/worker/$PREV/. /tmp/cachedb/worker/$WORKER 
