import plyvel
import os
import hashlib
from util import get_db_size

class DistStore():
    def __init__(self):
        self.stores = {}
        self.vols = []
        self.content_idx = 0
        self.vol_idx = 0
        self.master = None
    
    def create_master(self):
        self.master = plyvel.DB('/tmp/cachedb/master', create_if_missing=True)
        return self.master
    
    def print_master(self):
        for k, v in self.master:
            print(k, v)
    
    def close_master(self):
        for k, _ in self.master:
            self.master.delete(k)
        self.master.close()
        del self.master
    
    def clear_all(self):
        for k, v in self.master:
            self.master.delete(k)
        for vol in self.vols:
            for k, v in vol:
                vol.delete(k)

    # call this after we reach a certain amount of volumes hit
    def add_vol(self):
        path = f'/tmp/cachedb/volume/{self.vol_idx}'
        db = plyvel.DB(path, create_if_missing=True)
        self.vols.append(db)
        self.stores[self.vol_idx] = db
        self.vol_idx += 1
    
    # adds current volume to master
    def add_vol_to_master(self):
        db = self.vols[self.vol_idx-1]
        #print('DB:', db)
        k = str(self.vol_idx-1).encode()
        hasher = hashlib.new('sha512_256')
        hasher.update(k)
        hashed_k = hasher.hexdigest()
        self.master.put(str(hashed_k).encode(), str(db).encode())

    def put(self, val):
        db = self.vols[self.vol_idx-1]
        print(db, self.vol_idx-1, self.content_idx)
        k = str(self.vol_idx-1).encode()
        hasher = hashlib.new('sha512_256')
        hasher.update(k)
        hashed_k = hasher.hexdigest()
        db.put(str(hashed_k).encode(), str(val).encode())
        self.stores[self.content_idx] = val
        self.content_idx +=1
        path = f'/tmp/cachedb/volume/{self.vol_idx-1}'
        print(get_db_size(path))        
        return val

    def get(self, key):
        db = self.stores[self.vol_idx-1]
        k = str(self.vol_idx-1).encode()
        hasher = hashlib.new('sha512_256')
        hasher.update(k)
        hashed_k = hasher.hexdigest()
        return db.get(str(hashed_k).encode())
    
    def gets(self):
        return list(self.stores.values())
        
