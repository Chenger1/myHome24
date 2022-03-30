from dataclasses import dataclass

from django.contrib.auth import get_user_model

from common.chat_mixins import ListChatViewMixin, ChatViewMixin, DeleteChatViewMixin
from admin_panel.views.mixins import AdminPermissionMixin


User = get_user_model()


@dataclass
class UserChat:
    to_user_pk: int
    to_user_full_name: str
    chat_uuid: str


class ListChatView(AdminPermissionMixin, ListChatViewMixin):
    template = 'chat/list_chats.html'


class ChatView(AdminPermissionMixin, ChatViewMixin):
    template = 'chat/detail_chat.html'


class DeleteChatView(AdminPermissionMixin, DeleteChatViewMixin):
    pass
