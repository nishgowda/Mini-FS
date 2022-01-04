# DistStore

### *Simple* distributed key value store in python. All work is handled by leveldb and flask (looking to change this for something faster).

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

