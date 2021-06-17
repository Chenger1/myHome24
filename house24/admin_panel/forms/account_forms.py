from django import forms

from db.models.house import PersonalAccount, House, Section, Flat, Floor
from db.models.user import User


class PersonalAccountForm(forms.ModelForm):
    class Meta:
        model = PersonalAccount
        fields = '__all__'


class AccountSearchForm(forms.Form):
    debt_choices = [
        ('', 'Выберите...'),
        (0, 'Нет долга'),
        (1, 'Есть долг')
    ]
    status_choices = [
        ('', 'Выберите...'),
        (0, 'Активен'),
        (1, 'Неактивен')
    ]

    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=False)
    house = forms.ModelChoiceField(queryset=House.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False, empty_label='Выберите...')
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False, empty_label='Выберите...')
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=False)
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False, empty_label='Выберите...')
    debt = forms.ChoiceField(choices=debt_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                             required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)


class CreatePersonalAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        house_pk = kwargs.pop('house_pk', None)
        super().__init__(*args, **kwargs)
        if house_pk:
            self.fields['section'].queryset = Section.objects.filter(house__pk=house_pk)
            self.fields['flat'].queryset = Flat.objects.filter(house__pk=house_pk)

    status_choices = [
        (0, 'Активен'),
        (1, 'Неактивен')
    ]
    status = forms.ChoiceField(choices=status_choices,
                               widget=forms.Select(attrs={'class': 'form-control to_valid', 'id': 'status'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-control to_valid', 'id': 'house'}),
                                   required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label='Выберите...',
                                     widget=forms.Select(attrs={'class': 'form-control to_valid', 'id': 'section'}),
                                     required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-control to_valid', 'id': 'floor'}),
                                   required=False)
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), empty_label='Выберите...',
                                  widget=forms.Select(attrs={'class': 'form-control to_valid', 'id': 'flat'}),
                                  required=False)

    class Meta:
        model = PersonalAccount
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control to_valid', 'id': 'number'})
        }
