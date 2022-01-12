# KittenFS
<p align="center">
<img src="cat.jpg" alt="cat" width="600"/>
</p>

[![Unit Tests](https://github.com/nishgowda/KittenFS/actions/workflows/tests.yml/badge.svg)](https://github.com/nishgowda/KittenFS/actions/workflows/tests.yml)

An *actually* simple distributed key value store in python. All work is handled by leveldb and the servers are run by flask with gunicorn (to make it faster).

All work is handled by worker nodes and a master server is created that will hold metadata about each worker node that is created. The master node creates a new worker node every time a new worker is spun up on a different server. All worker indices are automatically incremnted on creation and all keys put are hashed and indexed intentionally.

## Supported OS
```
Most forms of Linux should be supported without errors.
Mac may experience errors in installing leveldb. This is mostly a dependency issue only.
Windows has not yet been tested.
```

## Installing
```
cd
git clone https://github.com/nishgowda/kittenfs
cd KittenFS
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

**Note:** With the way leveldb works, and depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/. You can use `mk.sh` script to automatically make this for you.

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
./start-master.sh 3000 && ./demo.sh 3001 0
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
- GET `/master/`
- POST `/worker/<worker_idx>`
- GET `/get/<idx>`
- PUT `/put/<key>/<val>`
- PUT `/put_file/<key>/<path>`
- DELETE `/delete/<key>`
- DELETE `/clear/`
- GET `/close/`

### Usage
```
curl --X http://localhost:3000/master 			# runs the master server
curl --X http://localhost:3001/worker			# runs the worker server

curl --X http://localhost:3001/put/'A'/'happy'  	# should put 'happy' into 'A'
curl --X http://localhost:3001/put_file/'B'/'cat.jpg'  	# should put the byte content of 'cat.jpg' into 'B'
curl --X http://localhost:3001/get/'A'/			# should return 'happy'
curl --X http://localhost:3001/delete/'A'		# should delete key 'A' with value 'happy' 
curl --X http://localhost:3001/clear/			# should clear all data left in worker
curl --X http://localhost:3001/close/			# closes connection to worker
curl --X http://localhost:3000/close			# closes connection to master
```
**Note:** Also curl the *clear* url for a worker when finished to clear the  worker server so you can keep runnning the tests without overlapping the data.
