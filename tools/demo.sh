#!/bin/bash
curl -X POST localhost:$1/worker/$2 && curl -X PUT -d value="dsadsdas" localhost:$1/put/'A'
