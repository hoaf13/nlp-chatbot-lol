import redis

red = redis.StrictRedis(host='localhost',
                        port=6379,
                        db=0)

def str_to_bool(s):
    if s == b'True':
        return True
    if s == b'False':
        return False
    else:
        raise ValueError
    
while True: 
    if red.get("is_new_product_worker1") is None:
        red.set("is_new_product_worker1", str(False))

    is_used = not str_to_bool(red.get("is_new_product_worker1")) 
    if is_used:
        red.set("product_worker1", )