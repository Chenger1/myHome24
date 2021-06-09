from django.views.generic import ListView

from db.models.house import Message

from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.message_forms import MessageSearchForm


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
