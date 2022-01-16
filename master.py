#!/usr/bin/env python3

from __init__ import kitten
from flask import Flask, request
import json
from util import get_db_size
import ast

app = Flask(__name__)

@app.route('/', methods=['POST'])
def create_master():
    ret = kitten.create_master()
    return json.dumps(str(ret))

@app.route('/add_worker/<worker_idx>', methods=['POST'])
def add_worker(worker_idx):
    if request.method == 'POST':
        worker_idx = int(worker_idx) - 1
        vals = json.loads(request.json)
        # grab meta_data and key from it
        meta_data = str(vals)
        key = str(vals['key'])
        #print("MONE",  worker_idx)
        v = kitten.k_in_master(str(worker_idx).encode())
        #print("prev is", v) 
        if not v:
            obj = [meta_data.encode()]
            #prev = kitten.k_in_master(str(worker_idx - 1).encode())
            #if not prev:
                #print("AM I HERE?")
            kitten.add_worker_to_master(str(worker_idx).encode(), str(obj).encode())
            return json.dumps("Added worker: " + key)
        else:
             prev = v
        prev = prev.decode()
        obj = ast.literal_eval(prev)
        #print("the prev is:", obj)
        print("meta_data:", meta_data.encode())
        obj.append(meta_data.encode())
        #print("the obj:", obj)
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
    app.run()
