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
    is_new = str_to_bool(red.get("is_new_product_worker2"))
    if is_new:
        taken_product = red.get("product_worker2")
        red.set("is_new_product_worker2", str(False))
        
        