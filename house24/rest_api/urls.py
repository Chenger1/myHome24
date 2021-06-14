from django.urls import path

from rest_api import views


app_name = 'rest_api'

urlpatterns = [
    path('section_list/', views.SectionList.as_view(), name='get_section_list'),
    path('floor_list/', views.FloorList.as_view(), name='get_floor_list'),
    path('flat_list/', views.FlatList.as_view(), name='get_flat_list'),
    path('tariff_services/', views.GetTariffServices.as_view(), name='get_tariff_services'),
    path('create_meter_api/', views.CreateMeterApiView.as_view(), name='create_meter_api'),
    path('meters_list/', views.GetMeterDataApiView.as_view(), name='get_meters_list'),
    path('owner_flat_list/', views.OwnerFlatList.as_view(), name='owner_flat_list'),
    path('owner_account_list/', views.OwnerPersonalAccounts.as_view(), name='owner_account_list'),
    path('personal_account_tickets_list/', views.PersonalAccountPaymentTicketList.as_view(),
         name='personal_account_tickets_list'),
    path('total_balance/', views.TotalBalance.as_view(), name='get_total_balance'),
    path('personal_account_status/', views.PersonalAccountStatus.as_view(), name='get_account_status'),
    path('payment_ticket_sum/', views.PaymentTicketSum.as_view(), name='payment_ticket_sum')
]
