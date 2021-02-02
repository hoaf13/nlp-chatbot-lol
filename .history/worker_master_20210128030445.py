import redis 

red = redis.StrictRedis(host='localhost',port=6379,db=0)

queue = list()

def str_to_bool(str):
    if str == b'False':
        return False
    if str == b'True':
        return True
    return None

while 
        