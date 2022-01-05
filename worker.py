#!/usr/bin/env python3

from master import dstore
from flask import Flask
from flask import jsonify
import json
from util import get_db_size, hashed_key
import sys
import requests

app = Flask(__name__)

@app.route('/worker')
def create_worker():
    worker = dstore.add_worker()
    #dstore.add_worker_to_master()
    print('DSTORE', dstore, 'worker:', worker)
    return jsonify(str(worker))


@app.route('/put/<val>')
def put_req(val):
    ret = dstore.put(val)
    # make the payload here
    payload = {
            'key': str(hashed_key(dstore.worker_idx)),
            'dbsize':get_db_size(dstore.worker_idx),
            }
    r = requests.post('http://localhost:5000/add_worker', payload)
    print(r.text)
    return jsonify(ret)

@app.route('/get/<key>')
def get_req(key):
    ret = dstore.get(int(key))
    return jsonify(str(ret.decode('utf-8')))

@app.route('/clear')
def clear():
    dstore.clear_workers()
    return jsonify("Cleared workers...clear server if you havent")

if __name__ == "__main__":
    port = sys.argv[1]
    app.run(port=port)
