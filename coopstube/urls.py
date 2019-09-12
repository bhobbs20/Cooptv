from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from coops import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls), 
    #Auth
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),

] 
