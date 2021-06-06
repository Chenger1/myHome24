from django import forms

from db.models.user import User
from db.models.house import PaymentItem, Transaction

import datetime


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


class CreateIncomeForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'id': 'owner', 'class': 'form-control to_valid'}),
                                   required=False)
    manager = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                     widget=forms.Select(attrs={'id': 'manager', 'class': 'form-control to_valid'}),
                                     required=False)
    payment_item_type = forms.ModelChoiceField(queryset=PaymentItem.objects.filter(type=0),
                                               widget=forms.Select(attrs={'id': 'payment_type',
                                                                          'class': 'form-control to_valid'}))

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid',
                                               'id': 'number'}),
            'created': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                                   'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                                   'class': "form-control to_valid", 'id': 'created'}),
            'personal_account': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'account'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'amount'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input to_valid',
                                                 'id': 'status'}),
            'description': forms.Textarea(attrs={'class': 'form-control to_valid',
                                                 'id': 'description', 'style': 'resize:none;'})
        }


class CreateOutcomeForm(forms.ModelForm):
    payment_item_type = forms.ModelChoiceField(queryset=PaymentItem.objects.filter(type=1),
                                               widget=forms.Select(attrs={'id': 'payment_type',
                                                                          'class': 'form-control to_valid'}))
    manager = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                     widget=forms.Select(attrs={'id': 'manager', 'class': 'form-control to_valid'}),
                                     required=False)

    class Meta:
        model = Transaction
        exclude = ('owner', 'personal_account')
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid',
                                               'id': 'number'}),
            'created': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                                   'value': datetime.datetime.now().strftime(
                                                                       '%Y-%m-%d'),
                                                                   'class': "form-control to_valid", 'id': 'created'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'amount'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input to_valid',
                                                 'id': 'status'}),
            'description': forms.Textarea(attrs={'class': 'form-control to_valid',
                                                 'id': 'description', 'style': 'resize:none;'})
        }
