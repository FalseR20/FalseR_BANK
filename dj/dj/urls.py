from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from mainapp import views

urlpatterns = [
    path('sign_in/', auth_views.LoginView.as_view()),
    path('sign_up/', views.sign_up),
    path('sign_out/', views.sign_out),
    path('cards/', views.cards),
    path('', views.index),

    path('admin/', admin.site.urls),
]
