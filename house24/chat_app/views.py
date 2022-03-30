import logging
import eventlet

from flask_socketio import SocketIO, join_room, leave_room, emit, Namespace
from flask import request, session

from models import Chat, Message


# eventlet.monkey_patch()
socketio = SocketIO(None, cors_allowed_origins='*')

logger = logging.Logger(__name__)


@socketio.on('notify_event')
def notify_event(data):
    emit('notify_response', data)


class ChatNamespace(Namespace):
    def on_connect_event(self, data):
        try:
            session[request.sid] = {'chat_uuid': data['chat_uuid'],
                                    'user_uuid': data['user_uuid']}
            join_room(data['chat_uuid'])
        except Exception as e:
            emit('client_info_handler', {'success': False,
                                         'type': 'connect'})
        else:
            emit('client_info_handler', {'success': True,
                                         'type': 'connect'})
        logger.info('Connected')

    def on_set_messages_as_read(self, data):
        count = Message.set_messages_as_read(data['chat_uuid'], data['user_uuid'])
        emit('read_message_response', {'count': count})

    def on_set_single_message_as_read(self, data):
        msg = Message.objects(pk=data['message_id'])
        msg.read = True
        msg.save()
        emit('client_info_handler', {'success': True,
                                     'type': 'read'})

    def on_disconnect_event(self, data):
        leave_room(data['chat_uuid'])
        emit('client_info_handler', {'success': True,
                                     'type': 'disconnect'})

    def on_send_message(self, data):
        user_session = session[request.sid]
        chat = Chat.get_chat_by_uuid(user_session['chat_uuid'])
        msg = Message.create_message(data['from_user'],
                                     data['to_user'],
                                     data['text'],
                                     chat)
        data['message_id'] = str(msg.pk)
        data['created_time'] = msg.created_time
        emit('client_message_handler', data, broadcast=True, room=user_session['chat_uuid'])


socketio.on_namespace(ChatNamespace('/chat'))

