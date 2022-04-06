from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from db.models.user import User
from db.models.house import PaymentTicket, PaymentTicketService, Section, Flat, Service, TicketTemplate

import datetime


class PaymentTicketSearchForm(forms.Form):
    status_choices = [
        ('', _('Choose...')),
        (0, _('Paid')),
        (1, _('Partially paid')),
        (2, _('Not paid'))
    ]
    done_choices = [
        ('', _('Choose...')),
        (1, _('Completed')),
        (0, _('Not completed'))
    ]

    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)
    start = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_start'}), required=False)
    end = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_end'}), required=False)
    month = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'month'}),
                            required=False)
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                   empty_label=_('Choose...'))
    is_done = forms.ChoiceField(choices=done_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                                required=False)


class CreatePaymentTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        house_pk = kwargs.pop('house_pk', None)
        super().__init__(*args, **kwargs)
        if house_pk:
            self.fields['section'].queryset = Section.objects.filter(house__pk=house_pk)
            self.fields['flat'].queryset = Flat.objects.filter(house__pk=house_pk)
        self.fields['status'].empty_label = _('Choose...')
        self.fields['section'].empty_label = _('Choose...')
        self.fields['house'].empty_label = _('Choose...')
        self.fields['floor'].empty_label = _('Choose...')
        self.fields['flat'].empty_label = _('Choose...')
        self.fields['personal_account'].empty_label = _('Choose...')
        self.fields['tariff'].empty_label = _('Choose...')

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
            'floor': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'floor'}),
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].empty_label = _('Choose...')
        self.fields['service'].queryset = Service.objects.filter(status=True)

    class Meta:
        model = PaymentTicketService
        exclude = ('payment_ticket', )
        widgets = {
            'id': forms.HiddenInput(),
            'service': forms.Select(attrs={'class': 'form-control to_valid service'}),
            'outcome': forms.NumberInput(attrs={'class': 'form-control to_valid outcome', 'min': '0',
                                                'step': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control to_valid unit_price',
                                                   'min': '0', 'step': '0.01'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control to_valid cost', 'min': '0', 'step': '0.01'}),
        }


TicketServiceFormset = forms.inlineformset_factory(PaymentTicket, PaymentTicketService,
                                                   form=TicketServiceForm, extra=0, can_delete=True)


class AddHtmlTemplate(forms.ModelForm):
    class Meta:
        model = TicketTemplate
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control to_valid', 'id': 'name'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file to_valid', 'id': 'file',
                                           'accept': '.html', 'placeholder': 'pdf_*.html'})
        }

    def clean(self):
        file = self.cleaned_data.get('file')
        if not file:
            # Because the file is required, the only way to have empty file field is wrong type
            raise ValidationError(_('Wrong file format. Required format - .html'))

        if not file.name.startswith('pdf_'):
            raise ValidationError('Filename does not match standard. It should star with "pdf_"')
