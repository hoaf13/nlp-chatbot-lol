from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from app import app 

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connected')
def test_connect(data):
    print("User {} has connected.".format(data))
    data = "User {} vừa vào phòng.".format(data)
    emit("server-send-multiple-messages", data, broadcast=True)

@socketio.on('disconnected')
def test_disconnect(data):
    print("User {} has disconnected.".format(data))
    data = "User {} rời phòng.".format(data)
    emit("server-send-multiple-messages", data, broadcast=True)

    
@socketio.on('client-send-multiple-messages')
def handle_send_multiple_messages(msg):
    emit("server-send-multiple-messages", msg, broadcast=True)
    
@socketio.on('client-send-single-messages')
def handle_send_single_messages(msg):
    ans = dict()
    ans['client_msg'] = msg
    ans['server_msg'] = "response -> " + msg
    print("SERVER RESPONSE: {}".format(ans))
    emit("server-send-single-messages", ans)