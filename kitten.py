import plyvel
import os
from util import hashed_key
import requests
import json

if os.environ['DOCKER']:
    DOCKER = True
else:
    Docker = False
class KittenFS():
    def __init__(self):
        self.worker = None
        self.master = None
        self.content_idx = 0 # index of the key/value that's stored
        self.worker_idx = 0  # index of the worker 
    
    def get_worker_idx(self):
        return self.worker_idx
    
    def set_worker_idx(self, idx):
        self.worker_idx = idx

    def create_master(self):
        self.master = plyvel.DB('/tmp/cachedb/master', create_if_missing=True)
        return self.master
    
    def k_in_master(self, idx):
        for k, v in self.master:
            #print(k, v)
            if k == idx:
                return v
        return False
    
    def print_master(self):
        for k, v in self.master:
            print(k, v)
    
    def close_worker(self):
        self.worker.close()
        return "closed worker " + str(self.worker_idx)
    
    def close_master(self):
        self.master.close()
        return "closed master"

    def clear_master(self):
        for k, _ in self.master:
            self.master.delete(k)
        return "Cleared master"

    def clear_worker(self, testing):
        for k, _ in self.worker:
            self.delete(k, with_hash=True, is_testing=testing)
        return "Cleared worker"

    # call this after we reach a certain amount of data hit
    def add_worker(self):
        path = f'/tmp/cachedb/worker/{self.worker_idx}'
        db = plyvel.DB(path, create_if_missing=True)
        self.worker = db
        print("self.worker is", self.worker)
        self.worker_idx += 1
        return db
    
    # adds child to master
    def add_worker_to_master(self, hashed_idx, metadata):
        self.master.put(hashed_idx, metadata)
        return hashed_idx

    def put(self,key,val):
        hashed_k = str(hashed_key(key)).encode()
        self.worker.put(hashed_k, val.encode())
        self.content_idx +=1
        return val

    def get(self, key):
        return self.worker.get(str(hashed_key(key)).encode())  

    def delete(self, key, with_hash, is_testing):
        if with_hash:
            h_key = key
            self.worker.delete(h_key)
        else:
            h_key = str(hashed_key(key)).encode() 
            self.worker.delete(h_key)
        if is_testing == False and DOCKER:
            requests.get(f'http://master:3000/delete/{h_key}')
        return str(hashed_key(key)).encode()

    def delete_from_master(self, h_key):
        #print(h_key, str(h_key).encode())
        ret = self.master.delete(str(h_key).encode())
        #print(f'deleted {ret} from master')
        return ret
