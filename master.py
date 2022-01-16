#!/usr/bin/env python3

from __init__ import kitten
from flask import Flask, request
import json
from util import get_db_size
import ast
import requests
app = Flask(__name__)

@app.route('/', methods=['POST'])
def create_master():
    ret = kitten.create_master()
    return json.dumps(str(ret))

# this is accessed when we PUT a value into a worker
@app.route('/add_worker/<worker_idx>', methods=['POST'])
def add_worker(worker_idx):
    if request.method == 'POST':
        worker_idx = int(worker_idx) - 1
        vals = json.loads(request.json)
        key = str(vals['key'])
        meta_data = str(vals)
        
        v = kitten.k_in_master(str(worker_idx).encode())
        if not v:
            # if there is nothing in master, then we start with a 
            # list of the current values meta data
            obj = [meta_data.encode()]    
            kitten.add_worker_to_master(str(worker_idx).encode(), str(obj).encode())
            return json.dumps("Added worker: " + key)
        else:
            # otherwise we get the previous data
             prev = v
        # now we handle updating the metadata
        prev = prev.decode()
        # create our list of dictionaries
        obj = ast.literal_eval(prev)
        
        # handles changes in key. if we update a key, then we only want
        # to update that key and don't need to add more data to the master
        for idx, item in enumerate(obj):
            d = item.decode()
            d = ast.literal_eval(d)
            if d['key'] == key:
                obj[idx] = vals # use vals here, bc we want an actual dict data structure
                kitten.add_worker_to_master(str(worker_idx).encode(), str(obj).encode())
                return json.dumps("Added worker: " + key)

        # new data coming into already existing list of dicts, so we can 
        # just append the new metadata to our list and add it to our
        # master and attach it to the appropriate worker index
        obj.append(meta_data.encode())
        kitten.add_worker_to_master(str(worker_idx).encode(), str(obj).encode())
        return json.dumps("Added worker: " + key)

@app.route('/gets')
def gets():
    out = {}
    for k, v in kitten.master:
        out[k.decode()] = v.decode()
    return json.dumps(out)

@app.route('/clear', methods=['DELETE'])
def clear():
    kitten.clear_master()
    return json.dumps("Cleared master...restart server")

@app.route('/delete/<key>', methods=['DELETE'])
def delete(key):
    return json.dumps(kitten.delete_from_master(key))

@app.route('/close')
def close():
    ret = kitten.close_master()
    return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True)
