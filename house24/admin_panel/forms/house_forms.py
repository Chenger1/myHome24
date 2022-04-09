from django import forms
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from db.models.house import House, Section, HouseUser
from db.models.user import User


class HouseSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
                           required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}),
                              required=False)


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
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=False)

    class Meta:
        model = Section
        fields = ('name', )


class FloorForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control to_valid'}),
                           required=False)
    sections = forms.ModelMultipleChoiceField(queryset=Section.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control ' +
                                                                                          'to_valid section_select',
                                                                                 'multiple': 'true'}),
                                              required=False)


class HouseUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                  widget=forms.Select(attrs={'class': 'form-control users_select'}),
                                  empty_label=_('Choose...'))

    class Meta:
        model = HouseUser
        fields = '__all__'


SectionFormset = forms.inlineformset_factory(House, Section,
                                             form=SectionForm, can_delete=True, extra=0)

FloorFormset = forms.formset_factory(form=FloorForm, can_delete=True)

UserFormset = forms.inlineformset_factory(parent_model=House, model=HouseUser, form=HouseUserForm,
                                          extra=0, can_delete=True)


def create_floor_formset(floor_queryset, section_queryset):
    floor_queryset_distinct = floor_queryset.distinct('name')  # otherwise we will see duplicates on page
    formset_factory = forms.formset_factory(form=FloorForm, can_delete=True, extra=floor_queryset_distinct.count())
    formset = formset_factory(prefix='floors')
    for form, floor in zip(formset.forms, floor_queryset_distinct):
        form.fields['name'].initial = floor.name
        form.fields['sections'].queryset = section_queryset
        form.fields['sections'].initial = floor_queryset.filter(name=floor.name)\
            .annotate(sections=F('section__pk')).values_list('sections', flat=True).distinct()
        # sections that contain this floor are selected.
    return formset
