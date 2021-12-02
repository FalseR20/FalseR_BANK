from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from mainapp import views

urlpatterns = [
    path('log_in/', auth_views.LoginView.as_view()),
    path('log_up/', views.log_up),
    path('log_out/', views.log_out),
    path('cards/', views.cards),
    path('', views.index),

    path('admin/', admin.site.urls),
]
