from django import forms

from db.models.user import User
from db.models.house import PaymentTicket, PaymentTicketService, Section, Flat

import datetime


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


class CreatePaymentTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        house_pk = kwargs.pop('house_pk', None)
        super().__init__(*args, **kwargs)
        if house_pk:
            self.fields['section'].queryset = Section.objects.filter(house__pk=house_pk)
            self.fields['flat'].queryset = Flat.objects.filter(house__pk=house_pk)

    class Meta:
        model = PaymentTicket
        exclude = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number',
                                               'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'status'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_done'}),
            'start': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                                 'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                                 'class': "form-control to_valid", 'id': 'start'}),
            'end': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                              'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                              'class': "form-control to_valid", 'id': 'end'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'}),
            'personal_account': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'account'}),
            'tariff': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'tariff'}),
            'sum': forms.HiddenInput(attrs={'class': 'form-control to_valid', 'id': 'ticket_sum'}),
            'created': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': "date",
                                                                   'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                                   'class': "form-control to_valid", 'id': 'created'})
        }


class TicketServiceForm(forms.ModelForm):
    class Meta:
        model = PaymentTicketService
        exclude = ('payment_ticket', )
        widgets = {
            'id': forms.HiddenInput(),
            'service': forms.Select(attrs={'class': 'form-control to_valid service'}),
            'outcome': forms.NumberInput(attrs={'class': 'form-control to_valid outcome', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control to_valid unit_price',
                                                   'min': '0'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control to_valid cost', 'min': '0'}),
        }


TicketServiceFormset = forms.inlineformset_factory(PaymentTicket, PaymentTicketService,
                                                   form=TicketServiceForm, extra=0, can_delete=True)
