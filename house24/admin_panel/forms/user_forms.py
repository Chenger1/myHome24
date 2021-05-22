from django import forms

from db.models.user import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        exclude = ('name', )
        widgets = {
            'statistic': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                    'type': 'checkbox'}),
            'cashbox': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                  'type': 'checkbox'}),
            'ticket': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                 'type': 'checkbox'}),
            'personal_account': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                           'type': 'checkbox'}),
            'flats': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                'type': 'checkbox'}),
            'owners': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                 'type': 'checkbox'}),
            'houses': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                 'type': 'checkbox'}),
            'messages': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                   'type': 'checkbox'}),
            'master_request': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                         'type': 'checkbox'}),
            'meters': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                 'type': 'checkbox'}),
            'site_control': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                       'type': 'checkbox'}),
            'services': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                   'type': 'checkbox'}),
            'tariffs': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                  'type': 'checkbox'}),
            'roles': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                'type': 'checkbox'}),
            'users': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                'type': 'checkbox'}),
            'credentials': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                      'type': 'checkbox'})
        }


RoleFormSet = forms.formset_factory(RoleForm, can_delete=False, extra=0)
