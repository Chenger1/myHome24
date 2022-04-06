from django import forms
from django.utils.translation import gettext_lazy as _

from db.models.user import User
from db.models.house import PaymentItem, Transaction, PersonalAccount, PaymentTicket

import datetime


class AccountTransactionSearchForm(forms.Form):
    status_choices = [
        ('', _('Choose...')),
        (0, _('Not completed')),
        (1, _('Completed'))
    ]
    income_outcome_choices = [
        ('', _('Choose')),
        (0, _('Income')),
        (1, _('Outcome'))
    ]

    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)
    payment_item_type = forms.ModelChoiceField(queryset=PaymentItem.objects.all(),
                                               widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                               empty_label=_('Choose'))
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                   empty_label=_('Choose'))
    personal_account = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
                                          required=False)
    income_outcome = forms.ChoiceField(choices=income_outcome_choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    start = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_start'}), required=False)
    end = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_end'}), required=False)


class CreateIncomeForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'id': 'owner', 'class': 'form-control to_valid'}),
                                   required=False, empty_label=_('Choose...'))
    manager = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                     widget=forms.Select(attrs={'id': 'manager', 'class': 'form-control to_valid'}),
                                     required=False, empty_label=_('Choose...'))
    payment_item_type = forms.ModelChoiceField(queryset=PaymentItem.objects.filter(type=0),
                                               widget=forms.Select(attrs={'id': 'payment_type',
                                                                          'class': 'form-control to_valid'}),
                                               empty_label=_('Choose...'))
    personal_account = forms.ModelChoiceField(queryset=PersonalAccount.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-control to_valid',
                                                                         'id': 'account'}),
                                              empty_label=_('Choose...'), required=False)
    payment_ticket = forms.ModelChoiceField(queryset=PaymentTicket.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control to_valid',
                                                                       'id': 'payment_ticket'},),
                                            empty_label=_('Choose...'), required=False)

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid',
                                               'id': 'number', 'min': '0'}),
            'created': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                                   'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                                   'class': "form-control to_valid", 'id': 'created'}),
            'paid_sum': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'paid_sum', 'min': '0',
                                                 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input to_valid',
                                                 'id': 'status'}),
            'description': forms.Textarea(attrs={'class': 'form-control to_valid',
                                                 'id': 'description', 'style': 'resize:none;',
                                                 'maxlength': '2000'})
        }


class CreateOutcomeForm(forms.ModelForm):
    payment_item_type = forms.ModelChoiceField(queryset=PaymentItem.objects.filter(type=1),
                                               widget=forms.Select(attrs={'id': 'payment_type',
                                                                          'class': 'form-control to_valid'}),
                                               empty_label=_('Choose...'))
    manager = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                     widget=forms.Select(attrs={'id': 'manager', 'class': 'form-control to_valid'}),
                                     required=False, empty_label=_('Choose...'))

    class Meta:
        model = Transaction
        exclude = ('owner', 'personal_account', 'transaction')
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid',
                                               'id': 'number', 'min': '0'}),
            'created': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                                   'value': datetime.datetime.now().strftime(
                                                                       '%Y-%m-%d'),
                                                                   'class': "form-control to_valid", 'id': 'created'}),
            'paid_sum': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'paid_sum', 'min': '0',
                                                 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input to_valid',
                                                 'id': 'status'}),
            'description': forms.Textarea(attrs={'class': 'form-control to_valid',
                                                 'id': 'description', 'style': 'resize:none;',
                                                 'maxlength': '2000'})
        }
