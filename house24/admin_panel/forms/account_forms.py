from django import forms

from db.models.house import PersonalAccount, House, Section, Flat
from db.models.user import User


class PersonalAccountForm(forms.ModelForm):
    class Meta:
        model = PersonalAccount
        fields = '__all__'


class AccountSearchForm(forms.Form):
    debt_choices = [
        (0, 'Нет долга'),
        (1, 'Есть долг')
    ]
    status_choices = [
        (0, 'Активен'),
        (1, 'Неактивен')
    ]

    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                required=False)
    house = forms.ModelChoiceField(queryset=House.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False)
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False)
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False)
    debt = forms.ChoiceField(choices=debt_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                             required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}))


class CreatePersonalAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        house_pk = kwargs.pop('house_pk', None)
        super().__init__(*args, **kwargs)
        if house_pk:
            self.fields['section'].queryset = Section.objects.filter(house__pk=house_pk)
            self.fields['flat'].queryset = Flat.objects.filter(house__pk=house_pk)

    class Meta:
        model = PersonalAccount
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number'}),
            'status': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'status'}),
            'house': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
            'section': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'})
        }
