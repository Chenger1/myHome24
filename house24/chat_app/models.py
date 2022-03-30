import uuid
from datetime import datetime

import mongoengine as me

me.connect('localhost:5000')


class Chat(me.Document):
    chat_uuid = me.UUIDField(primary_key=True, default=uuid.uuid4)
    user_one = me.UUIDField(required=True)
    user_two = me.UUIDField(required=True)

    def get_second_person(self, first_person):
        if self.user_one != first_person:
            return self.user_one
        return self.user_two

    @classmethod
    def get_chats_for_user(cls, user_uuid):
        return Chat.objects(me.Q(user_one=user_uuid) | me.Q(user_two=user_uuid))

    @classmethod
    def get_or_create(cls, user_one_uuid, user_two_uuid):
        chat = Chat.objects(me.Q(user_one=user_one_uuid, user_two=user_two_uuid) | me.Q(user_one=user_two_uuid,
                                                                                        user_two=user_one_uuid)).first()
        if not chat:
            chat = Chat(user_one=user_one_uuid,
                        user_two=user_two_uuid)
            chat.save()
        return chat

    @classmethod
    def get_chat_by_uuid(cls, chat_uuid):
        return cls.objects(chat_uuid=chat_uuid).first()

    @classmethod
    def delete_chat(cls, chat_uuid):
        cls.objects(chat_uuid=chat_uuid).delete()


class Message(me.Document):
    chat = me.ReferenceField(Chat, required=True)
    from_user = me.UUIDField(required=True)
    to_user = me.UUIDField(required=True)
    text = me.StringField(required=True)
    created = me.DateTimeField(default=datetime.now)

    read = me.BooleanField(default=False)

    @property
    def created_time(self):
        return self.created.strftime('%H:%M')

    @classmethod
    def get_messages_by_chat(cls, chat):
        return Message.objects(chat=chat)

    @classmethod
    def create_message(cls, from_user, to_user, text, chat):
        msg = cls(from_user=from_user,
                  to_user=to_user,
                  text=text,
                  chat=chat).save()
        return msg

    @classmethod
    def set_messages_as_read(cls, chat_uuid, current_user):
        chat = Chat.objects(chat_uuid=chat_uuid).first()
        messages = cls.objects(me.Q(chat=chat, read=False, from_user__ne=current_user) |
                               me.Q(chat=chat, read=False, to_user__ne=current_user))
        for msg in messages:
            msg.read = True
            msg.save()
        return messages.count()
