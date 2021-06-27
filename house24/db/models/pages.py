from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse


from db.models.mixin import SingletonModel
from db.models.receiver import *


class MainPage(SingletonModel):
    slide1 = models.ImageField(upload_to='main_page/')
    slide2 = models.ImageField(upload_to='main_page/')
    slide3 = models.ImageField(upload_to='main_page/')
    title = models.CharField(max_length=150,  blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show_link = models.BooleanField(default=1)
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('admin_panel:main_page')

    def get_files(self):
        return [self.slide1, self.slide2, self.slide3]


class InfoBlock(models.Model):
    entity = models.ForeignKey(MainPage, related_name='blocks', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='main_page/block/',  blank=True, null=True)
    title = models.CharField(max_length=150,  blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_files(self):
        return [self.image] if self.image else None


class AboutPage(SingletonModel):
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='about/', blank=True, null=True)
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)
    additional_title = models.CharField(max_length=50, blank=True, null=True)
    additional_description = models.TextField(blank=True, null=True)

    def get_files(self):
        return [self.photo] if self.photo else None

    def get_absolute_url(self):
        return reverse('admin_panel:about_page')


class AboutGallery(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/gallery/')

    def get_files(self):
        return [self.image] if self.image else None

    def get_delete_url(self):
        return reverse('admin_panel:delete_about_gallery_image', args=[self.pk])


class AdditionalGallery(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='add_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/additional/')

    def get_files(self):
        return [self.image] if self.image else None

    def get_delete_url(self):
        return reverse('admin_panel:delete_about_additional_gallery_image', args=[self.pk])


class Document(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    file = models.FileField(upload_to='about/documents/')

    def get_files(self):
        return [self.file] if self.file else None

    def get_delete_url(self):
        return reverse('admin_panel:delete_document', args=[self.pk])


class Credentials(SingletonModel):
    name = models.CharField(max_length=150)
    information = models.TextField()

    def get_absolute_url(self):
        return reverse('admin_panel:credentials_admin')


class ContactsPage(SingletonModel):
    phone_validation = RegexValidator(regex=r'^\+\d{8,15}$', message='Неправильный формат номера.')

    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, validators=[phone_validation], blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    link = models.CharField(max_length=100, blank=True, null=True)
    map = models.TextField(blank=True, null=True)
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('admin_panel:contacts_page')


class ServicesPage(SingletonModel):
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('admin_panel:services_page')


class ServiceBlock(models.Model):
    entity = models.ForeignKey(ServicesPage, related_name='blocks', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services_page/', blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_files(self):
        return [self.image] if self.image else None
