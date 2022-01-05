# DistStore

### *Simple* distributed key value store in python. All work is handled by leveldb and flask (looking to change this for something faster).

### A master is created that will hold metadata about each worker node that is created. After the worker node reaches surpasses some data size, the master node adds the worker to itself and creates a new worker node where new content will be stored into# until the same process occurs. This will keep repeating.

**Note:** With the way leveldb works, depending on your system, you may need to manually create a *master* and a *worker* directory in /tmp/.

## API

### PUT
```
Use the /PUT route to store some value. Key is auto-incremented and hashed.
```
### GET
```
Use the /GET route to get the value for a given key.
```

### Start the server
*Note:* You must always start the master server before adding any key/value storage.

Run `./server.py` and you can run the test and start the master server at once in `./start-master && ./test`

### Also curl the *clear* url when finished to clear master and volume server so you can keep runnning the tests without overlapping the data.
