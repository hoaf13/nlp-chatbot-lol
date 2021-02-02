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
    if red.get("is_new_product_worker2") is None:
        red.set("is_new_product_worker2", str(False))
    if red.get("is_new_product_worker3") is None:
        red.set("is_new_product_worker3", str(False))

    is_used = not str_to_bool(red.get("is_new_product_worker2"))
    if is_used:
        if len(queue) < 1: 
            continue
        taken_product = red.get("product_worker2")
        red.set("is_new_product_worker2", str(False))
        # do something 
    
    is_used = not str_to_bool(red.get("is_new_product_worker2"))
    if is_used:
        if len(queue) < 1: 
            continue
        taken_product = red.get("product_worker2")
        red.set("is_new_product_worker2", str(False))
        # do something 
    
        