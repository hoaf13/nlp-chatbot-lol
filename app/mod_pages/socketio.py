from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from flask import request
from app import app 
import requests
import json
import redis
from app.models import Conversation
import re 

socketio = SocketIO(app, cors_allowed_origins='*')

conversation_id = 1
for conversation in list(Conversation.query.all()):
    conversation_id = max(conversation_id, conversation.conversation_id)
conversation_id += 1

USERNAMES = ['admin']

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('connected')
def test_connect(data):
    global conversation_id
    conversation_id += 1
    print("User {} has connected.".format(data))
    data = "User {} vừa vào phòng.".format(data)
    emit("server-send-multiple-messages", data, broadcast=True)

@socketio.on('client-send-disconnect')
def test_connect(data):
    data = dict()
    data['username'] = data 
    data['msg'] = ' vừa rời phòng.'
    emit("server-send-disconnect", data, broadcast=True, include_self=False)

@socketio.on('client-send-username-register')
def handle_send_username_register(username):
    flag_existing = False
    if username in USERNAMES or username.isspace() or username == '':
        flag_existing = True
    ans = dict()
    ans['flag_existing'] = flag_existing
    print(flag_existing)
    if not flag_existing:
        USERNAMES.append(username)
        emit('server-send-successful-register', ans)
    else:
        emit('server-send-failed-register', ans)

@socketio.on('client-send-message-successful-register')
def handle_send_message_successfull_register(username):
    print("Username in client-send-message-successful-register: {}".format(username))
    emit('server-send-message-successfull-register', username, broadcast=True)

@socketio.on('client-logout')
def handle_logout(username):
    USERNAMES.remove(username)
    emit('server-send-logout', username, broadcast=True,include_self=False)

@socketio.on('client-send-multiple-messages')
def handle_send_multiple_messages(msg):
    print("client-send-multiple-messages: {}".format(msg))
    emit("server-send-multiple-messages", msg, broadcast=True)
    
@socketio.on('client-send-single-messages')
def handle_send_single_messages(msg):
    ans = dict()
    ans['client_msg'] = msg
    url = request.url_root + 'apis/conversation/'  
    myobj = {'conversation_id':conversation_id, 'message_question': str(msg)}
    x = requests.post(url, json=myobj)
    ans['server_msg'] = json.loads(x.text)['message_answer']
    
    ans["flag_image"] = "false"
    print(x.text)
    if "support_socket" in x.text and "action_ask_hero" not in x.text:
        ans["flag_image"] = "true"
    if "support_socket" in x.text:
        flag_image = "true"
    emit("server-send-single-messages", ans)