from django.views.generic import CreateView, View, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

from db.models.house import Message, InviteMessage
from db.services.search import MessageSearch

from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.message_forms import MessageSearchForm, CreateMessageForm, CreateInviteMessageForm
from admin_panel.views.mixins import DeleteInstanceView, ListInstancesMixin

import json


class ListMessages(ListInstancesMixin):
    model = Message
    template_name = 'message/list_messages_admin.html'
    search_form = MessageSearchForm
    search_obj = MessageSearch

    def get_context_data(self):
        context = super().get_context_data()
        context['invites'] = InviteMessage.objects.all()
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


class CreateMessageWithDebtView(CreateMessageView):
    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.form_class(request.POST)
        else:
            form = self.form_class(initial={'with_debt': True})
        return form


class DeleteMessagesView(View):
    def get(self, request):
        pks = json.loads(request.GET.get('pk'))
        for pk in pks:
            try:
                Message.objects.get(pk=pk).delete()
            except ObjectDoesNotExist:
                get_object_or_404(InviteMessage, pk=pk).delete()
        return JsonResponse({'status': 200})


class DetailMessageView(AdminPermissionMixin, DetailView):
    model = Message
    template_name = 'message/detail_message_admin.html'
    context_object_name = 'message'


class DeleteMessageView(DeleteInstanceView):
    model = Message
    redirect_url = 'admin_panel:list_messages_admin'


class CreateInviteMessageView(AdminPermissionMixin, CreateView):
    model = InviteMessage
    form_class = CreateInviteMessageForm
    success_url = reverse_lazy('admin_panel:list_owners_admin')
    template_name = 'message/create_invite_message.html'
