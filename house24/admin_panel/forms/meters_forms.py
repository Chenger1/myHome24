from django import forms

from db.models.house import House, Section, Service


class SearchMeasureForm(forms.Form):
    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
