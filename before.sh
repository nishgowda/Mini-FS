#!/bin/bash

./main master 3000 && MASTER=3000 ./main worker 3001 && ./start-master 3000
