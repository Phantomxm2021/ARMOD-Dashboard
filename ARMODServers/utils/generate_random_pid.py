import uuid
import time

def generate_unique_id(name):
    new_name = name + str(time.time())
    return uuid.uuid3(uuid.NAMESPACE_DNS,new_name).int & (1<<32)-1