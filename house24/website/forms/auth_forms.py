from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class AdminLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'type': 'email'}),
            'password1': forms.PasswordInput(attrs={'id': 'password1', 'class': 'form-control',
                                                    'type': 'password'}),
            'password2': forms.PasswordInput(attrs={'id': 'password2', 'class': 'form-control',
                                                    'type': 'password'})
        }
