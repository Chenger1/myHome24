from django.urls import path

from user_profile.views import user_views


app_name = 'user_profile'


urlpatterns = [
    path('view/<int:pk>/', user_views.UserProfileView.as_view(), name='user_profile'),
    path('view/edit/<int:pk>/', user_views.UpdateClientView.as_view(), name='edit_user_client'),
    path('logout/', user_views.LogoutClient.as_view(), name='logout_client')
]
