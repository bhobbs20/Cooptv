from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from coops import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('dashboard', views.dashboard, name='dashboard'), 
    #Auth
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    #Coops
    path('coop/create', views.CreateCoop.as_view(), name='create_coop'),
    path('coop/<int:pk>', views.DetailCoop.as_view(), name='detail_coop'),
    path('coop/<int:pk>/update', views.UpdateCoop.as_view(), name='update_coop'),
    path('coop/<int:pk>/delete', views.DeleteCoop.as_view(), name='delete_coop'),
    #Videos
    path('coop/<int:pk>/addvideo', views.add_video, name='add_video'),
    # path('video/search', views.video_search, name='video_search'),
    # path('video/<int:pk>/delete', views.DeleteVideo.as_view(), name='delete_video'),
] 
