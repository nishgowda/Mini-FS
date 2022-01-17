#!/bin/bash
DOCKER=True MASTER=3000 gunicorn  worker:app -b 0.0.0.0:3001
