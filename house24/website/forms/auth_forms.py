from django import forms
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class LoginForm(forms.Form):
    error_messages = {
        'invalid_login': 'Неправильный логин или пароль',
        'not_allowed': 'Войдите через профиль администрации'
    }

    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'type': 'email',
                                                            'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control',
                                                                 'type': 'password', 'placeholder': 'Пароль'}))

    def authenticate_admin(self, request):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = authenticate(request, username=email, password=password)
        if not user:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        elif not user.is_staff:
            raise forms.ValidationError(self.error_messages['not_allowed'])
        else:
            return user
