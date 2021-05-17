from django import forms

from db.models.pages import MainPage, InfoBlock


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = '__all__'
        widgets = {
            'slide1': forms.FileInput(attrs={'id': 'slide1', 'class': 'upload',
                                             'accept': '.png, .jpeg, .jpg, .svg'}),
            'slide2': forms.FileInput(attrs={'id': 'slide2', 'class': 'upload',
                                             'accept': '.png, .jpeg, .jpg, .svg'}),
            'slide3': forms.FileInput(attrs={'id': 'slide3', 'class': 'upload',
                                             'accept': '.png, .jpeg, .jpg, .svg'}),
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'description'}),
            'show_link': forms.CheckboxInput(attrs={'id': 'show_link', 'class': 'form-check-input',
                                                    'type': 'checkbox'}),
            'seo_title': forms.TextInput(attrs={'id': 'seo_title', 'class': 'form-control'}),
            'seo_description': forms.Textarea(attrs={'id': 'seo_description', 'class': 'form-control'}),
            'seo_keywords': forms.TextInput(attrs={'id': 'seo_keywords', 'class': 'form-control'})
        }


class InfoBlockForm(forms.ModelForm):
    class Meta:
        model = InfoBlock
        exclude = ('entity', )
        widgets = {
            'image': forms.FileInput(attrs={'id': 'image', 'class': 'upload',
                                            'accept': '.png, .jpeg, .jpg, .svg'}),
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'description', 'class': 'form-control',
                                                 'style': 'resize:none;'}),
        }


mainPageFormSet = forms.inlineformset_factory(MainPage, InfoBlock,
                                              form=InfoBlockForm, extra=6,
                                              can_delete=False)
