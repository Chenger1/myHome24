from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse_lazy


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
        return reverse_lazy('admin_panel:main_page')

    def get_images(self):
        return [self.slide1, self.slide2, self.slide3]


class InfoBlock(models.Model):
    entity = models.ForeignKey(MainPage, related_name='blocks', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='main_page/block/',  blank=True, null=True)
    title = models.CharField(max_length=100,  blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_images(self):
        return [self.image] if self.image else None


class AboutPage(SingletonModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='about/')
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)
    additional_title = models.CharField(max_length=100, blank=True, null=True)
    additional_description = models.TextField(blank=True, null=True)

    def get_images(self):
        return [self.photo] if self.photo else None


class AboutGallery(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/gallery/')

    def get_images(self):
        return [self.image] if self.image else None


class AdditionalGallery(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='add_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/additional/')

    def get_images(self):
        return [self.image] if self.image else None


class Document(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='about/documents/')


class Credentials(SingletonModel):
    name = models.CharField(max_length=150)
    information = models.TextField()


class ContactsPage(SingletonModel):
    phone_validation = RegexValidator(regex=r'^\+\d{8,15}$', message='Неправильный формат номера.')

    title = models.CharField(max_length=100)
    description = models.TextField()
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, validators=[phone_validation])
    email = models.EmailField(max_length=150)
    link = models.CharField(max_length=100)
    map = models.TextField()
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)


class ServicesPage(SingletonModel):
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)


class ServiceBlock(models.Model):
    entity = models.ForeignKey(ServicesPage, related_name='blocks', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services_page/')
    title = models.CharField(max_length=100)
    description = models.TextField()

    def get_images(self):
        return [self.image] if self.image else None


class TariffPage(SingletonModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)
