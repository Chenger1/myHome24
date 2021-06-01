from django import forms

from db.models.user import User


class PaymentTicketSearch(forms.Form):
    status_choices = [
        (0, 'Оплачена'),
        (1, 'Частично оплачена'),
        (2, 'Неоплачена')
    ]
    done_choices = [
        (0, 'Проведена'),
        (1, 'Не проведена')
    ]

    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    month = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    flat = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    is_done = forms.ChoiceField(choices=done_choices, widget=forms.Select(attrs={'class': 'form-control'}))
