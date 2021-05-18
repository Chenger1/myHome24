from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy


class AdminPermissionMixin(PermissionRequiredMixin):
    permission_required = ('is_staff', 'is_superuser')
    login_url = reverse_lazy('website:admin_site_login_view')
    permission_denied_message = 'У этого пользователя нет доступа к данной странице'

    def has_permission(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return False
