from django.urls import path

from user_profile.views import user_views
from user_profile.views import master_views
from user_profile.views import message_views
from user_profile.views import tariff_views


app_name = 'user_profile'


urlpatterns = [
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
]
