from django.urls import path

from admin_panel.views.index_views import IndexView, LogoutAdmin
from admin_panel.views.pages.page_views import (MainPageView, AboutPageView, DeleteAboutPageGallery,
                                                DeleteAdditionalGallery, DeleteDocument)


app_name = 'admin_panel'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout/', LogoutAdmin.as_view(), name='logout_admin'),

    # PAGES
    path('main_page/', MainPageView.as_view(), name='main_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('about/delete_gallery_image/<int:pk>/', DeleteAboutPageGallery.as_view(), name='delete_about_gallery_image'),
    path('about/delete_additional_gallery_image/<int:pk>/', DeleteAdditionalGallery.as_view(),
         name='delete_about_additional_gallery_image'),
    path('about/delete_document/<int:pk>/', DeleteDocument.as_view(), name='delete_document'),
]
