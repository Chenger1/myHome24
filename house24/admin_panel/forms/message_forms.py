from django import forms

from db.models.house import Message


class MessageSearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Поиск'}))


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control to_valid', 'id': 'title',
                                            'placeholder': 'Тема сообщения:'}),
            'text': forms.Textarea(attrs={'id': 'text', 'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-control', 'id': 'house'}),
            'section': forms.Select(attrs={'class': 'form-control', 'id': 'section'}),
            'floor': forms.Select(attrs={'class': 'form-control', 'id': 'floor'}),
            'flat': forms.Select(attrs={'class': 'form-control', 'id': 'flat'}),
            'with_debt': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'with_debt'})
        }
