from app import app
from flask import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connected')
def test_connect(data):
    send("User {} vào phòng".format(data), broadcast=True)

@socketio.on('disconnected')
def test_disconnect(data):
    send("User {} has disconnected.".format(data), brsoadcast=True)
    
@socketio.on('client-send-data')
def test_emit(data):
    print("data recived: {}".format(data))
    send(data, broadcast=True)

@socketio.on('client-send-private-data')
def handle_send_private_data(msg):
    response = "response-> " + msg
    ans = dict()
    ans['client-msg'] = msg
    ans['server-msg'] = response
    print(ans)
    socketio.emit("server-send-private-data", ans, broadcast=False) 

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    socketio.run(app)
