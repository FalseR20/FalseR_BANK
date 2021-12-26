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
    re_path(r'cards/(?P<number>\d+)/send_to_account/$', views.send_to_account),
    re_path(r'cards/(?P<number>\d+)/send_to_card/$', views.send_to_card),
    re_path(r'cards/(?P<number>\d+)/info/$', views.card_info),
    re_path(r'cards/(?P<number>\d+)/(?P<template_id>\d+)/$', views.template_operation),
    re_path(r'cards/(?P<number>\d+)/transactions/(?P<transaction_id>\d+)/$', views.transaction_info),

    path('admin/', admin.site.urls),
]
