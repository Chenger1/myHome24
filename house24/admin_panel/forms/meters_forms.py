from django import forms

from db.models.house import House, Section, Service, Meter, Flat

from datetime import datetime


class SearchMeasureForm(forms.Form):
    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))


class CreateMeterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        house_pk = kwargs.pop('house_pk', None)
        super().__init__(*args, **kwargs)
        if house_pk:
            self.fields['section'].queryset = Section.objects.filter(house__pk=house_pk)
            self.fields['flat'].queryset = Flat.objects.filter(house__pk=house_pk)

    class Meta:
        model = Meter
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number'}),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control to_valid",
            }),
            'status': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'status'}),
            'data': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'data'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'service': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'service'})
        }
