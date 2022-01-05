import os
import hashlib
def get_db_size(worker_idx):
    db_dir =  f'/tmp/cachedb/worker/{worker_idx-1}'
    size = 0
    for f in os.listdir(db_dir):
        path = os.path.join(db_dir, f)
        if os.path.isfile(path):
            size += os.path.getsize(path)
    return size

def hashed_key(key):
    k = str(key).encode()
    hasher = hashlib.new('sha512_256')
    hasher.update(k)
    hashed_k = hasher.hexdigest()
    return hashed_k
