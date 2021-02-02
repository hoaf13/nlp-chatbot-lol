from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from app import app 
import requests
import json

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connected')
def test_connect(data):
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
    url = 'http://127.0.0.1:5000/apis/conversation/'
    myobj = {'conversation_id':1, 'message_question': str(msg)}
    x = requests.post(url, json = myobj)
    ans['server_msg'] = json.loads(x.text)['message_answer']
    if "support_socket" in x.text:
        ans["flag_image"] = "true"
    else:
        ans["flag_image"] = "false"
    ans['flag_image'] = 
    if "support_socket" in x.text:
        flag_image = "true"
    emit("server-send-single-messages", ans)