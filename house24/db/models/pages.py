from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse_lazy


from db.models.mixin import SingletonModel


class MainPage(SingletonModel):
    slide1 = models.ImageField(upload_to='main_page/', blank=True, null=True)
    slide2 = models.ImageField(upload_to='main_page/', blank=True, null=True)
    slide3 = models.ImageField(upload_to='main_page/', blank=True, null=True)
    title = models.CharField(max_length=150,  blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show_link = models.BooleanField(default=1)
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('admin_panel:main_page')


class InfoBlock(models.Model):
    entity = models.ForeignKey(MainPage, related_name='blocks', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='main_page/block/',  blank=True, null=True)
    title = models.CharField(max_length=100,  blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class AboutPage(SingletonModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='about/')
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)
    additional_title = models.CharField(max_length=100, blank=True, null=True)
    additional_description = models.TextField(blank=True, null=True)


class AboutGallery(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/gallery/')


class AdditionalGallery(models.Model):
    entity = models.ForeignKey(AboutPage, related_name='add_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/additional/')


class Document(models.Model):
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


class TariffPage(SingletonModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=150, blank=True, null=True)
