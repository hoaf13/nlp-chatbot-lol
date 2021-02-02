from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from flask import request
from app import app 
import requests
import json
import redis

red = redis.StrictRedis(host='localhost',
                        port=6379,
                        db=0)
socketio = SocketIO(app, cors_allowed_origins='*')
conversation_id = 1

def str_to_bool(s):
    if s == b'True':
        return True
    if s == b'False':
        return False
    else:
        raise ValueError

@socketio.on('connected')
def test_connect(data):
    conversation_id += 1
    print("User {} has connected.".format(data))
    data = "User {} vừa vào phòng.".format(data)
    emit("server-send-multiple-messages", data, broadcast=True)

@socketio.on('disconnected')
def test_connect(data):
    print("User {} has disconnected.".format(data))
    data = "User {} vừa rời phòng.".format(data)
    emit("server-send-multiple-messages", data, broadcast=True)

    
@socketio.on('client-send-multiple-messages')
def handle_send_multiple_messages(msg):
    emit("server-send-multiple-messages", msg, broadcast=True)
    
@socketio.on('client-send-single-messages')
def handle_send_single_messages(msg):
    ans = dict()
    ans['client_msg'] = msg
    url = request.url_root + 'apis/conversation/'
    
    myobj = {'conversation_id':conversation_id, 'message_question': str(msg)}

    if red.get("is_new_product_worker1") is None:
        red.set("is_new_product_worker1", str(False))
    is_used = not str_to_bool(red.get("is_new_product_worker1")) 
    
    if is_used:
        product = myobj
        red.set("product_worker1", product)
        red.set("is_new_product_worker1", str(True))
    
    is_new = str_to_bool(red.get("is_new_product_worker2"))
    if is_new:
        taken_product = red.get("product_worker2")
        print("taken_product2: {}".format(taken_product))
        red.set("is_new_product_worker2", str(False))
    
    is_new = str_to_bool(red.get("is_new_product_worker3"))
    if is_new:
        taken_product = red.get("product_worker3")
        print("taken_product3: {}".format(taken_product))
        red.set("is_new_product_worker3", str(False))
    # x = requests.post(url, json=myobj)
    # ans['server_msg'] = json.loads(x.text)['message_answer']
    
    # ans["flag_image"] = "false"
    # print(x.text)
    # if "support_socket" in x.text and "action_ask_hero" not in x.text:
    #     ans["flag_image"] = "true"
    # if "support_socket" in x.text:
    #     flag_image = "true"
    emit("server-send-single-messages", ans)