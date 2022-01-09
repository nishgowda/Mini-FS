#!/usr/bin/env python3

from catstore import CatStore
from flask import Flask, jsonify, request
import json
from util import get_db_size

app = Flask(__name__)

catstore = CatStore()
@app.route('/master')
def create_master():
    ret = catstore.create_master()
    return jsonify(str(ret))

@app.route('/add_worker', methods=['POST'])
def add_worker():
    if request.method == 'POST':
        vals = request.form
        # grab meta_data and key from it
        meta_data = str(vals)
        key = str(vals['key'])
        print(key, meta_data)
        if not catstore.k_in_master(key.encode()):
            catstore.add_worker_to_master(key.encode(), meta_data.encode())
        return jsonify("Added worker: ", key)

@app.route('/clear')
def clear():
    catstore.clear_master()
    return jsonify("Cleared master...restart server")

@app.route('/close')
def close():
    ret = catstore.close_master()
    return jsonify(ret)
if __name__ == "__main__":
    app.run()
