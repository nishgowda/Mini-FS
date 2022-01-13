#!/bin/bash
curl -X POST http://localhost:$1/worker/$2
curl -X PUT http://localhost:$1/put/'A'/'dsadsdas'
