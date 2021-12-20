from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from mainapp import views

urlpatterns = [
    path('', views.index),
    path('sign_in/', auth_views.LoginView.as_view()),
    path('sign_up/', views.sign_up),
    path('sign_out/', views.sign_out),
    path('cards/new/', views.new_card),
    re_path(r'cards/(?P<number>\d+)/$', views.card_page),
    re_path(r'cards/(?P<number>\d+)/(?P<template_id>\d+)/$', views.card_operation),

    path('admin/', admin.site.urls),
]
