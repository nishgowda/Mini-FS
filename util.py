import os
def get_db_size(db_dir):
    size = 0
    for f in os.listdir(db_dir):
        path = os.path.join(db_dir, f)
        if os.path.isfile(path):
            size += os.path.getsize(path)
    return size

