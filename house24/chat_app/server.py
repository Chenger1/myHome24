import os
from threading import Lock

from flask import Flask, make_response, jsonify

from views import socketio


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'some_secret_key')
socketio.init_app(app)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return make_response(jsonify({'status': 'ok'}))


if __name__ == '__main__':
    socketio.run(app, debug=True)
