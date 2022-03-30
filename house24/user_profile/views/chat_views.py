from dataclasses import dataclass

from django.contrib.auth import get_user_model

from common.chat_mixins import ListChatViewMixin, ChatViewMixin, DeleteChatViewMixin


User = get_user_model()


@dataclass
class UserChat:
    to_user_pk: int
    to_user_full_name: str
    chat_uuid: str
    chat_with_admin: bool


class ListChatView(ListChatViewMixin):
    template = 'user_chat/list_chats.html'


class ChatView(ChatViewMixin):
    template = 'user_chat/detail_chat.html'


class DeleteChatView(DeleteChatViewMixin):
    pass
