import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

import mongoengine as me

me.connect('localhost:5000')
db = SQLAlchemy()


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

    @classmethod
    def get_unread_messages(cls, current_user):
        return cls.objects(me.Q(from_user=current_user, read=False) |
                           me.Q(to_user=current_user, read=False))


# SQL Part

class User(db.Model):
    __tablename__ = 'db_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    uuid = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    is_staff = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    photo = db.Column(db.String)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def photo_url(self):
        return f'media/{self.photo}'

    @classmethod
    def get_user_by_uuid(cls, user_uuid):
        return cls.query.filter(cls.uuid == user_uuid).first()
