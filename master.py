#!/usr/bin/env python3

from diststore import DistStore
from flask import Flask, jsonify, request
import json
from util import get_db_size

app = Flask(__name__)

dstore = DistStore()
@app.route('/master')
def create_master():
    ret = dstore.create_master()
    return jsonify(str(ret))

@app.route('/add_worker', methods=['POST'])
def add_worker():
    if request.method == 'POST':
        vals = request.form
        print(vals)
        key = vals['key']
        db_size = vals['dbsize'].encode()
        #print(data, data.form,data.values)
        if not dstore.k_in_master(key.encode()):
            dstore.add_worker_to_master(key.encode(), db_size)
        return jsonify("Added worker: ", key)

@app.route('/clear')
def clear():
    dstore.clear_master()
    return jsonify("Cleared master...restart server")

if __name__ == "__main__":
    app.run()