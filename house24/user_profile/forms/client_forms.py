from django import forms

from db.models.user import User


class OwnerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronym', 'birthday', 'phone_number',
                  'viber', 'telegram', 'email', 'about', 'photo', 'number')
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control to_valid'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control to_valid'}),
            'patronym': forms.TextInput(attrs={'id': 'patronym', 'class': 'form-control to_valid'}),
            'birthday': forms.DateInput(attrs={'id': 'date', 'class': 'form-control to_valid', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control to_valid',
                                                   'placeholder': '+380638271139'}),
            'viber': forms.TextInput(attrs={'id': 'viber', 'class': 'form-control to_valid',
                                            'placeholder': '+380638271139'}),
            'telegram': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control to_valid',
                                               'placeholder': '@nickname or +380638271139'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control to_valid'}),
            'about': forms.Textarea(attrs={'id': 'about', 'class': 'form-control to_valid',
                                           'style': 'height: 299px;'}),
            'photo': forms.FileInput(attrs={'id': 'photo', 'class': 'form-control-file to_valid'}),
            'number': forms.NumberInput(attrs={'id': 'number', 'class': 'form-control to_valid', 'min': '0'})
        }

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