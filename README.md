# diststore

A *simple* distributed key value store in python. All work is handled by leveldb and flask (looking to change this for something faster).

A master server is created that will hold metadata about each worker node that is created. All work is handled by worker nodes and the master node adds metadata to itself and creates a new worker node until the same process occurs. This will keep repeating.

**Note:** With the way leveldb works, depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/.


## Usage

### Start the server
*Note:* You must always start the master server before adding any key/value storage.

- Run `./master.py` and `./worker.py <port_number>` seperately. 
- Run `./start-master` and `./test <worker_idx> <content_id>`.
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
The standard functions of the API
- GET `/master/`
- GET `/worker/<worker_idx>`
	- creates a new worker process with the given index	
- GET `/get/<idx>`
	- gets a value with the given key index 
- PUT `/put/<key>/<val>`
	- put a new value in the worker with a given key and value
- DELETE `/delete/<key>`
	- deletes from the database with a given key

Master
```
/master

run ./master.py on terminal to spin up the master server. 

Then make a request to /master to connect it to the server db 
```

Worker
```
/worker

run ./worker.py <port_number>  on terminal to start a worker server running on port_number. 

Make a request to /worker/<worker_idx> to create a new worker server with worker_idx.
```

Put
```
/put/<key>/<val>

make a request to /put/<key><val> on the worker server to store some value.  The value is kept by the certain worker you make the request to. 
```
Get
```
/get/<key>/

make a request to /get/<key> to recieve the value for the given key.
```

#### Also curl the *clear* url for a worker when finished to clear the  worker server so you can keep runnning the tests without overlapping the data.
