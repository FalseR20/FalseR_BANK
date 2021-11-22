from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from mainapp import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.log_out),

    path('admin/', admin.site.urls),
]
