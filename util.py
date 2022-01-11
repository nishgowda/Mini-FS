import os
import hashlib
import time

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

def get_meta_data(worker_idx):
    metadata = {
                'key': str(hashed_key(worker_idx)),
                'dbsize':get_db_size(worker_idx),
                'created_at': time.strftime("%Y/%m/%d %H:%M:%S")
            }
    return metadata        

# straight from: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
