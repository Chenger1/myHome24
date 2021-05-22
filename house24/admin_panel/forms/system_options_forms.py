from django import forms

from db.models.house import Service, Measure, Tariff, TariffService
from db.models.pages import Credentials


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = '__all__'
        widgets = {
            'measure_name': forms.TextInput(attrs={'class': 'form-control'})
        }


MeasureFormset = forms.modelformset_factory(model=Measure, form=MeasureForm, can_delete=False, extra=1)


class ServiceForm(forms.ModelForm):
    measure = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=Measure.objects.all(), required=True)

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def save(self, commit=True):
        if not self.cleaned_data:
            return False
        super().save(commit=commit)


ServiceFormset = forms.modelformset_factory(model=Service, form=ServiceForm, can_delete=False, extra=1)


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'description', 'class': 'form-control',
                                                 'style': 'resize:none;'})
        }


class TariffServiceBlockForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control service_select'}))
    currency = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control currency', 'disabled': 'true'}),
                               required=False)

    class Meta:
        model = TariffService
        exclude = ('tariff', )
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


TariffServiceBlockFormset = forms.inlineformset_factory(Tariff, TariffService, form=TariffServiceBlockForm,
                                                        can_delete=False, extra=0)


class CredentialsForm(forms.ModelForm):
    class Meta:
        model = Credentials
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'information': forms.Textarea(attrs={'id': 'information', 'class': 'form-control',
                                                 'style': 'resize:none;'})
        }
