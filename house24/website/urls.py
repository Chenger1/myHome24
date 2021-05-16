from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings

from website.views.pages import MainPageView


app_name = 'website'


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
