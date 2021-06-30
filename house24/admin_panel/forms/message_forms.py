from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from db.models.house import Message, InviteMessage

User = get_user_model()


class MessageSearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Поиск'}),
                           required=False)


class CreateMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].empty_label = 'Всем'
        self.fields['section'].empty_label = 'Всем'
        self.fields['floor'].empty_label = 'Всем'
        self.fields['flat'].empty_label = 'Всем'

    class Meta:
        model = Message
        exclude = ('sender', )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control to_valid', 'id': 'title',
                                            'placeholder': 'Тема сообщения:'}),
            'text': forms.Textarea(attrs={'id': 'text', 'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'floor': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'floor'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'}),
            'with_debt': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'with_debt'}),
            'owner': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'owner'})
        }


class CreateInviteMessageForm(forms.ModelForm):
    class Meta:
        model = InviteMessage
        exclude = ('user', )
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control to_valid', 'id': 'phone',
                                            'placeholder': '+380638271139'}),
            'text': forms.TextInput(attrs={'class': 'form-control to_valid', 'id': 'text',
                                           'placeholder': 'Сообщение для клиента'})
        }

    def clean(self):
        phone = self.cleaned_data.get('phone')
        if not User.objects.filter(phone_number=phone).exists():
            raise ValidationError('Пользователя с таким номером телефона нет в системе')
