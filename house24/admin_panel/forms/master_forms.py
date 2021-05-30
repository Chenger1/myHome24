from django import forms

from db.models.user import User


class MasterRequestSearchForm(forms.Form):
    type_choices = [
        (0, 'Любой специалист'),
        (1, 'Сантехник'),
        (2, 'Электрик'),
        (3, 'Слесарь')
    ]
    status_choices = [
        (0, 'Новое'),
        (1, 'В работе'),
        (2, 'Выполнено')
    ]

    number = forms.IntegerField(widgets=forms.NumberInput(attrs={'class': 'form-control'}),
                                required=False)
    time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'}),
                               required=False)
    type = forms.ChoiceField(choices=type_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                             required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    flat = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False),
                                   widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    master = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}),
                               required=False)
