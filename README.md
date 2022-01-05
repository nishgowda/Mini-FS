# diststore

A *Simple* distributed key value store in python. All work is handled by leveldb and flask (looking to change this for something faster).

A master is created that will hold metadata about each worker node that is created. All work is handled by worker nodes and the master node adds metadata to itself and creates a new worker node until the same process occurs. This will keep repeating.

**Note:** With the way leveldb works, depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/.


### API
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
This adds the worker to the master server if the worker has not already been added.

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

### Start the server
*Note:* You must always start the master server before adding any key/value storage.

- Run `./master.py` and `./worker.py <port_number>` seperately. 
- Call the `/master` and `/worker` urls for the master and worker servers respectively. This creates connections to the dbs
- Then you can make requests to the worker server by placing put and get requests to it.
- For each new worker you make, the master server will add metadata about it to it's content

#### Also curl the *clear* url when finished to clear master and worker server so you can keep runnning the tests without overlapping the data.
