from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AdminCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = request.user

        if 'admin' in request.path:
            if user.is_authenticated:
                if request.path == '/admin/' and not request.user.role.statistic:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'accounts/index/' in request.path and not request.user.role.personal_account:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'meters/index/' in request.path and not request.user.role.meters:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'owners/index/' in request.path and not request.user.role.owners:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'master_request/index/' in request.path and not request.user.role.master_request:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'payment_ticket/index/' in request.path and not request.user.role.ticket:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'account-transaction/index/' in request.path and not request.user.role.account_transaction:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'houses/index/' in request.path and not request.user.role.houses:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'flats/index/' in request.path and not request.user.role.flats:
                    return redirect(request.path.role.get_available_url_pattern_by_role())
                elif 'services/index/' in request.path and not request.user.role.services:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'tariff/index/' in request.path and not request.user.role.tariffs:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'roles/index/' in request.path and not request.user.role.roles:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'user-admin/index/' in request.path and not request.user.role.users:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'credentials/index/' in request.path and not request.user.role.credentials:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'main_page' in request.path or 'about' in request.path or 'services' in request.path \
                     or 'tariffs' in request.path or 'contacts' in request.path:
                    if not request.user.role.site_control:
                        return redirect(request.user.role.get_available_url_pattern_by_role())
            elif 'login/' not in request.path:
                return redirect('website:admin_site_login_view')
        return self.get_response(request)
