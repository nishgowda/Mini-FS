import plyvel
import os
from util import get_db_size, hashed_key

class DistStore():
    def __init__(self):
        self.stores = {}
        self.workers = {}
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
            print('k...', k)
            if k == idx:
                return True
        return False
    
    def print_master(self):
        for k, v in self.master:
            print(k, v)
    
    def clear_master(self):
        for k, _ in self.master:
            self.master.delete(k)
        #self.masters.close()

    def clear_worker(self):
        worker = list(self.workers.values())[0]
        for k, _ in worker:
            worker.delete(k)
    # call this after we reach a certain amount of data hit
    def add_worker(self):
        path = f'/tmp/cachedb/worker/{self.worker_idx}'
        db = plyvel.DB(path, create_if_missing=True)
        #print(hashed_key(self.worker_idx-1))
        self.workers[str(hashed_key(self.worker_idx -1)).encode()] = db
        self.worker_idx += 1
        return db
    
    # adds child to master
    def add_worker_to_master(self, hashed_idx, db_size):
        print('DB:', hashed_idx) # checks if the worker db is correct.
        self.master.put(hashed_idx, db_size)
        print('added new woker to master!!!')

    def put(self,key,val):
        hashed_k = str(hashed_key(key)).encode()
        hashed_worker_idx = str(hashed_key(self.worker_idx -2)).encode()
        db = self.workers[hashed_worker_idx]
        #print(db, self.worker_idx-1, self.content_idx)
        db.put(hashed_k, str(val).encode())
        self.content_idx +=1
        return val

    def get(self, key):
        hashed_k = str(hashed_key(self.worker_idx-2)).encode()
        db = self.workers[hashed_k]
        return db.get(str(hashed_key(key)).encode())        
