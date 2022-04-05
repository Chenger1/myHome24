import os
import environ
from threading import Lock

from flask import Flask, make_response, jsonify

from views import socketio
from models import db


env = environ.Env()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'some_secret_key')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@"
    f"{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"
)

socketio.init_app(app)
db.init_app(app)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return make_response(jsonify({'status': 'ok'}))


if __name__ == '__main__':
    socketio.run(app, debug=True)
