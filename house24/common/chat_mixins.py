import json
from dataclasses import dataclass

from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse

from chat_app.models import Chat, Message


User = get_user_model()


@dataclass
class UserChat:
    to_user_pk: int
    to_user_full_name: str
    chat_uuid: str
    chat_with_admin: bool = False


class ListChatViewMixin(View):
    template = None

    def get(self, request):
        chats = Chat.get_chats_for_user(request.user.uuid)
        context = {'chats': self.transform_chat_obj_to_dataclass(chats, request.user.uuid)}
        return render(request, self.template, context=context)

    def transform_chat_obj_to_dataclass(self, chats, from_user_uuid):
        users_uuid = [chat.get_second_person(from_user_uuid) for chat in chats]
        users = User.objects.filter(uuid__in=users_uuid)

        user_chats = []
        for chat in chats:
            user = next((u for u in users if chat.get_second_person(from_user_uuid) == u.uuid))
            if not user:
                continue

            user_chats.append(UserChat(to_user_pk=user.pk, to_user_full_name=user.full_name,
                                       chat_uuid=chat.chat_uuid,
                                       chat_with_admin=user.is_staff))
        return user_chats


class ChatViewMixin(View):
    template = None

    def get(self, request, to_user):
        to_user = User.objects.get(pk=to_user)
        chat = Chat.get_or_create(request.user.uuid, to_user.uuid)
        messages = Message.get_messages_by_chat(chat)
        Message.set_messages_as_read(chat.chat_uuid, request.user.uuid)
        context = {'chat': chat,
                   'messages': messages,
                   'chat_path': settings.SOCKET_IO_PATH,
                   'to_user': to_user}
        return render(request, self.template, context=context)


class DeleteChatViewMixin(View):
    def get(self, request):
        chats_uuid = json.loads(request.GET.get('chats_uuid'))

        for chat_uuid in chats_uuid:
            Chat.delete_chat(chat_uuid)
        return JsonResponse({'status': 200})
