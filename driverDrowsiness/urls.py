"""driverDrowsiness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from gui.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registration_view, name = 'register'),
    path('login/', login_view, name = 'login'),
    path('webcam/', webcam_feed, name = 'webcam feed'),
    path('home/', webcam_home, name = 'home'),
    path('logout/', logout_view, name = 'logout'),
    path('acc_settings/', acc_settings_view, name = 'acc_settings'),
    path('setting', setting_view, name="settings")
]
