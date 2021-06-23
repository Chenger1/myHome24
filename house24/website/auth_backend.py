from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except ObjectDoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None


class IDBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.filter(is_staff=False).get(number=username)
        except ObjectDoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None
