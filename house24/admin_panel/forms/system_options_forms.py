from django import forms

from db.models.house import Service, Measure


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = '__all__'
        widgets = {
            'measure_name': forms.TextInput(attrs={'class': 'form-control'})
        }


MeasureFormset = forms.modelformset_factory(model=Measure, form=MeasureForm, can_delete=False, extra=1)


class ServiceForm(forms.ModelForm):
    measure = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=Measure.objects.all(), required=True)

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def save(self, commit=True):
        if not self.cleaned_data:
            return False
        super().save(commit=commit)


ServiceFormset = forms.modelformset_factory(model=Service, form=ServiceForm, can_delete=False, extra=1)
