from django.contrib.auth import get_user_model

from admin_panel.views.mixins import ListUsersViewMixin

User = get_user_model()


class ListOwnerView(ListUsersViewMixin):
    model = User
    template_name = 'owner/list_owners.html'
    context_object_name = 'users'
    is_staff = False
