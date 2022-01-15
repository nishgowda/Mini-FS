#!/usr/bin/env python3

from __init__ import kitten
from flask import Flask, request
import json
from util import get_db_size

app = Flask(__name__)

@app.route('/', methods=['POST'])
def create_master():
    ret = kitten.create_master()
    return json.dumps(str(ret))

@app.route('/add_worker', methods=['POST'])
def add_worker():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            vals = json.loads(request.json)
            # grab meta_data and key from it
            meta_data = str(vals)
            key = str(vals['key'])
            if not kitten.k_in_master(key.encode()):
                kitten.add_worker_to_master(key.encode(), meta_data.encode())
            return json.dumps("Added worker: " + key)
        else:
            return "Content-Type not supported!"

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
