import plyvel
import os
from util import get_db_size, hashed_key

# content_idx is the index of the key/value you store
# worker_idx is specified by the /worker/<worker_idx> 
class DistStore():
    def __init__(self):
        self.stores = {}
        self.worker = None
        self.content_idx = 0
        self.worker_idx = 0
        self.master = None
    
    def set_worker_idx(self, idx):
        self.worker_idx = idx

    def create_master(self):
        self.master = plyvel.DB('/tmp/cachedb/master', create_if_missing=True)
        return self.master
    
    def k_in_master(self, idx):
        for k, _ in self.master:
            if k == idx:
                return True
        return False
    
    def print_master(self):
        for k, v in self.master:
            print(k, v)
    def close_master(self):
        self.master.close()
        return "closed master"
    def close_worker(self):
        self.worker.close()
        return "closed worker " + str(self.worker_idx)

    def clear_master(self):
        for k, _ in self.master:
            self.master.delete(k)

    def clear_worker(self):
        for k, _ in self.worker:
            self.worker.delete(k)
    
    # call this after we reach a certain amount of data hit
    def add_worker(self):
        path = f'/tmp/cachedb/worker/{self.worker_idx}'
        db = plyvel.DB(path, create_if_missing=True)
        self.worker = db
        self.worker_idx += 1
        return db
    
    # adds child to master
    def add_worker_to_master(self, hashed_idx, db_size):
        self.master.put(hashed_idx, db_size)

    def put(self,key,val):
        hashed_k = str(hashed_key(key)).encode()
        self.worker.put(hashed_k, val.encode())
        self.content_idx +=1
        return val

    def get(self, key):
        return self.worker.get(str(hashed_key(key)).encode())  

    def delete(self, key):
        h_key = hashed_key(key)
        self.worker.delete(str(h_key).encode())
        return h_key.encode()
