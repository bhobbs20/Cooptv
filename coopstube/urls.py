from django.contrib import admin
# from django.contrib.auth import views as auth_views
from django.urls import path, include
from coops import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # path('admin/', admin.site.urls), 

] 
