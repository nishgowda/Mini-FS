import plyvel
import os
import hashlib
from util import get_db_size


class DistStore():
    def __init__(self):
        self.stores = {}
        self.workers = []
        self.content_idx = 0
        self.worker_idx = 0
        self.master = None
    
    def create_master(self):
        self.master = plyvel.DB('/tmp/cachedb/master', create_if_missing=True)
        return self.master
    
    def print_master(self):
        for k, v in self.master:
            print(k, v)
     
    def clear_and_close(self):
        for k, _ in self.master:
            self.master.delete(k)

        # ik this is ugly but it works enough
        for worker in self.workers:
            for k, _ in worker:
                worker.delete(k)
            worker.close()
            del worker

        self.master.close()
        del self.master

    # call this after we reach a certain amount of data hit
    def add_worker(self):
        path = f'/tmp/cachedb/worker/{self.worker_idx}'
        db = plyvel.DB(path, create_if_missing=True)
        self.workers.append(db)
        self.worker_idx += 1
    
    # adds current child to master
    def add_worker_to_master(self):
        db = self.workers[self.worker_idx-1]
        print('DB:', db) # checks if the worker db is correct.
        k = str(self.worker_idx-1).encode()
        hasher = hashlib.new('sha512_256')
        hasher.update(k)
        hashed_k = hasher.hexdigest()
        self.master.put(str(hashed_k).encode(), str(db).encode())

    def put(self, val):
        db = self.workers[self.worker_idx-1]
        print(db, self.worker_idx-1, self.content_idx)
        k = str(self.worker_idx-1).encode()
        hasher = hashlib.new('sha512_256')
        hasher.update(k)
        hashed_k = hasher.hexdigest()
        db.put(str(hashed_k).encode(), str(val).encode())
        self.content_idx +=1
        path = f'/tmp/cachedb/worker/{self.worker_idx-1}'
        print(get_db_size(path)) # use this later to determine where
        # to split data into how many chunks
        return val

    def get(self, key):
        db = self.workers[self.worker_idx-1]
        k = str(self.worker_idx-1).encode()
        hasher = hashlib.new('sha512_256')
        hasher.update(k)
        hashed_k = hasher.hexdigest()
        return db.get(str(hashed_k).encode())
    
    def gets(self):
        ret = []
        for worker in self.workers:
            for _, v in worker:
                ret.append(v)
        return ret
        
