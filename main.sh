#!/bin/bash

TYPE=$1
PORT=$2

re='^[0-9]+$'
# check if valid port
if ! [[ $PORT =~ $re ]] ; then
	echo "$PORT is ot a valid number">&2; exit 1
fi

if [ $TYPE == "master" ]; then
	gunicorn -b 127.0.0.1:$PORT master:app &
elif [ $TYPE == "worker" ]; then
	gunicorn -b 127.0.0.1:$PORT worker:app &
else
	echo "Not a valid option sorry"
fi
	
