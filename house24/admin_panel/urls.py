from django.urls import path

from admin_panel.views.index_views import IndexView, LogoutAdmin
from admin_panel.views.pages.page_views import (MainPageView, AboutPageView, DeleteAboutPageGallery,
                                                DeleteAdditionalGallery, DeleteDocument, ServicesPageView,
                                                ServicesDeleteBlockView, TariffPageView, TariffDeleteBlockView,
                                                ContactsPageView)
from admin_panel.views.options.option_views import (ServiceOptionView, SaveServiceForm, SaveMeasureForm,
                                                    DeleteServiceBlock, DeleteMeasureBlock, CredentialsView,
                                                    PaymentItemsListView, CreatePaymentItemView, UpdatePaymentItemView,
                                                    DeletePaymentItemView)
from admin_panel.views.options.tariff_option_views import (ListTariff, CreateTariff, GetServiceMeasure, DeleteTariff,
                                                           UpdateTariff, DeleteTariffService, DuplicateTariff)
from admin_panel.views.user.user_views import (UpdateRolesView, ListUsersView, CreateAdminUser, UpdateAdminUser,
                                               DeleteAdminUser, DetailAdminUser, ListOwnerView, CreateOwnerUser,
                                               UpdateOwnerUser,
                                               DeleteOwnerUser, DetailOwnerView)
from admin_panel.views.house_views import (ListHousesView, CreateHouseView, UpdateHouseView, GetUserRole,
                                           DeleteHouseInstance, DeleteSection, DeleteFloor, DeleteHouseUser,
                                           DetailHouseView)
from admin_panel.views.flat_views import (ListFlatsView, CreateFlatView, UpdateFlatView, GetHouseSectionAndFloor,
                                          DeleteFlatView, DetailFlatView)
from admin_panel.views import accounts
from admin_panel.views.mixins import FlatOwner
from admin_panel.views import meter_views


