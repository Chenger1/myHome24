from django import forms

from db.models.pages import (MainPage, InfoBlock, AboutPage, AboutGallery, AdditionalGallery, Document,
                             ServicesPage, ServiceBlock, ContactsPage)


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
                                            'accept': '.png, .jpeg, .jpg'}),
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'block_description', 'class': 'form-control',
                                                 'style': 'resize:none;', 'maxlength': '500'}),
        }


MainPageFormSet = forms.inlineformset_factory(MainPage, InfoBlock,
                                              form=InfoBlockForm, max_num=6, extra=6,
                                              can_delete=False)


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = '__all__'
        widgets = {
            'photo': forms.FileInput(attrs={'id': 'photo', 'class': 'upload',
                                            'accept': '.png, .jpeg, .jpg'}),
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'description'}),
            'seo_title': forms.TextInput(attrs={'id': 'seo_title', 'class': 'form-control'}),
            'seo_description': forms.Textarea(attrs={'id': 'seo_description', 'class': 'form-control'}),
            'seo_keywords': forms.TextInput(attrs={'id': 'seo_keywords', 'class': 'form-control'}),
            'additional_title': forms.TextInput(attrs={'id': 'additional_title', 'class': 'form-control'}),
            'additional_description': forms.Textarea(attrs={'id': 'additional_description'}),
        }


class AboutPageGalleryForm(forms.ModelForm):
    class Meta:
        model = AboutGallery
        fields = ('image', )
        widgets = {
            'image': forms.FileInput(attrs={'class': 'upload',
                                            'accept': '.png, .jpeg, .jpg'}),
        }


class AboutPageAdditionalGalleryForm(forms.ModelForm):
    class Meta:
        model = AdditionalGallery
        fields = ('image', )
        widgets = {
            'image': forms.FileInput(attrs={'class': 'upload',
                                            'accept': '.png, .jpeg, .jpg'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'file')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'style': 'display:block;'})
        }


AboutPageGalleryInlineFormset = forms.inlineformset_factory(AboutPage, AboutGallery,
                                                            form=AboutPageGalleryForm, extra=0,
                                                            can_delete=True)

AboutPageAdditionalGalleryInlineFormset = forms.inlineformset_factory(AboutPage, AdditionalGallery,
                                                                      form=AboutPageAdditionalGalleryForm, extra=0,
                                                                      can_delete=True)

DocumentsFormset = forms.inlineformset_factory(AboutPage, Document,
                                               form=DocumentForm, extra=0, can_delete=True)


class ServicesForm(forms.ModelForm):
    class Meta:
        model = ServicesPage
        fields = '__all__'
        widgets = {
            'seo_title': forms.TextInput(attrs={'id': 'seo_title', 'class': 'form-control'}),
            'seo_description': forms.Textarea(attrs={'id': 'seo_description', 'class': 'form-control'}),
            'seo_keywords': forms.TextInput(attrs={'id': 'seo_keywords', 'class': 'form-control'}),
        }


class ServicesBlockForm(forms.ModelForm):
    class Meta:
        model = ServiceBlock
        exclude = ('entity', )
        widgets = {
            'image': forms.FileInput(attrs={'id': 'image', 'class': 'upload',
                                            'accept': '.png, .jpeg, .jpg'}),
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'block_description', 'class': 'form-control block_desc',
                                                 'style': 'resize:none;', 'maxlength': '1000'}),
        }


ServicesBlockFormset = forms.inlineformset_factory(ServicesPage, ServiceBlock,
                                                   form=ServicesBlockForm, extra=0, can_delete=True)


class ContactsPageForm(forms.ModelForm):
    class Meta:
        model = ContactsPage
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'description'}),
            'full_name': forms.TextInput(attrs={'id': 'full_name', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'id': 'location', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control'}),
            'link': forms.URLInput(attrs={'id': 'link', 'class': 'form-control'}),
            'map': forms.Textarea(attrs={'id': 'map', 'class': 'form-control'}),
            'seo_title': forms.TextInput(attrs={'id': 'seo_title', 'class': 'form-control'}),
            'seo_description': forms.Textarea(attrs={'id': 'seo_description', 'class': 'form-control'}),
            'seo_keywords': forms.TextInput(attrs={'id': 'seo_keywords', 'class': 'form-control'}),
        }
