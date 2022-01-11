#!/bin/bash
curl --X http://localhost:$1/worker/$2
curl --X http://localhost:$1/put/'A'/'dsadsdas'
