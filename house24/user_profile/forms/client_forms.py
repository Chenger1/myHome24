from django import forms

from db.models.user import User
from db.models.house import MasterRequest, Transaction

import datetime


class OwnerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronym', 'birthday', 'phone_number',
                  'viber', 'telegram', 'email', 'about', 'photo', 'number')
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control to_valid'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control to_valid'}),
            'patronym': forms.TextInput(attrs={'id': 'patronym', 'class': 'form-control to_valid'}),
            'birthday': forms.DateInput(attrs={'id': 'date', 'class': 'form-control to_valid', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control to_valid',
                                                   'placeholder': '+380638271139'}),
            'viber': forms.TextInput(attrs={'id': 'viber', 'class': 'form-control to_valid',
                                            'placeholder': '+380638271139'}),
            'telegram': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control to_valid',
                                               'placeholder': '@nickname or +380638271139'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control to_valid'}),
            'about': forms.Textarea(attrs={'id': 'about', 'class': 'form-control to_valid',
                                           'style': 'height: 299px;'}),
            'photo': forms.FileInput(attrs={'id': 'photo', 'class': 'form-control-file to_valid'}),
            'number': forms.NumberInput(attrs={'id': 'number', 'class': 'form-control to_valid', 'min': '0'})
        }

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password1', 'class': 'form-control to_valid',
                                                                  'type': 'password'}),
                                required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2', 'class': 'form-control to_valid',
                                                                  'type': 'password'}),
                                required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        else:
            old_pass = User.objects.get(pk=self.instance.pk).password
            user.password = old_pass
        if commit:
            user.save()
        return user


class CreateMasterRequest(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = 'Выберите...'
        self.fields['flat'].empty_label = 'Выберите...'

    class Meta:
        model = MasterRequest
        fields = ('type', 'flat', 'date', 'time', 'description')
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control to_valid",
                'id': 'created'
            }),
            'time':  forms.TimeInput(format=('%H:%M'), attrs={
                'type': "time",
                'value': datetime.datetime.now().strftime('%H:%M'),
                'class': "form-control to_valid",
                'id': 'time'
            }),
            'description': forms.Textarea(attrs={'class': 'form-control to_valid',
                                                 'style': 'resize:none;', 'id': 'description'}),
            'type': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'type'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat',
                                        'required': 'true'}),
        }


class SearchMessageForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'text'}), required=False)


class SearchTicketsForm(forms.Form):
    status_choices = [
        ('', 'Выберите'),
        (0, 'Оплачена'),
        (1, 'Частично оплачена'),
        (2, 'Неоплачена')
    ]

    start = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'date', 'type': 'date'}),
                            required=False)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
                               required=False, choices=status_choices)


class CreateTransaction(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('number', 'created', 'owner', 'personal_account', 'paid_sum', 'payment_ticket',
                  'payment_item_type')
        widgets = {
            'number': forms.HiddenInput(),
            'created': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control to_valid",
                'id': 'created',
            }),
            'personal_account': forms.HiddenInput(),
            'paid_sum': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sum',
                                                 'min': '0'}),
            'payment_ticket': forms.HiddenInput(),
            'payment_item_type': forms.HiddenInput(),
            'owner': forms.HiddenInput()
        }
