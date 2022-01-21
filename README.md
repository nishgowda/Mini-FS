# kittenFS
<p align="center">
<img src="cat.jpg" alt="cat" width="600"/>
</p>

[![Unit Tests](https://github.com/nishgowda/KittenFS/actions/workflows/tests.yml/badge.svg)](https://github.com/nishgowda/KittenFS/actions/workflows/tests.yml)

An *actually* simple distributed key value store in python. 

- Data is stored on *disk*
- Database conenctions are made with [leveldb](https://github.com/google/leveldb)
- Servers are run by flask and sped up with gunicorn
- Includes option to run on docker containers
- All keys put are hashed and indexed

All work is handled by worker nodes and a master server is created that will hold metadata about each worker node that is created. The master node adds metadata about the new worker whenever a new one is spun up on a different server. All worker indices are automatically incremented on creation.

## Supported OS
```
Most forms of Linux should be supported out of the box.
Mac may experience errors in installing leveldb, however, this is mostly a dependency issue only.
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
**Note:** With the way leveldb works, and depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/. You can use the `mk.sh` script in the *tools* directory to automatically make this for you.

## Using Docker
You can also run kittenFS on docker, so you don't need to worry about problems with installation or your OS at all. 

Note that this is still in **development** so there are some bugs, particularly when running multiple worker instances.

 There are severall command line flags you can use here to meet your needs. 
- You can control how many workers you want to spin up with `num_workers`
- You can specify if you want to rebuild the images with `build`. This automates to 1, so the value you use here doesn't matter.
- You can specify if you wan to create the docker-network with the `network` flag. This also automates to 1.
- You can specify if you want to remake the shared volumes from containers with the `volumes` flag.  
```
# spins up 2 worker servers and builds the docker images, while specifying to make volumes
./docker-setup.sh -num_workers 2 -build 1  -volumes 1
```
Take a look at the ```docker-setup.sh``` script for a closer look at this process.


## Starting the servers
**Note**: You can skip the following step if you've used the docker-setup shell script and move straight to setting up the master and worker servers.

Use the bash script ```main.sh``` to quickly spin up master and worker servers in the background. It's key that you create the master server before any workers.
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
You can also create a new worker that starts as a clone of another through the `clone` API endpoint.
```
curl --X localhost:3002/clone/1
```
This allows the new worker on 3002 to copy the contents of the worker with index 1.

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

## TODO:
- Fix docker bugs
- Add support for rebalancing
- Add caching support for files
- Create tests for Windows operating system

## Contributing
Any contributions are more than welcome! Just leave a pull request and if it passes tests and checks out we can merge. Ideas to start off with can be found in implementing one of the items in the TODO list.