import os
from threading import Lock

from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'some_secret_key')
socketio = SocketIO(app, cors_allowed_origins='*')
thread = None
thread_lock = Lock()

if __name__ == '__main__':
    socketio.run(app)
