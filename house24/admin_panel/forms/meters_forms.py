from django import forms

from db.models.house import House, Section, Service, Meter


class SearchMeasureForm(forms.Form):
    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))


class CreateMeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number'}),
            'date': forms.DateInput(attrs={'class': 'form-control to valid', 'id': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'status'}),
            'data': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'data'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'service': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'service'})
        }
