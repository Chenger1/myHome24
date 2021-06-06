from django import forms

from db.models.user import User
from db.models.house import PaymentItem


class AccountTransactionSearchForm(forms.Form):
    status_choices = [
        (0, 'Непроведен'),
        (1, 'Проведен')
    ]
    income_outcome_choices = [
        (0, 'Приход'),
        (1, 'Расход')
    ]

    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)
    transaction_type = forms.ModelChoiceField(queryset=PaymentItem.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    personal_account = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    income_outcome = forms.ChoiceField(choices=income_outcome_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)
