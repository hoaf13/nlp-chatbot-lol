from app import app
from flask import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connected')
def test_connect(data):
    send("User {} has connected".format(data), broadcast=True)

@socketio.on('disconnected')
def test_disconnect(data):
    send("User {} has disconnected.".format(data), brsoadcast=True)
    
@socketio.on('client-send-data')
def test_emit(data):
    print("data recived: {}".format(data))
    send(data, broadcast=True)

@socketio.on('client-send-private-data')
def test_send_private_data(value):
    client_msg =  value
    server_msg = "response from " + value
    ans = dict()
    ans['client_msg'] = client_msg
    ans['server_msg'] = server_msg
    print("Ans: {}".format(ans))
    socketio.emit('private-data', ans)
    
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    socketio.run(app)
