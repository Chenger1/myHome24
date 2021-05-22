from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AdminCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = request.user

        if 'admin' in request.path:
            if user.is_authenticated:
                if request.path == '/admin/' and not request.user.role.statistic:
                    raise Http404()
                elif 'services/index/' in request.path and not request.user.role.services:
                    raise Http404()
                elif 'tariff/index/' in request.path and not request.user.role.tariffs:
                    raise Http404()
                elif 'roles/index/' in request.path and not request.user.role.roles:
                    raise Http404()
                elif 'user-admin/index/' in request.path and not request.user.role.users:
                    raise Http404()
                elif 'credentials/index/' in request.path and not request.user.role.credentials:
                    raise Http404()
                elif 'main_page' in request.path or 'about' in request.path or 'services' in request.path \
                     or 'tariffs' in request.path or 'contacts' in request.path:
                    if not request.user.role.site_control:
                        raise Http404()
            elif 'login/' not in request.path:
                return redirect('website:admin_site_login_view')
        return self.get_response(request)
