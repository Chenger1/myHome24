from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings

from website.views.pages import MainPageView, AboutPageView, ServicesPageView, ContactsPageView


app_name = 'website'


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page_view'),
    path('about/', AboutPageView.as_view(), name='about_page_view'),
    path('services', ServicesPageView.as_view(), name='services_page_view'),
    path('contacts/', ContactsPageView.as_view(), name='contacts_page_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
