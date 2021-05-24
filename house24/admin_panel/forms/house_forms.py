from django import forms

from db.models.house import House, Section, Floor
from db.models.user import User


class HouseSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}))


class CreateHouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ('user', )
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'id': 'image1', 'class': 'form-control-file'}),
            'image2': forms.FileInput(attrs={'id': 'image2', 'class': 'form-control-file'}),
            'image3': forms.FileInput(attrs={'id': 'image3', 'class': 'form-control-file'}),
            'image4': forms.FileInput(attrs={'id': 'image4', 'class': 'form-control-file'}),
            'image5': forms.FileInput(attrs={'id': 'image5', 'class': 'form-control-file'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                  widget=forms.Select(attrs={'class': 'form-control users_select'}))


SectionFormset = forms.inlineformset_factory(House, Section,
                                             form=SectionForm, can_delete=False, extra=0)


FloorFormset = forms.inlineformset_factory(House, Floor,
                                           form=FloorForm, can_delete=False, extra=0)

UserFormset =forms.formset_factory(UserForm, can_delete=False, extra=0)
