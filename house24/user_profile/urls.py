from django.urls import path

from user_profile.views import user_views
from user_profile.views import master_views


app_name = 'user_profile'


urlpatterns = [
    # PROFILE
    path('view/<int:pk>/', user_views.UserProfileView.as_view(), name='user_profile'),
    path('view/edit/<int:pk>/', user_views.UpdateClientView.as_view(), name='edit_user_client'),
    path('logout/', user_views.LogoutClient.as_view(), name='logout_client'),

    #MASTER REQUESTS
    path('master_request/client/<int:pk>/', master_views.ListClientMasterRequestView.as_view(),
         name='list_master_requests_client'),
    path('master_request/client/create_request/<int:pk>/', master_views.CreateClientMasterRequestView.as_view(),
         name='create_master_request_client'),
]
