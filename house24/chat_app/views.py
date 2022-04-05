import logging
import eventlet

from flask_socketio import SocketIO, join_room, leave_room, emit, Namespace
from flask import request, session

from models import Chat, Message, User


# eventlet.monkey_patch()
socketio = SocketIO(None, cors_allowed_origins='*')

logger = logging.Logger(__name__)


class ChatNamespace(Namespace):
    def on_connect_event(self, data):
        try:
            session[request.sid] = {'chat_uuid': data['chat_uuid'],
                                    'user_uuid': data['user_uuid']}
            join_room(data['chat_uuid'])
            join_room(f'notifications-{data["user_uuid"]}')
        except Exception as e:
            emit('client_info_handler', {'success': False,
                                         'type': 'connect'})
        else:
            emit('client_info_handler', {'success': True,
                                         'type': 'connect'})
        logger.info('Connected')

    def on_connect_notification_event(self, data):
        notification_room_name = f'notifications-{data["user_uuid"]}'
        join_room(notification_room_name)
        emit('client_info_handler', {'success': True, 'type': 'connect'})

    def on_set_messages_as_read(self, data):
        count = Message.set_messages_as_read(data['chat_uuid'], data['user_uuid'])
        emit('read_message_response', {'count': count})

    def on_set_single_message_as_read(self, data):
        msg = Message.objects(pk=data['message_id']).first()
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

        user_notification_room = f'notifications-{data["to_user"]}'
        user = User.get_user_by_uuid(data['from_user'])
        data['user_full_name'] = user.full_name
        data['user_photo'] = user.photo_url
        data['user_pk'] = user.id
        data['is_staff'] = user.is_staff
        emit('notify_response', data, room=user_notification_room, broadcast=True)


socketio.on_namespace(ChatNamespace('/chat'))
