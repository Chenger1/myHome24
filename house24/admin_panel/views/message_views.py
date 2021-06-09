from django.views.generic import ListView, CreateView, View, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from db.models.house import Message

from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.message_forms import MessageSearchForm, CreateMessageForm
from admin_panel.views.mixins import DeleteInstanceView

import json


class ListMessages(AdminPermissionMixin, ListView):
    model = Message
    template_name = 'message/list_messages_admin.html'
    context_object_name = 'messages'
    paginate_by = 20
    search_form = MessageSearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.search_form()
        return context


class CreateMessageView(AdminPermissionMixin, CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = 'message/create_message_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_messages_admin')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.sender = self.request.user
        return super().form_valid(form)


class DeleteMessagesView(View):
    model = Message

    def get(self, request):
        pks = json.loads(request.GET.get('pk'))
        for pk in pks:
            get_object_or_404(self.model, pk=pk).delete()
        return JsonResponse({'status': 200})


class DetailMessageView(AdminPermissionMixin, DetailView):
    model = Message
    template_name = 'message/detail_message_admin.html'
    context_object_name = 'message'


class DeleteMessageView(DeleteInstanceView):
    model = Message
    redirect_url = 'admin_panel:list_messages_admin'
