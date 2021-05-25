from django import forms

from db.models.house import House, Section, Floor
from db.models.user import User


class FlatSearchForm(forms.Form):
    debt_choices = [
        (0, 'Нет долга'),
        (1, 'Есть долг')
    ]

    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                required=False)
    house = forms.ModelChoiceField(queryset=House.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False)
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    debt = forms.ChoiceField(choices=debt_choices, widget=forms.Select(attrs={'class': 'form-control'}))
