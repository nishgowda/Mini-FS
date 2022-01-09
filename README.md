# catstore

A *simple* distributed key value store in python. All work is handled by leveldb and flask with gunicorn (to make it faster).

A master server is created that will hold metadata about each worker node that is created. All work is handled by worker nodes and the master node adds metadata about the worker and creates a new worker node every time you run `worker.py` on a different server.

**Note:** With the way leveldb works, and depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/.

## Usage
### Start the server
*Note:* You must always start the master server before adding any key/value storage.

- Run `./master <port_number>` to spin up the master server .
- Run `MASTER=<master_port_number> ./worker <port_number>` to spin up a worker.
- Run `./start-master <master_port_number> && ./demp <worker_port_number> <content_id>` to quickly run a quick example.
```
./master 3000 & 
MASTER=3000 ./worker 3001 &
./start-master 3000 && ./demo 3001 0
```
### Replicating workers
You can also create a new worker that starts as a clone of another with the `CLONE` flag.
```
CLONE=0 MASTER=3000 ./worker 3002
```
This allows the new worker on 3002 to copy the contents of the worker with index 0.

- Then you can make requests to the worker server by requesting put and get requests.
- For each new worker you make, the master server will add metadata about it.
```
curl --X http://localhost:5000/master 			# runs the master server
curl --X http://localhost:5001/worker			# runs the worker server

curl --X http://localhost:5001/put/'A'/'happy'  	# should put 'happy' into 'A'
curl --X http://localhost:5001/put_file/'B'/'cat.jpg'  	# should put the byte content of 'cat.jpg' into 'B'
curl --X http://localhost:5001/get/'A'/			# should return 'happy'
curl --X http://localhost:5001/delete/'A'		# should delete key 'A' with value 'happy' 
```

## API
- MASTER `/master/`
	- spins up the master conenction on the master server
- WORKER `/worker/<worker_idx>`
	- creates a new worker process with the given index	
- GET `/get/<idx>`
	- gets a value with the given key index 
- PUT `/put/<key>/<val>`
	- put a new value in the worker with a given key and value
- PUT_FILE `/put_file/<key>/<path>`
	- put a file in the worker given a key and the path to the file
- DELETE `/delete/<key>`
	- deletes from the database with a given key
- CLEAR `/clear/<worker_idx>`
	- clears all keys from the worker given it's index
- CLOSE `/close/<worker_idx>`
	- closes all connections to the worker server with the given index
- CLOSE `/close/`  (on master) 
	- closes all connections to the master server

**Note:** Also curl the *clear* url for a worker when finished to clear the  worker server so you can keep runnning the tests without overlapping the data.
