from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings

from user_profile.views import user_views
from user_profile.views import master_views
from user_profile.views import message_views
from user_profile.views import tariff_views
from user_profile.views import payment_ticket_views
from user_profile.views import index
from user_profile.views import chat_views

from common.render_pdf import RenderPdfTemplate


app_name = 'user_profile'


urlpatterns = [
    path('cabinet/flat/<int:pk>/', index.IndexView.as_view(), name='client_statistic'),
    path('cabinet/flat/statistic/', index.GetStatistic.as_view(), name='get_statistic'),

    # PROFILE
    path('view/<int:pk>/', user_views.UserProfileView.as_view(), name='user_profile'),
    path('view/edit/<int:pk>/', user_views.UpdateClientView.as_view(), name='edit_user_client'),
    path('logout/', user_views.LogoutClient.as_view(), name='logout_client'),

    # MASTER REQUESTS
    path('master_request/client/<int:pk>/', master_views.ListClientMasterRequestView.as_view(),
         name='list_master_requests_client'),
    path('master_request/client/create_request/<int:pk>/', master_views.CreateClientMasterRequestView.as_view(),
         name='create_master_request_client'),
    path('master_request/client/delete_request/<int:pk>/', master_views.DeleteMasterRequest.as_view(),
         name='delete_master_request_client'),

    # MESSAGE
    path('message/client/<int:pk>/', message_views.ListClientMessagesView.as_view(),
         name='list_client_messages_view'),
    path('message/client/delete_messages/', message_views.ExcludeUserFromReceivingMessage.as_view(),
         name='delete_messages_client'),
    path('message/client/detail_message/<int:pk>/', message_views.ClientMessageDetailView.as_view(),
         name='client_detail_message'),
    path('message/client/delete_message/<int:pk>/', message_views.ExcludeMessage.as_view(),
         name='delete_message_client'),

    # TARIFFS
    path('tariffs/client/<int:pk>/', tariff_views.ListTariffView.as_view(), name='list_tariffs_client'),

    # PAYMENT TICKETS
    path('payment_tickets/client/by_flat/<int:pk>/', payment_ticket_views.ListPaymentTicketsByFlatView.as_view(),
         name='list_payment_tickets_client_by_flat'),
    path('payment_tickets/client/all/<int:pk>/', payment_ticket_views.ListPaymentTicketsView.as_view(),
         name='list_payment_tickets_client'),
    path('payment_tickets/client/ticket/<int:pk>/', payment_ticket_views.PaymentTicketDetailClintView.as_view(),
         name='payment_ticket_detail_client'),
    path('payment_tickets/client/ticket/download/', RenderPdfTemplate.as_view(),
         name='render_pdf_template_client'),
    path('payment_tickets/client/ticket/<int:pk>/print/', payment_ticket_views.PrintPaymentTicketView.as_view(),
         name='payment_ticket_print'),
    path('payment_tickets/client/ticket/<int:pk>/payment/',
         payment_ticket_views.CreateTransactionByTicket.as_view(), name='create_client_transaction_by_ticket'),

    # CHAT
    path('chats/', chat_views.ListChatView.as_view(), name='user_chat_list'),
    path('chats/<int:to_user>/', chat_views.ChatView.as_view(), name='user_chat_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
