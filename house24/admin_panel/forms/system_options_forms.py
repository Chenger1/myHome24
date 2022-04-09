from django import forms
from django.utils.translation import gettext_lazy as _

from db.models.house import Service, Measure, Tariff, TariffService, PaymentItem
from db.models.pages import Credentials


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = '__all__'
        widgets = {
            'measure_name': forms.TextInput(attrs={'class': 'form-control to_valid'})
        }


MeasureFormset = forms.modelformset_factory(model=Measure, form=MeasureForm, can_delete=True, extra=0)


class ServiceForm(forms.ModelForm):
    measure = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control to_valid'}),
                                     queryset=Measure.objects.all(), required=True, empty_label=_('Choose...'))

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control to_valid'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def save(self, commit=True):
        if not self.cleaned_data:
            return False
        super().save(commit=commit)


ServiceFormset = forms.modelformset_factory(model=Service, form=ServiceForm, can_delete=True, extra=0)


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control to_valid'}),
            'description': forms.Textarea(attrs={'id': 'description', 'class': 'form-control to_valid',
                                                 'style': 'resize:none;'})
        }


class TariffServiceBlockForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control service_select to_valid'}),
                                     empty_label=_('Choose...'))
    currency = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control currency to_valid',
                                                             'disabled': 'true'}),
                               required=False)

    class Meta:
        model = TariffService
        exclude = ('tariff', )
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control to_valid', 'min': '0', 'step': '0.01'}),
        }


TariffServiceBlockFormset = forms.inlineformset_factory(Tariff, TariffService, form=TariffServiceBlockForm,
                                                        can_delete=True, extra=0)


class CredentialsForm(forms.ModelForm):
    class Meta:
        model = Credentials
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'information': forms.Textarea(attrs={'id': 'information', 'class': 'form-control',
                                                 'style': 'resize:none;'})
        }


class PaymentItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = _('Choose...')

    class Meta:
        model = PaymentItem
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'type': forms.Select(attrs={'id': 'type', 'class': 'form-control'})
        }
