from django.shortcuts import render
from django.views import View

from chat_app.models import Chat


class ListChatView(View):
    def get(self, request):
        chats = Chat.get_chats_for_user(request.user.uuid)
        context = {'chats': chats}
        return render(request, 'chat/list_chats.html', context=context)


class ChatView(View):
    pass
