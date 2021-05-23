from django import forms


class HouseSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}))
