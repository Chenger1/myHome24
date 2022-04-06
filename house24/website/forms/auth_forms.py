from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class ClientLoginForm(forms.Form):
    error_messages = {
        'invalid_login': _('Wrong login or password'),
    }

    login_data = forms.CharField(widget=forms.TextInput(attrs={'id': 'login_data', 'class': 'form-control',
                                                               'placeholder': _('E-mail or ID')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control',
                                                                 'type': 'password', 'placeholder': _('Password')}))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'remember_me'}), required=False)

    def authenticate_client(self, request):
        login_data = self.cleaned_data['login_data']
        password = self.cleaned_data['password']

        user = authenticate(request, username=login_data, password=password)
        if not user:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        else:
            return user