app_name = 'admin_panel'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout/', LogoutAdmin.as_view(), name='logout_admin'),
    path('flat_owner/', FlatOwner.as_view(), name='get_flat_owner'),

    # PAGES
    path('main_page/index', MainPageView.as_view(), name='main_page'),
    path('about/index', AboutPageView.as_view(), name='about_page'),
    path('about/delete_gallery_image/', DeleteAboutPageGallery.as_view(), name='delete_about_gallery_image'),
    path('about/delete_additional_gallery_image/', DeleteAdditionalGallery.as_view(),
         name='delete_about_additional_gallery_image'),
    path('about/delete_document/', DeleteDocument.as_view(), name='delete_document'),
    path('services/index', ServicesPageView.as_view(), name='services_page'),
    path('services/delete_block/', ServicesDeleteBlockView.as_view(), name='delete_services_block'),
    path('tariffs/index', TariffPageView.as_view(), name='tariff_page'),
    path('tariffs/delete_block/', TariffDeleteBlockView.as_view(), name='delete_tariff_block'),
    path('contacts/index', ContactsPageView.as_view(), name='contacts_page'),

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
    path('tariff/index/delete_service/', DeleteTariffService.as_view(), name='delete_tariff_service'),
    path('tariff/index/duplicate/<int:pk>/', DuplicateTariff.as_view(), name='duplicate_tariff'),

    # # USERS
    path('roles/index/', UpdateRolesView.as_view(), name='list_roles_admin'),
    path('user-admin/index/', ListUsersView.as_view(), name='list_users_admin'),
    path('user-admin/index/create_user_admin/', CreateAdminUser.as_view(), name='create_user_admin'),
    path('user-admin/index/update_user_admin/<int:pk>/', UpdateAdminUser.as_view(), name='update_user_admin'),
    path('user-admin/index/delete_user_admin/<int:pk>/', DeleteAdminUser.as_view(), name='delete_user_admin'),
    path('user-admin/index/detail_user_admin/<int:pk>/', DetailAdminUser.as_view(), name='detail_user_admin'),

    # # CREDENTIALS
    path('credentials/index/', CredentialsView.as_view(), name='credentials_admin'),

    # # PAYMENT ITEMS
    path('payment_items/index/', PaymentItemsListView.as_view(), name='payment_items_admin'),
    path('payment_items/index/create_item/', CreatePaymentItemView.as_view(), name='create_payment_item_admin'),
    path('payment_items/index/update_item/<int:pk>/', UpdatePaymentItemView.as_view(), name='update_payment_item_admin'),
    path('payment_items/index/delete_item/<int:pk>/', DeletePaymentItemView.as_view(), name='delete_payment_item_admin'),

    # OWNERS
    path('owners/index/', ListOwnerView.as_view(), name='list_owners_admin'),
    path('owners/index/create_owner/', CreateOwnerUser.as_view(), name='create_owner_admin'),
    path('owners/index/update_owner/<int:pk>/', UpdateOwnerUser.as_view(), name='update_owner_admin'),
    path('owners/index/delete_owner/<int:pk>/', DeleteOwnerUser.as_view(), name='delete_owner_admin'),
    path('owners/index/detail_owner/<int:pk>/', DetailOwnerView.as_view(), name='detail_owner_admin'),

    # HOUSES
    path('houses/index/', ListHousesView.as_view(), name='list_houses_admin'),
    path('houses/index/create_house/', CreateHouseView.as_view(), name='create_house_admin'),
    path('houses/index/update_house/<int:pk>/', UpdateHouseView.as_view(), name='update_house_admin'),
    path('houses/index/get_user_role/', GetUserRole.as_view(), name='get_user_role'),
    path('houses/index/delete_house/<int:pk>/', DeleteHouseInstance.as_view(), name='delete_house_admin'),
    path('houses/index/delete_section/', DeleteSection.as_view(), name='delete_section_admin'),
    path('houses/index/delete_floor/', DeleteFloor.as_view(), name='delete_floor_admin'),
    path('houses/index/delete_house_user/', DeleteHouseUser.as_view(), name='delete_house_user_admin'),
    path('houses/index/detail_house/<int:pk>/', DetailHouseView.as_view(), name='detail_house_admin'),

    # FLATS
    path('flats/index/', ListFlatsView.as_view(), name='list_flats_admin'),
    path('flats/index/create_flat/', CreateFlatView.as_view(), name='create_flat_admin'),
    path('flats/index/update_flat/<int:pk>/', UpdateFlatView.as_view(), name='update_flat_admin'),
    path('flats/index/delete_flat/<int:pk>/', DeleteFlatView.as_view(), name='delete_flat_admin'),
    path('flats/index/get_house_section_floor/', GetHouseSectionAndFloor.as_view(), name='get_house_section_and_floor'),
    path('flats/index/detail_flat/<int:pk>/', DetailFlatView.as_view(), name='detail_flat_admin'),

    # ACCOUNTS
    path('accounts/index/', accounts.ListPersonalAccountsView.as_view(), name='list_accounts_admin'),
    path('accounts/index/create_account/', accounts.CreatePersonalAccountView.as_view(), name='create_account_admin'),
    path('accounts/index/delete_account/<int:pk>/', accounts.DeleteAccountView.as_view(), name='delete_account_admin'),
    path('accounts/index/update_account/<int:pk>/', accounts.UpdatePersonalAccountView.as_view(),
         name='update_account_admin'),
    path('accounts/index/detail_account/<int:pk>/', accounts.PersonalAccountDetailView.as_view(),
         name='detail_account_admin'),

    # METERS
    path('meters/index/', meter_views.ListMetersView.as_view(), name='list_meters_admin'),
    path('meters/index/create_meter/', meter_views.CreateMeterView.as_view(), name='create_meter_admin'),
    path('meters/index/update_meter/<int:pk>/', meter_views.UpdateMeterView.as_view(), name='update_meter_admin'),
    path('meters/index/list_history/<int:pk>/', meter_views.ListMeterHistory.as_view(), name='list_meter_history'),
]
