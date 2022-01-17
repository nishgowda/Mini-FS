# kittenFS
<p align="center">
<img src="cat.jpg" alt="cat" width="600"/>
</p>

[![Unit Tests](https://github.com/nishgowda/KittenFS/actions/workflows/tests.yml/badge.svg)](https://github.com/nishgowda/KittenFS/actions/workflows/tests.yml)

An *actually* simple distributed key value store in python. All work is handled by leveldb and the servers are run by flask with gunicorn (to make it faster).

All work is handled by worker nodes and a master server is created that will hold metadata about each worker node that is created. The master node adds metadata about the new worker whenever a new one is spun up on a different server. All worker indices are automatically incremented on creation and all keys put are hashed and indexed intentionally.

## Supported OS
```
Most forms of Linux should be supported without errors.
Mac may experience errors in installing leveldb. This is mostly a dependency issue only.
Windows has not yet been tested.
```

## Installing
```
cd ~
git clone https://github.com/nishgowda/kittenFS
cd kittenFS
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
**Note:** With the way leveldb works, and depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/. You can use `mk.sh` script to automatically make this for you.

### Using Docker
You can also run kittenFS on docker, so you don't need to worry about problems with installation or your OS at all. Feel free to run to setup it for you.
```
./docker-setup.sh
```
This builds two different containers, MASTER and a WORKER and creates a docker network between them that allows them to communicate with each other.
Of course, this is currently meant as a way to quickly setup yourself up with docker for this project so it isn't really that scalable yet to building more workers. However, this is still developing and the plan is for that to happen.

## Start the servers
*Note:* You must always start the master server before adding any key/value storage.
Use the bash script *main* to quickly spin up master and worker servers in the background.
```
./main.sh master 3000 			# spin up master on 3000
MASTER=3000 ./main.sh worker 3001 	# spin up a worker on 3001; specifies master running on 3000
MASTER=3000 ./main.sh worker 3002 	# spin up a worker on 3002; specifies master running on 3000
```

If you want to start the master and worker server on ports 3000 and 3001 respectively, while seeing a demo of the application, feel free to run this command that uses shell scripts to do this.
```
./tools/start-master.sh 3000 && ./tools/demo.sh 3001 0
```

### Replicating workers
You can also create a new worker that starts as a clone of another with the `CLONE` flag.
```
CLONE=1 MASTER=3000 ./main.sh worker 3003
```
This allows the new worker on 3002 to copy the contents of the worker with index 1.

- Then you can make requests to the worker server by requesting put and get requests.
- For each new worker you make, the master server will add metadata about it.

## API
| Master  | Worker |
| ----    | ------ |
| POST `/`               | POST `/worker/<worker_idx>` |
| GET `/add_worker`      | GET `/get/<idx>`            |
| GET `/gets`            | PUT `/put`                  |
| DELETE `/delete/<key>` | DELETE `/delete/<key>`      |
| DELETE `/clear`        | DELETE `/clear`             |
| GET `/close`		 | GET `/close`		       |


### Usage
```
# spin up the master server
curl -X POST localhost:3000
# spin up a worker on port 3001 with index 0						
curl -X POST localhost:3001/worker/0					

# put 'happy' into 'A'
curl -X  PUT -d value="happy" localhost:3001/put/'A'		

# put '~/Downloads/cat,jpg' file into 'B'
curl -X  PUT -d file="~/Downlaods/cat.jpg"  localhost:3001/put/'B' 	

# get value stored for 'A'
curl --X localhost:3001/get/'A'		

# get metadata for master
curl --X localhost:3001/gets				

# clear all data in worker 3001
curl -X  DELETE localhost:3001/clear					

# clear all data in master server
curl -X  DELETE localhost:3000/clear					

# close all connection to worker on 3001
curl --X localhost:3001/close		

# close connection to master server		
curl --X localhost:3000/close						
```
**Note:** Also curl the *clear* url for a worker when finished to clear the  worker server so you can keep runnning the tests without overlapping the data.
