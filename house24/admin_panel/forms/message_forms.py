from django import forms


class MessageSearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Поиск'}))
