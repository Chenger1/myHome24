from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings

from website.views.pages import MainPageView, AboutPageView, ServicesPageView, ContactsPageView, DownloadDocument
from website.views.auth_views import AdminLoginView, ClientLoginView


app_name = 'website'


urlpatterns = [

    #  PUBLIC PAGES
    path('', MainPageView.as_view(), name='main_page_view'),
    path('about/', AboutPageView.as_view(), name='about_page_view'),
    path('services', ServicesPageView.as_view(), name='services_page_view'),
    path('contacts/', ContactsPageView.as_view(), name='contacts_page_view'),
    path('site/login', ClientLoginView.as_view(), name='client_site_login_view'),
    path('site/admin_login/', AdminLoginView.as_view(), name='admin_site_login_view'),
    path('download_document/<int:pk>/', DownloadDocument.as_view(), name='download_document'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
