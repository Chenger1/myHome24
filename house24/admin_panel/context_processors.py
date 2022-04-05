from dataclasses import dataclass

from django.contrib.auth import get_user_model


from chat_app.models import Message


User = get_user_model()


@dataclass
class UnreadMessage:
    text: str
    photo_url: str
    user_full_name: str
    created: str
    to_user: str
    is_staff: bool

    @classmethod
    def prepare_unread_messages(cls, raw_messages):
        user_uuid = [m.from_user for m in raw_messages]
        users = User.objects.filter(uuid__in=user_uuid)

        messages = []
        for message in raw_messages:
            user = next((u for u in users if u.uuid == message.from_user))
            messages.append(UnreadMessage(text=message.text,
                                          photo_url=user.photo_url,
                                          user_full_name=user.full_name,
                                          created=message.created,
                                          to_user=user.pk,
                                          is_staff=user.is_staff))
        return messages


def add_new_users_to_template(request):
    """
    This function send "new_users_query" and "new_users_count" variables to each template.
    """
    new_users = User.objects.filter(status=1)
    return {
        'new_users_query': new_users,
        'new_users_count': new_users.count()
    }


def add_unread_messages_to_template(request):
    if request.user.is_authenticated:
        raw_messages = Message.get_unread_messages(request.user.uuid)
        return {
             'unread_messages': UnreadMessage.prepare_unread_messages(raw_messages)
        }
    return {}
