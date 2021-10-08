import hashlib
from functools import partial
def create_md5(data, block_size=65536):    
    str_md5 = hashlib.sha1(data.encode("utf-8")).hexdigest()
    return str_md5