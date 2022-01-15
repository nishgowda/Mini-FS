#!/bin/bash
curl -X POST http://localhost:$1/worker/$2
curl -X PUT -d value="dsadsdas" http://localhost:$1/put/'A'
