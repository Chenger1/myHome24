import logging

from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request, session

from models import Chat, Message


socketio = SocketIO(None, cors_allowed_origins='*')

logger = logging.Logger(__name__)


@socketio.on('connect_event')
def connect_handler(data):
    try:
        session[request.sid] = {'chat_uuid': data['chat_uuid'],
                                'user_uuid': data['user_uuid']}
        join_room(data['chat_uuid'])
    except Exception as e:
        emit('client_info_handler', {'success': False})
    else:
        emit('client_info_handler', {'success': True})
    logger.info('Connected')


@socketio.on('disconnect_event')
def disconnect_handler(data):
    leave_room(data['chat_uuid'])
    emit('client_info_handler', {'success': True})


@socketio.on('send_message')
def send_message(data):
    user_session = session[request.sid]
    chat = Chat.get_chat_by_uuid(user_session['chat_uuid'])
    Message.create_message(data['from_user'],
                           data['to_user'],
                           data['text'],
                           chat)
    emit('client_message_handler', data, broadcast=True, room=user_session['chat_uuid'])
