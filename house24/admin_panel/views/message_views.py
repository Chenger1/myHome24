from django.views.generic import ListView

from db.models.house import Message

from admin_panel.permission_mixin import AdminPermissionMixin


class ListMessages(AdminPermissionMixin, ListView):
    model = Message
    template_name = 'message/list_message_admin.html'
    context_object_name = 'messages'
    paginate_by = 20
