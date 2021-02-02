from app import app
from flask import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connected')
def test_connect(data):
    print("User {} has connected.".format(data))
     
@socketio.on('client-send-data')
def test_emit(data):
    print("data recived: {}".format(data))
    send(data, broadcast=True)

@socketio.on('client-send-multiple-messages')
def handle_send_multiple_messages(msg):
    emit("server-send-multiple-message")


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    socketio.run(app)
