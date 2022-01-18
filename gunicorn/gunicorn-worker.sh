#!/bin/bash

DOCKER=True MASTER=3000 gunicorn  worker:app -w 2 --threads 2 -b 0.0.0.0:$PORT

