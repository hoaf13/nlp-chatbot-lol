import redis 

red = redis.StrictRedis(host='localhost',port=6379,db=0)

queue = list()

def str_to_bool(str):
    if str == b'False':
        return False
    if str == b'True':
        return True
    return None

while True:
    # check supplier product status
    is_new = str_to_bool(red.get("is_new_product_worker1"))
    if is_new:
        taken_product = red.get('product_worker1')
        queue.append(taken_product)
        red.set("new_product_worker1", str(False))
    
    # publish product to consummer
    if red.get()

        