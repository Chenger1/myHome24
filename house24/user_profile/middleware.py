from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class CheckUserProfileAccess(MiddlewareMixin):
    def process_request(self, request):
        if '/user_profile/' in request.path:
            if request.user.is_authenticated:
                return self.get_response(request)
            return redirect('website:main_page_view')
        return self.get_response(request)
