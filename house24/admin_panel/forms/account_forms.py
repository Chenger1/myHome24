from django import forms

from db.models.house import PersonalAccount


class PersonalAccountForm(forms.ModelForm):
    class Meta:
        model = PersonalAccount
        fields = '__all__'
