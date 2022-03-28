import uuid
from datetime import datetime

import mongoengine as me

me.connect('localhost:5000')


class Chat(me.Document):
    chat_uuid = me.UUIDField(primary_key=True, default=uuid.uuid4)
    user_one = me.UUIDField(required=True)
    user_two = me.UUIDField(required=True)

    @classmethod
    def get_chats_for_user(cls, user_uuid):
        return Chat.objects(me.Q(user_one=user_uuid) | me.Q(user_two=user_uuid))


class Message(me.Document):
    chat = me.ReferenceField(Chat, required=True)
    from_user = me.UUIDField(required=True)
    to_user = me.UUIDField(required=True)
    text = me.StringField(required=True)
    created = me.DateTimeField(default=datetime)
