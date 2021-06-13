from django import forms

from db.models.user import User
from db.models.house import MasterRequest

import datetime


class MasterRequestSearchForm(forms.Form):
    type_choices = [
        ('', 'Выберите...'),
        (0, 'Любой специалист'),
        (1, 'Сантехник'),
        (2, 'Электрик'),
        (3, 'Слесарь')
    ]
    status_choices = [
        ('', 'Выберите...'),
        (0, 'Новое'),
        (1, 'В работе'),
        (2, 'Выполнено')
    ]

    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=False)
    start = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_start'}), required=False)
    end = forms.DateField(widget=forms.HiddenInput(attrs={'id': 'date_end'}), required=False)
    master_type = forms.ChoiceField(choices=type_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                                    required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    flat = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                   empty_label='Выберите...')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    master = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                    empty_label='Выберите...')
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)


class CreateMasterRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = 'Выберите...'
        self.fields['status'].empty_label = 'Выберите...'
        self.fields['flat'].empty_label = 'Выберите...'

    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                   empty_label='Выберите...')

    class Meta:
        model = MasterRequest
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control to_valid",
            }),
            'time':  forms.TimeInput(format=('%H:%M'), attrs={
                'type': "time",
                'value': datetime.datetime.now().strftime('%H:%M'),
                'class': "form-control to_valid",
            }),
            'description': forms.Textarea(attrs={'class': 'form-control to_valid',
                                                 'style': 'resize:none;'}),
            'comment': forms.Textarea(attrs={'id': 'comment'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'flat': forms.Select(attrs={'class': 'form-control'}),
        }
