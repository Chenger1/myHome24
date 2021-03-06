"""house24 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('rest_api/', include('rest_api.urls', namespace='rest_api')),
    path('', include('website.urls', namespace='website')),
    path('robots.txt', include('robots.urls')),
    path('user_profile/', include('user_profile.urls', namespace='user_profile')),
    path('ht/', include('health_check.urls')),
]
