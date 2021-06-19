from django.urls import path

from admin_panel.views.index_views import IndexView, LogoutAdmin
from admin_panel.views.pages import page_views
from admin_panel.views.options import option_views
from admin_panel.views.options import tariff_option_views
from admin_panel.views.user import user_views
from admin_panel.views import house_views
from admin_panel.views import flat_views
from admin_panel.views import accounts
from admin_panel.views.mixins import FlatOwner
from admin_panel.views import meter_views
from admin_panel.views import master_request_views
from admin_panel.views import payment_ticket_views
from admin_panel.views import account_transaction_views
from admin_panel.views import message_views

from common.render_pdf import RenderPdfTemplate


app_name = 'admin_panel'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout/', LogoutAdmin.as_view(), name='logout_admin'),
    path('flat_owner/', FlatOwner.as_view(), name='get_flat_owner'),

    # PAGES
    path('main_page/index/', page_views.MainPageView.as_view(), name='main_page'),
    path('about/index/', page_views.AboutPageView.as_view(), name='about_page'),
    path('services/index/', page_views.ServicesPageView.as_view(), name='services_page'),
    path('contacts/index/', page_views.ContactsPageView.as_view(), name='contacts_page'),

    # OPTIONS
    path('service/index/', option_views.ServiceOptionView.as_view(), name='service_measure_option'),
    path('services/index/save_service/', option_views.SaveServiceForm.as_view(), name='save_service_form'),
    path('services/index/save_measure/', option_views.SaveMeasureForm.as_view(), name='save_measure_form'),

    # # TARIFF
    path('tariff/index/', tariff_option_views.ListTariff.as_view(), name='list_tariff_admin'),
    path('tariff/index/create/', tariff_option_views.CreateTariff.as_view(), name='create_tariff'),
    path('tariff/index/get_service_measure/', tariff_option_views.GetServiceMeasure.as_view(),
         name='get_service_measure'),
    path('tariff/index/delete/<int:pk>/', tariff_option_views.DeleteTariff.as_view(), name='delete_tariff'),
    path('tariff/index/update/<int:pk>/', tariff_option_views.UpdateTariff.as_view(), name='update_tariff'),
    path('tariff/index/duplicate/<int:pk>/', tariff_option_views.DuplicateTariff.as_view(), name='duplicate_tariff'),
    path('tariff/index/detail_tariff/<int:pk>/', tariff_option_views.DetailTariffView.as_view(),
         name='detail_tariff_admin'),

    # # USERS
    path('roles/index/', user_views.UpdateRolesView.as_view(), name='list_roles_admin'),
    path('user-admin/index/', user_views.ListUsersView.as_view(), name='list_users_admin'),
    path('user-admin/index/create_user_admin/', user_views.CreateAdminUser.as_view(), name='create_user_admin'),
    path('user-admin/index/update_user_admin/<int:pk>/', user_views.UpdateAdminUser.as_view(), name='update_user_admin'),
    path('user-admin/index/delete_user_admin/<int:pk>/', user_views.DeleteAdminUser.as_view(), name='delete_user_admin'),
    path('user-admin/index/detail_user_admin/<int:pk>/', user_views.DetailAdminUser.as_view(), name='detail_user_admin'),

    # # CREDENTIALS
    path('credentials/index/', option_views.CredentialsView.as_view(), name='credentials_admin'),

    # # PAYMENT ITEMS
    path('payment_items/index/', option_views.PaymentItemsListView.as_view(), name='payment_items_admin'),
    path('payment_items/index/create_item/', option_views.CreatePaymentItemView.as_view(),
         name='create_payment_item_admin'),
    path('payment_items/index/update_item/<int:pk>/', option_views.UpdatePaymentItemView.as_view(),
         name='update_payment_item_admin'),
    path('payment_items/index/delete_item/<int:pk>/', option_views.DeletePaymentItemView.as_view(),
         name='delete_payment_item_admin'),

    # OWNERS
    path('owners/index/', user_views.ListOwnerView.as_view(), name='list_owners_admin'),
    path('owners/index/create_owner/', user_views.CreateOwnerUser.as_view(), name='create_owner_admin'),
    path('owners/index/update_owner/<int:pk>/', user_views.UpdateOwnerUser.as_view(), name='update_owner_admin'),
    path('owners/index/delete_owner/<int:pk>/', user_views.DeleteOwnerUser.as_view(), name='delete_owner_admin'),
    path('owners/index/detail_owner/<int:pk>/', user_views.DetailOwnerView.as_view(), name='detail_owner_admin'),
    path('owners/index/name_ascending/', user_views.ListOwnerLastNameAscendingView.as_view(),
         name='list_owners_name_ascending_admin'),
    path('owners/index/name_descending/', user_views.ListOwnerLastNameDescendingView.as_view(),
         name='list_owners_name_descending_admin'),
    path('owners/index/date_ascending/', user_views.ListOwnerDateJoinedAscendingView.as_view(),
         name='list_owners_date_joined_ascending'),
    path('owners/index/date_descending/', user_views.ListOwnerDateJoinedDescendingView.as_view(),
         name='list_owners_date_joined_descending_admin'),

    # HOUSES
    path('houses/index/', house_views.ListHousesView.as_view(), name='list_houses_admin'),
    path('houses/index/create_house/', house_views.CreateHouseView.as_view(), name='create_house_admin'),
    path('houses/index/update_house/<int:pk>/', house_views.UpdateHouseView.as_view(), name='update_house_admin'),
    path('houses/index/get_user_role/', house_views.GetUserRole.as_view(), name='get_user_role'),
    path('houses/index/delete_house/<int:pk>/', house_views.DeleteHouseInstance.as_view(), name='delete_house_admin'),
    path('houses/index/detail_house/<int:pk>/', house_views.DetailHouseView.as_view(), name='detail_house_admin'),
    path('houses/index/name_ascending/', house_views.ListHouseNameAscendingView.as_view(),
         name='list_houses_name_ascending_admin'),
    path('houses/index/name_descending/', house_views.ListHouseNameDescendingView.as_view(),
         name='list_houses_name_descending_admin'),
    path('houses/index/address_ascending/', house_views.ListHouseAddressAscendingView.as_view(),
         name='list_houses_address_ascending_admin'),
    path('houses/index/address_descending/', house_views.ListHouseAddressDescendingView.as_view(),
         name='list_houses_address_descending_admin'),

    # FLATS
    path('flats/index/', flat_views.ListFlatsView.as_view(), name='list_flats_admin'),
    path('flats/index/create_flat/', flat_views.CreateFlatView.as_view(), name='create_flat_admin'),
    path('flats/index/update_flat/<int:pk>/', flat_views.UpdateFlatView.as_view(), name='update_flat_admin'),
    path('flats/index/delete_flat/<int:pk>/', flat_views.DeleteFlatView.as_view(), name='delete_flat_admin'),
    path('flats/index/get_house_section_floor/', flat_views.GetHouseSectionAndFloor.as_view(),
         name='get_house_section_and_floor'),
    path('flats/index/detail_flat/<int:pk>/', flat_views.DetailFlatView.as_view(), name='detail_flat_admin'),
    path('flats/index/number_ascending/', flat_views.ListFlatsViewNumberAscendingView.as_view(),
         name='list_flats_number_ascending_admin'),
    path('flats/index/number_descending/', flat_views.ListFlatsViewNumberDescendingView.as_view(),
         name='list_flats_number_descending_admin'),
    path('flats/index/house_ascending/', flat_views.ListFlatsViewHouseAscendingView.as_view(),
         name='list_flats_house_ascending_admin'),
    path('flats/index/house_descending/', flat_views.ListFlatsViewHouseDescendingView.as_view(),
         name='list_flats_house_descending_admin'),
    path('flats/index/section_ascending/', flat_views.ListFlatsViewSectionAscendingView.as_view(),
         name='list_flats_section_ascending_admin'),
    path('flats/index/section_descending/', flat_views.ListFlatsViewSectionDescendingView.as_view(),
         name='list_flats_section_descending_admin'),
    path('flats/index/floor_ascending/', flat_views.ListFlatsViewFloorAscendingView.as_view(),
         name='list_flats_floor_ascending_admin'),
    path('flats/index/floor_descending/', flat_views.ListFlatsViewFloorDescendingView.as_view(),
         name='list_flats_floor_descending_admin'),
    path('flats/index/owner_ascending/', flat_views.ListFlatsViewOwnerAscendingView.as_view(),
         name='list_flats_owner_ascending_admin'),
    path('flats/index/owner_descending/', flat_views.ListFlatsViewOwnerDescendingView.as_view(),
         name='list_flats_owner_descending_admin'),

    # ACCOUNTS
    path('accounts/index/', accounts.ListPersonalAccountsView.as_view(), name='list_accounts_admin'),
    path('accounts/index/create_account/', accounts.CreatePersonalAccountView.as_view(), name='create_account_admin'),
    path('accounts/index/delete_account/<int:pk>/', accounts.DeleteAccountView.as_view(), name='delete_account_admin'),
    path('accounts/index/update_account/<int:pk>/', accounts.UpdatePersonalAccountView.as_view(),
         name='update_account_admin'),
    path('accounts/index/detail_account/<int:pk>/', accounts.PersonalAccountDetailView.as_view(),
         name='detail_account_admin'),
    path('accounts/index/download_spreadsheet/', accounts.DownloadSpreadSheet.as_view(),
         name='download_spreadsheet_account'),

    # METERS
    path('meters/index/', meter_views.ListMetersView.as_view(), name='list_meters_admin'),
    path('meters/index/create_meter/', meter_views.CreateMeterView.as_view(), name='create_meter_admin'),
    path('meters/index/update_meter/<int:pk>/', meter_views.UpdateMeterView.as_view(), name='update_meter_admin'),
    path('meters/index/list_history/<int:pk>/', meter_views.ListMeterHistory.as_view(), name='list_meter_history'),
    path('meters/index/detail_meter/<int:pk>/', meter_views.MeterDetailView.as_view(), name='detail_meter_admin'),
    path('meters/index/delete_meter/<int:pk>/', meter_views.DeleteMeterView.as_view(), name='delete_meter_admin'),
    path('meters/index/duplicate_meter/<int:pk>/', meter_views.DuplicateMeterView.as_view(),
         name='duplicate_meter_admin'),
    path('meters/index/number_ascending/', meter_views.ListMetersNumberAscendingView.as_view(),
         name='list_meters_number_ascending_admin'),
    path('meters/index/number_descending/', meter_views.ListMetersNumberDescendingView.as_view(),
         name='list_meters_number_descending_admin'),
    path('meters/index/list_history/<int:pk>/date_ascending/', meter_views.ListMeterHistoryDateAscending.as_view(),
         name='list_meter_history_date_ascending'),
    path('meters/index/list_history/<int:pk>/date_descending/', meter_views.ListMeterHistoryDateDescending.as_view(),
         name='list_meter_history_date_descending'),
    path('meters/index/list_history/<int:pk>/month_ascending/', meter_views.ListMeterHistoryMonthAscending.as_view(),
         name='list_meter_history_month_ascending'),
    path('meters/index/list_history/<int:pk>/month_descending/', meter_views.ListMeterHistoryMonthDescending.as_view(),
         name='list_meter_history_month_descending'),
    path('meters/index/create_meter_by_flat/<int:pk>/', meter_views.CreateMeterView.as_view(),
         name='create_meter_by_flat_admin'),

    # MASTER REQUESTS
    path('master_request/index/', master_request_views.ListMasterRequestsView.as_view(),
         name='list_master_requests_admin'),
    path('master_request/index/create_request/', master_request_views.CreateMasterRequestView.as_view(),
         name='create_master_request_admin'),
    path('master_request/index/update_request/<int:pk>/', master_request_views.UpdateMasterRequestView.as_view(),
         name='update_master_request_admin'),
    path('master_request/index/delete_request/<int:pk>/', master_request_views.DeleteMasterRequest.as_view(),
         name='delete_master_request_admin'),
    path('master_request/index/detail_request/<int:pk>/', master_request_views.DetailMasterRequest.as_view(),
         name='detail_master_request_admin'),
    path('master_request/index/number_ascending/', master_request_views.ListMasterRequestsNumberAscendingView.as_view(),
         name='list_master_requests_number_ascending_admin'),
    path('master_request/index/number_descending/', master_request_views.ListMasterRequestsNumberDescendingView.as_view(),
         name='list_master_requests_number_descending_admin'),
    path('master_request/index/date_ascending/', master_request_views.ListMasterRequestsDateAscendingView.as_view(),
         name='list_master_requests_date_ascending_admin'),
    path('master_request/index/date_descending/', master_request_views.ListMasterRequestsDateDescendingView.as_view(),
         name='list_master_requests_date_descending_admin'),
    path('master_request/index/type_ascending/', master_request_views.ListMasterRequestsTypeAscendingView.as_view(),
         name='list_master_requests_type_ascending_admin'),
    path('master_request/index/type_descending/', master_request_views.ListMasterRequestsTypeDescendingView.as_view(),
         name='list_master_requests_type_descending_admin'),

    # PAYMENT TICKET
    path('payment_ticket/index/', payment_ticket_views.ListPaymentTicketsView.as_view(),
         name='list_payment_ticket_admin'),
    path('payment_ticket/index/create_ticket/', payment_ticket_views.CreatePaymentTicketView.as_view(),
         name='create_payment_ticket_admin'),
    path('payment_ticket/index/delete_ticket/<int:pk>/', payment_ticket_views.DeletePaymentTicketView.as_view(),
         name='delete_payment_ticket_admin'),
    path('payment_ticket/index/update_ticket/<int:pk>/', payment_ticket_views.UpdatePaymentTicketView.as_view(),
         name='update_payment_ticket_admin'),
    path('payment_ticket/index/bulk_delete_tickets', payment_ticket_views.BulkDeleteTicketService.as_view(),
         name='bulk_delete_payment_tickets'),
    path('payment_ticket/index/duplicate_ticket/<int:pk>/', payment_ticket_views.DuplicatePaymentTicket.as_view(),
         name='duplicate_payment_ticket'),
    path('payment_ticket/index/ticket/<int:pk>/', payment_ticket_views.DetailPaymentTicketView.as_view(),
         name='detail_payment_ticket_admin'),
    path('payment_ticket/index/account/<int:pk>/', payment_ticket_views.ListTicketsByAccount.as_view(),
         name='list_payment_tickets_by_account'),
    path('payment_ticket/index/account/create/<int:pk>/', payment_ticket_views.CreatePaymentTicketWithAccount.as_view(),
         name='create_ticket_with_account'),
    path('payment_ticket/index/account/create/<int:pk>/', payment_ticket_views.CreatePaymentTicketWithFlat.as_view(),
         name='create_ticket_with_flat'),
    path('payment_ticket/index/date_ascending/', payment_ticket_views.ListPaymentTicketDateAscendingView.as_view(),
         name='list_payment_ticket_date_ascending_admin'),
    path('payment_ticket/index/date_descending/', payment_ticket_views.ListPaymentTicketDateDescendingView.as_view(),
         name='list_payment_ticket_date_descending_admin'),
    path('payment_ticket/index/month_ascending/', payment_ticket_views.ListPaymentTicketMonthAscendingView.as_view(),
         name='list_payment_ticket_month_ascending_admin'),
    path('payment_ticket/index/month_descending/', payment_ticket_views.ListPaymentTicketMonthDescendingView.as_view(),
         name='list_payment_ticket_month_descending_admin'),

    # # HTML TEMPLATES
    path('payment_ticket/index/print/<int:pk>/', payment_ticket_views.ListTemplates.as_view(),
         name='list_payment_ticket_html_templates'),
    path('payment_ticket/index/print/template/', payment_ticket_views.TemplateSettings.as_view(),
         name='payment_ticket_template_settings'),
    path('payment_ticket/index/print/template/delete_template/<int:pk>/',
         payment_ticket_views.DeleteTemplateView.as_view(), name='payment_ticket_template_delete'),
    path('payment_ticket/index/print/template/set_default/<int:pk>/',
         payment_ticket_views.SetTemplateAsDefaultView.as_view(), name='payment_ticket_template_set_default'),
    path('payment_ticket/index/print/template/download_template/<int:pk>/',
         payment_ticket_views.DownloadTemplate.as_view(), name='payment_ticket_template_download'),
    path('payment_ticket/index/print/template/download_ticket/',
         RenderPdfTemplate.as_view(), name='payment_ticket_render_pdf'),

    # account-transaction
    path('account-transaction/index/', account_transaction_views.ListAccountTransactionView.as_view(),
         name='list_account_transaction_admin'),
    path('account-transaction/index/create_income/', account_transaction_views.CreateIncomeView.as_view(),
         name='create_income_admin'),
    path('account-transaction/index/create_outcome/', account_transaction_views.CreateOutcomeView.as_view(),
         name='create_outcome_admin'),
    path('account-transaction/index/update_income/<int:pk>/', account_transaction_views.UpdateIncomeView.as_view(),
         name='update_income_admin'),
    path('account-transaction/index/update_outcome/<int:pk>/', account_transaction_views.UpdateOutcomeView.as_view(),
         name='update_outcome_admin'),
    path('account-transaction/index/delete_transaction/<int:pk>/',
         account_transaction_views.DeleteTransactionView.as_view(), name='delete_transaction_admin'),
    path('account-transaction/index/transaction/<int:pk>/', account_transaction_views.DetailTransactionView.as_view(),
         name='detail_transaction_admin'),
    path('account-transaction/index/duplicate_income/<int:pk>/', account_transaction_views.DuplicateIncomeView.as_view(),
         name='duplicate_income_admin'),
    path('account-transaction/index/duplicate_outcome/<int:pk>/',
         account_transaction_views.DuplicateOutcomeView.as_view(),
         name='duplicate_outcome_admin'),
    path('account-transaction/index/account/<int:pk>/', account_transaction_views.ListIncomeTransactionByAccount.as_view(),
         name='list_transactions_by_account'),
    path('account-transaction/index/create_income/account/<int:pk>/',
         account_transaction_views.CreateIncomeByAccountView.as_view(),
         name='create_income_with_account'),
    path('account-transaction/index/create_income/flat/<int:pk>/',
         account_transaction_views.CreateIncomeByFlatView.as_view(),
         name='create_income_with_flat'),
    path('account-transaction/index/date_ascending/',
         account_transaction_views.ListAccountTransactionViewAscendingView.as_view(),
         name='list_account_transaction_ascending_admin'),
    path('account-transaction/index/date_descending/',
         account_transaction_views.ListAccountTransactionViewDescendingView.as_view(),
         name='list_account_transaction_descending_admin'),
    path('account-transaction/index/download_spreadsheet/', account_transaction_views.DownloadSpreadSheet.as_view(),
         name='download_spreadsheet_transactions'),
    path('account-transaction/index/download_spreadsheet/<int:pk>/',
         account_transaction_views.DownloadConcreteTransactionSpreadSheet.as_view(),
         name='download_spreadsheet_concrete_transactions'),

    # MESSAGE
    path('message/index/', message_views.ListMessages.as_view(), name='list_messages_admin'),
    path('message/index/create_message/', message_views.CreateMessageView.as_view(), name='create_message_admin'),
    path('message/index/create_message_with_debt/', message_views.CreateMessageWithDebtView.as_view(),
         name='create_message_with_debt_admin'),
    path('message/index/delete_messages/', message_views.DeleteMessagesView.as_view(), name='delete_messages_admin'),
    path('message/index/detail_message/<int:pk>/', message_views.DetailMessageView.as_view(),
         name='detail_message_admin'),
    path('message/index/delete_message/<int:pk>/', message_views.DeleteMessageView.as_view(),
         name='delete_message_admin'),
    path('message/index/invite_message/', message_views.CreateInviteMessageView.as_view(), name='create_invite_message')
]
