#!/usr/bin/env python3

from kitten import KittenFS
from flask import Flask, jsonify, request
import json
from util import get_db_size

app = Flask(__name__)

kitten = KittenFS()
@app.route('/master')
def create_master():
    ret = kitten.create_master()
    return jsonify(str(ret))

@app.route('/add_worker', methods=['POST'])
def add_worker():
    if request.method == 'POST':
        vals = request.form
        # grab meta_data and key from it
        meta_data = str(vals)
        key = str(vals['key'])
        print(key, meta_data)
        if not kitten.k_in_master(key.encode()):
            kitten.add_worker_to_master(key.encode(), meta_data.encode())
        return jsonify("Added worker: ", key)

@app.route('/clear')
def clear():
    kitten.clear_master()
    return jsonify("Cleared master...restart server")

@app.route('/close')
def close():
    ret = kitten.close_master()
    return jsonify(ret)
if __name__ == "__main__":
    app.run()
