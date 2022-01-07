#!/usr/bin/env python3

from master import dstore
from flask import Flask, jsonify, send_from_directory
import json
from util import get_db_size, hashed_key, allowed_file
import sys
import requests
import io
import time
app = Flask(__name__)

@app.route('/worker/<worker_idx>')
def create_worker(worker_idx):
    dstore.set_worker_idx(int(worker_idx))
    worker = dstore.add_worker()
    #dstore.add_worker_to_master()
    print('DSTORE', dstore, 'worker:', worker)
    if worker is not None:
        worker = str(worker)
    return jsonify(worker)


@app.route('/put/<key>/<val>')
def put_req(key, val):
    if allowed_file(val):
        print('dasda?')
        infile = open(val, 'rb')
        data = infile.read()
        dstore.put(key, data)
        ret = 'Saved ' + val
    else:
        ret = dstore.put(key, val)

    # make the payload here; gonna be metadata
    metadata = {
                'key': str(hashed_key(dstore.worker_idx)),
                'dbsize':get_db_size(dstore.worker_idx),
                'created_at': time.strftime("%Y, %m, %d, %H, %M, %S")
            }
    r = requests.post('http://localhost:5000/add_worker', metadata)
    if ret is not None:
        ret = str(ret)
    #print(r.text)
    return jsonify(ret)

@app.route('/get/<key>')
def get_req(key):
    ret = dstore.get(key)
    if ret is not None:
        ret = str(ret.decode('utf-8'))
    return jsonify(ret)
@app.route('/delete/<key>')
def delete_req(key):
    ret = dstore.delete(key)
    if ret is not None:
        ret = str(ret.decode('utf-8'))
    return jsonify(ret)

@app.route('/clear')
def clear():
    dstore.clear_worker()
    return jsonify("Cleared worker..")


if __name__ == "__main__":
    port = sys.argv[1]
    app.run(port=port)
