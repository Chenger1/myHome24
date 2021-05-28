from django.urls import path

from rest_api import views


app_name = 'rest_api'

urlpatterns = [
    path('section_list/', views.SectionList.as_view(), name='get_section_list'),
    path('floor_list/', views.FloorList.as_view(), name='get_floor_list'),
]
