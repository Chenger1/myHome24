from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.core.exceptions import SuspiciousOperation
from django.utils.cache import patch_vary_headers
from django.utils.http import http_date

import time


class AdminCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = request.user

        if 'admin' in request.path:
            if user.is_authenticated:
                if request.path == '/admin/' and not request.user.role.statistic:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'accounts/index/' in request.path and not request.user.role.personal_account:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'meters/index/' in request.path and not request.user.role.meters:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'owners/index/' in request.path and not request.user.role.owners:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'master_request/index/' in request.path and not request.user.role.master_request:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'payment_ticket/index/' in request.path and not request.user.role.ticket:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'account-transaction/index/' in request.path and not request.user.role.account_transaction:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'houses/index/' in request.path and not request.user.role.houses:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'flats/index/' in request.path and not request.user.role.flats:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
                elif 'message/index/' in request.path and not request.user.role.messages:
                    return redirect(request.user.role.get_available_url_pattern_by_role())
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
                return redirect('admin_panel:admin_login')
        return self.get_response(request)


def resolve_request_to_session_cookie_name(request):
    if request.path.startswith('/admin') or '/admin_login/' in request.path:
        return f'admin_{settings.SESSION_COOKIE_NAME}'
    else:
        return f'client_{settings.SESSION_COOKIE_NAME}'


class AdminSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        cookie_name = resolve_request_to_session_cookie_name(request)
        session_key = request.COOKIES.get(cookie_name)
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            pass
        else:
            # First check if we need to delete this cookie.
            # The session should be deleted only if the session is entirely empty
            cookie_name = resolve_request_to_session_cookie_name(request)
            if cookie_name in request.COOKIES and empty:
                response.delete_cookie(
                    cookie_name,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                )
            else:
                if accessed:
                    patch_vary_headers(response, ("Cookie",))
                if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
                    if request.session.get_expire_at_browser_close():
                        max_age = None
                        expires = None
                    else:
                        max_age = request.session.get_expiry_age()
                        expires_time = time.time() + max_age
                        expires = http_date(expires_time)
                    # Save the session data and refresh the client cookie.
                    # Skip session save for 500 responses, refs #3881.
                    if response.status_code != 500:
                        try:
                            request.session.save()
                        except UpdateError:
                            raise SuspiciousOperation(
                                "The request's session was deleted before the "
                                "request completed. The user may have logged "
                                "out in a concurrent request, for example."
                            )
                        response.set_cookie(
                            cookie_name,
                            request.session.session_key,
                            max_age=max_age,
                            expires=expires,
                            domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=settings.SESSION_COOKIE_SECURE or None,
                            httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                            samesite=settings.SESSION_COOKIE_SAMESITE,
                        )
        return response
