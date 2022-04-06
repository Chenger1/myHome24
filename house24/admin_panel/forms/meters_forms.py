from django import forms
from django.utils.translation import gettext_lazy as _

from db.models.house import House, Section, Service, Meter, Flat

from datetime import datetime


class SearchMeasureForm(forms.Form):
    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False, empty_label=_('Choose...'))
    section = forms.ModelChoiceField(queryset=Section.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False, empty_label=_('Choose...'))
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False, empty_label=_('Choose...'))


class SearchMeasureHistoryForm(forms.Form):
    status_choices = [
        ('', _('Choose...')),
        (0, _('New')),
        (1, _('Accounted')),
        (2, _('Accounted and paid')),
        (3, _('Zero'))
    ]

    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False, empty_label=_('Choose...'))
    section = forms.ModelChoiceField(queryset=Section.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False, empty_label=_('Choose...'))
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False, empty_label=_('Choose...'))
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    flat = forms.CharField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)
    start = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_start'}), required=False)
    end = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_end'}), required=False)


class CreateMeterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        house_pk = kwargs.pop('house_pk', None)
        super().__init__(*args, **kwargs)
        if house_pk:
            self.fields['section'].queryset = Section.objects.filter(house__pk=house_pk)
            self.fields['flat'].queryset = Flat.objects.filter(house__pk=house_pk)
        self.fields['flat'].empty_label = _('Choose...')
        self.fields['section'].empty_label = _('Choose...')
        self.fields['floor'].empty_label = _('Choose...')
        self.fields['house'].empty_label = _('Choose...')
        self.fields['service'].empty_label = _('Choose...')
        self.fields['service'].queryset = Service.objects.filter(status=True)

    class Meta:
        model = Meter
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number', 'min': '0'}),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control to_valid",
            }),
            'status': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'status'}),
            'data': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'data', 'min': '0'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'floor': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'floor'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'service': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'service'})
        }
