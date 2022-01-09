#!/usr/bin/env python3

from master import catstore
from flask import Flask, jsonify, send_from_directory
import json
from util import get_db_size, hashed_key, allowed_file
import requests
import io
import time
import os

#MASTER=config('MASTER_MASTER')
MASTER=os.environ['MASTER']
try:
    CLONE=os.environ['CLONE']
except:
    CLONE=False

app = Flask(__name__)

@app.route('/worker/<worker_idx>')
def create_worker(worker_idx):
    catstore.set_worker_idx(int(worker_idx))
    worker = catstore.add_worker()
    print('DSTORE', catstore, 'worker:', worker)
    if CLONE:
        os.system(f'./clone {CLONE} {worker_idx}')
    if worker is not None:
        worker = str(worker)
    return jsonify(worker)


@app.route('/put/<key>/<val>')
def put_req(key, val):
    ret = catstore.put(key, val)

    # make the payload here; gonna be metadata
    metadata = {
                'key': str(hashed_key(catstore.worker_idx)),
                'dbsize':get_db_size(catstore.worker_idx),
                'created_at': time.strftime("%Y, %m, %d, %H, %M, %S")
            }
    r = requests.post(f'http://localhost:{MASTER}/add_worker', metadata)
    if ret is not None:
        ret = str(ret)
    return jsonify(ret)
@app.route('/put_file/<key>/<path:path>')
def put_file(key, path):
    infile = open(path, 'rb')
    data = infile.read()
    catstore.put(key, str(data))
    ret = 'Saved ' + path
    #print(ret)
    # make the payload here; gonna be metadata
    metadata = {
                'key': str(hashed_key(catstore.worker_idx)),
                'dbsize':get_db_size(catstore.worker_idx),
                'created_at': time.strftime("%Y, %m, %d, %H, %M, %S")
            }
    r = requests.post(f'http://localhost:{MASTER}/add_worker', metadata)
    if ret is not None:
        ret = str(ret)
    return jsonify(ret)

@app.route('/get/<key>')
def get_req(key):
    ret = catstore.get(key)
    if ret is not None:
        ret = str(ret.decode('utf-8'))
    return jsonify(ret)

@app.route('/delete/<key>')
def delete_req(key):
    ret = catstore.delete(key)
    if ret is not None:
        ret = str(ret.decode('utf-8'))
    return jsonify(ret)

@app.route('/clear')
def clear():
    catstore.clear_worker()
    return jsonify("Cleared worker..")

@app.route('/close')
def close():
    ret = catstore.close_worker()
    return jsonify(ret)

if __name__ == "__main__":
    app.run()
