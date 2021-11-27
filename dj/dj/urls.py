from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from mainapp import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view()),
    path('logup/', views.log_up),
    path('register/', views.log_up),
    path('logout/', views.log_out),
    path('', views.index, name="home"),

    path('admin/', admin.site.urls),
]
