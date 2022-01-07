# diststore

A *simple* distributed key value store in python. All work is handled by leveldb and flask (looking to change this for something faster).

A master server is created that will hold metadata about each worker node that is created. All work is handled by worker nodes and the master node adds metadata about the worker and creates a new worker node every time you run `worker.py` on a different server.

**Note:** With the way leveldb works, and depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/.


## Usage

### Start the server
*Note:* You must always start the master server before adding any key/value storage.

- Run `./master.py` and `./worker.py <port_number>` seperately. 
- Run `./start-master &&`./test <worker_idx> <content_id>` to quickly run a quick example.
- Then you can make requests to the worker server by placing put and get requests to it.
- For each new worker you make, the master server will add metadata about it to it's content.

```
curl --X http://localhost:5000/master 		# runs the master server
curl --X http://localhost:5001/worker		# runs the worker server

curl --X http://localhost:5001/put/'A'/'happy'  # should put 'happy' into 'A'
curl --X http://localhost:5001/get/'A'/		# should return 'happy'
curl --X http://localhost:5001/delete/'A'	# should delete key 'A' with value 'happy' 
```

### API
- MASTER `/master/`
- WORKER `/worker/<worker_idx>`
	- creates a new worker process with the given index	
- GET `/get/<idx>`
	- gets a value with the given key index 
- PUT `/put/<key>/<val>`
	- put a new value in the worker with a given key and value
- DELETE `/delete/<key>`
	- deletes from the database with a given key
- CLEAR `/clear/<worker_idx>`
	- clears all keys from the worker given it's index

**Note:** Also curl the *clear* url for a worker when finished to clear the  worker server so you can keep runnning the tests without overlapping the data.
