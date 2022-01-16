#!/usr/bin/env python3

from __init__ import kitten
from flask import Flask, jsonify, request
import json
from util import  get_meta_data, hashed_key
import requests
import time
import os


MASTER=os.environ['MASTER']
try:
    CLONE=os.environ['CLONE']
except:
    CLONE=False


app = Flask(__name__)

@app.route('/worker/<worker_idx>', methods=['POST'])
def create_worker(worker_idx):
    kitten.set_worker_idx(int(worker_idx))
    print('kitten indx', kitten.worker_idx)
    worker = kitten.add_worker()
    #print('worker:', worker)
    if CLONE:
        os.system(f'./clone {CLONE} {worker_idx}')
    if worker is not None:
        worker = str(worker)
    return jsonify(worker)

@app.route('/put/<key>', methods=['PUT'])
def put_req(key):
    data =  request.form
    #print(data)
    
    if not data:
        return json.dumps("No data passed")
    else:
        try:
            #print(data['file'])
            ret = kitten.put(hashed_key(key), data['file'])
        except:
            #print(data['value'])
            ret = kitten.put(hashed_key(key), data['value'])
    # make the payload here; gonna be metadata
    metadata = get_meta_data(kitten.worker_idx, key)
    print("metadata is", metadata)
    #print('metaddata', metadata)
    r = requests.post(f'http://localhost:{MASTER}/add_worker/{kitten.worker_idx}', json=metadata)
    if ret is not None:
        ret = str(ret)
    return jsonify(ret)


@app.route('/get/<key>')
def get_req(key):
    ret = kitten.get(hashed_key(key))
    if ret is not None:
        ret = str(ret.decode('utf-8'))
    return jsonify(ret)

@app.route('/delete/<key>', methods=['DELETE'])
def delete_req(key):

    ret = kitten.delete(key, with_hash=False, is_testing=False)
    if ret is not None:
        ret = str(ret.decode('utf-8'))
    return jsonify(ret)

@app.route('/getindex')
def get_index():
    return jsonify(kitten.worker_idx - 1)

@app.route('/clear', methods=['DELETE'])
def clear():
    kitten.clear_worker(testing=False)
    return jsonify("Cleared worker")

@app.route('/close')
def close():
    ret = kitten.close_worker()
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True)
