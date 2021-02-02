from app import app
from flask import request
from app.mod_pages.socketio import socketio 

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    socketio.run(app)
    