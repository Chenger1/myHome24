from django import forms
from django.utils.translation import gettext_lazy as _

from db.models.user import User, Role
from db.models.house import MasterRequest

import datetime


class MasterRequestSearchForm(forms.Form):
    type_choices = [
        ('', _('Choose...')),
        (0, _('Any master')),
        (1, _('Plumber')),
        (2, _('Electrician')),
        (3, _('Locksmith'))
    ]
    status_choices = [
        ('', _('Choose...')),
        (0, _('New')),
        (1, _('In progress')),
        (2, _('Done'))
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
                                   empty_label=_('Choose...'))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    master = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                    empty_label=_('Choose...'))
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)


class CreateMasterRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = _('Choose...')
        self.fields['status'].empty_label = _('Choose...')
        self.fields['flat'].empty_label = _('Choose...')

    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                   empty_label=_('Choose...'))
    type = forms.ModelChoiceField(queryset=Role.objects.exclude(name='Director'),
                                  widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                  empty_label=_('Any master'))
    master = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True).exclude(role__name='Director'),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False,
                                    empty_label=_('Choose...'))

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
                                                 'style': 'resize:none;', 'maxlength': '2000'}),
            'comment': forms.Textarea(attrs={'id': 'comment'}),
            'status': forms.Select(attrs={'class': 'form-control to_valid'}),
            'flat': forms.Select(attrs={'class': 'form-control to_valid'}),
        }
