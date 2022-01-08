#!/usr/bin/env python3

from master import dstore
from flask import Flask, jsonify, send_from_directory
import json
from util import get_db_size, hashed_key, allowed_file
import requests
import io
import time
import os
import subprocess

#MASTER=config('MASTER_MASTER')
MASTER=os.environ['MASTER']
try:
    CLONE=os.environ['CLONE']
except:
    CLONE=False

app = Flask(__name__)

@app.route('/worker/<worker_idx>')
def create_worker(worker_idx):
    dstore.set_worker_idx(int(worker_idx))
    worker = dstore.add_worker()
    print('DSTORE', dstore, 'worker:', worker)
    if CLONE:
        os.system(f'./clone {CLONE} {worker_idx}')
    if worker is not None:
        worker = str(worker)
    return jsonify(worker)


@app.route('/put/<key>/<val>')
def put_req(key, val):
    ret = dstore.put(key, val)

    # make the payload here; gonna be metadata
    metadata = {
                'key': str(hashed_key(dstore.worker_idx)),
                'dbsize':get_db_size(dstore.worker_idx),
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
    dstore.put(key, str(data))
    ret = 'Saved ' + path
    #print(ret)
    # make the payload here; gonna be metadata
    metadata = {
                'key': str(hashed_key(dstore.worker_idx)),
                'dbsize':get_db_size(dstore.worker_idx),
                'created_at': time.strftime("%Y, %m, %d, %H, %M, %S")
            }
    r = requests.post(f'http://localhost:{MASTER}/add_worker', metadata)
    if ret is not None:
        ret = str(ret)
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

@app.route('/close')
def close():
    ret = dstore.close_worker()
    return jsonify(ret)

if __name__ == "__main__":
    app.run()
