from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.conf import settings

from website.views.pages import MainPageView, AboutPageView, ServicesPageView, ContactsPageView, DownloadDocument
from website.views.auth_views import ClientLoginView
from website.sitemaps import MainPageSitemap, AboutPageSitemap, ContactPageSitemap, ServicesPageSitemap


app_name = 'website'

sitemaps = {
    'main_page': MainPageSitemap,
    'about_page': AboutPageSitemap,
    'contact_page': ContactPageSitemap,
    'services_page': ServicesPageSitemap
}


urlpatterns = [

    #  PUBLIC PAGES
    path('', MainPageView.as_view(), name='main_page_view'),
    path('about/', AboutPageView.as_view(), name='about_page_view'),
    path('services', ServicesPageView.as_view(), name='services_page_view'),
    path('contacts/', ContactsPageView.as_view(), name='contacts_page_view'),
    path('site/login', ClientLoginView.as_view(), name='client_site_login_view'),
    path('download_document/<int:pk>/', DownloadDocument.as_view(), name='download_document'),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps}, name='get_sitemap'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
