from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class AdminPermissionMixin(PermissionRequiredMixin):
    permission_required = ('is_staff', 'is_superuser')
    login_url = reverse_lazy('website:admin_site_login_view')
    permission_denied_message = _('This user doesnt have access to this page')

    def has_permission(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return False
