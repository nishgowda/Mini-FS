#!/bin/bash

./main.sh master 3000 && MASTER=3000 ./main.sh worker 3001
./tools/start-master.sh 3000 && ./tools/demo 3001 0
