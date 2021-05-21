from django.urls import path

from admin_panel.views.index_views import IndexView, LogoutAdmin
from admin_panel.views.pages.page_views import (MainPageView, AboutPageView, DeleteAboutPageGallery,
                                                DeleteAdditionalGallery, DeleteDocument, ServicesPageView,
                                                ServicesDeleteBlockView, TariffPageView, TariffDeleteBlockView,
                                                ContactsPageView)
from admin_panel.views.options.option_views import (ServiceOptionView, SaveServiceForm, SaveMeasureForm,
                                                    DeleteServiceBlock, DeleteMeasureBlock)
from admin_panel.views.options.tariff_option_views import (ListTariff, CreateTariff, GetServiceMeasure, DeleteTariff,
                                                           UpdateTariff)


app_name = 'admin_panel'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout/', LogoutAdmin.as_view(), name='logout_admin'),

    # PAGES
    path('main_page/', MainPageView.as_view(), name='main_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('about/delete_gallery_image/', DeleteAboutPageGallery.as_view(), name='delete_about_gallery_image'),
    path('about/delete_additional_gallery_image/', DeleteAdditionalGallery.as_view(),
         name='delete_about_additional_gallery_image'),
    path('about/delete_document/', DeleteDocument.as_view(), name='delete_document'),
    path('services/', ServicesPageView.as_view(), name='services_page'),
    path('services/delete_block/', ServicesDeleteBlockView.as_view(), name='delete_services_block'),
    path('tariffs/', TariffPageView.as_view(), name='tariff_page'),
    path('tariffs/delete_block/', TariffDeleteBlockView.as_view(), name='delete_tariff_block'),
    path('contacts/', ContactsPageView.as_view(), name='contacts_page'),

    # OPTIONS
    path('service/index/', ServiceOptionView.as_view(), name='service_measure_option'),
    path('services/index/save_service/', SaveServiceForm.as_view(), name='save_service_form'),
    path('services/index/save_measure/', SaveMeasureForm.as_view(), name='save_measure_form'),
    path('services/index/delete_service/', DeleteServiceBlock.as_view(), name='delete_service_option'),
    path('services/index/delete_measure/', DeleteMeasureBlock.as_view(), name='delete_measure_option'),

    # # TARIFF
    path('tariff/index/', ListTariff.as_view(), name='list_tariff_admin'),
    path('tariff/index/create/', CreateTariff.as_view(), name='create_tariff'),
    path('tariff/index/get_service_measure/', GetServiceMeasure.as_view(), name='get_service_measure'),
    path('tariff/index/delete/<int:pk>/', DeleteTariff.as_view(), name='delete_tariff'),
    path('tariff/index/update/<int:pk>/', UpdateTariff.as_view(), name='update_tariff'),
]
