from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError

from db.models.user import Role
from db.models.house import House, Flat


User = get_user_model()


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


RoleFormSet = forms.modelformset_factory(model=Role, form=RoleForm, extra=0, can_delete=False)


class SearchForm(forms.Form):
    status_choices = [
        (0, 'Активен'),
        (1, 'Новый'),
        (2, 'Отключен')
    ]
    debt_choices = [
        (0, 'Да')
    ]

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    role = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                  queryset=Role.objects.all(), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=status_choices, required=False)

    id_field = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'id_field',
                                                                  'class': 'form-control'}), required=False)
    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   widget=forms.Select(attrs={'id': 'house',
                                                              'class': 'form-control'}), required=False)
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(),
                                  widget=forms.Select(attrs={'id': 'flat',
                                                             'class': 'form-control'}), required=False)
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'id': 'date',
                                                                'class': 'form-control'}), required=False)
    is_debt = forms.ChoiceField(choices=debt_choices,
                                widget=forms.Select(attrs={'id': 'is_debt',
                                                           'class': 'form-control'}), required=False)


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'role', 'status',
                  'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control to_valid'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control to_valid'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control to_valid',
                                                   'placeholder': '+380638271139'}),
            'status': forms.Select(attrs={'id': 'status', 'class': 'form-control to_valid'}),
            'role': forms.Select(attrs={'id': 'role', 'class': 'form-control to_valid'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control to_valid'})
        }

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password2 != password1:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        update_last_login(None, user)
        return user


class CreateAdminUserForm(AdminUserForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password1', 'class': 'form-control to_valid',
                                                                  'type': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2', 'class': 'form-control to_valid',
                                                                  'type': 'password'}))


class UpdateAdminUserForm(AdminUserForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password1', 'class': 'form-control to_valid',
                                                                  'type': 'password'}),
                                required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2', 'class': 'form-control to_valid',
                                                                  'type': 'password'}),
                                required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        else:
            old_pass = User.objects.get(pk=self.instance.pk).password
            user.password = old_pass
        if commit:
            user.save()
        return user
