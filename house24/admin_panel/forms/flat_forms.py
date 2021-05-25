from django import forms

from db.models.house import House, Section, Floor, Flat
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
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False)
    debt = forms.ChoiceField(choices=debt_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                             required=False)


class CreateFlatForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control to_valid select2bs4'}))
    account = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'personal_account',
                                                                 'class': 'form-control to_valid'}))

    class Meta:
        model = Flat
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number'}),
            'square': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'square'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'floor': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'floor'}),
            'tariff': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'tariff'}),
        }
