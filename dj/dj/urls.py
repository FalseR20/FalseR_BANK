from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path

import mainapp.views

urlpatterns = [
    # Mainapp
    path('', mainapp.views.index),
    path('sign_in/', auth_views.LoginView.as_view()),
    path('sign_up/', mainapp.views.sign_up),
    path('sign_out/', mainapp.views.sign_out),
    path('cards/new/', mainapp.views.new_card),
    re_path(r'cards/(?P<number>\d+)/$', mainapp.views.card_page),
    re_path(r'cards/(?P<number>\d+)/send_to_account/$', mainapp.views.send_to_account),
    re_path(r'cards/(?P<number>\d+)/send_to_card/$', mainapp.views.send_to_card),
    re_path(r'cards/(?P<number>\d+)/info/$', mainapp.views.card_info),
    re_path(r'cards/(?P<number>\d+)/(?P<template_id>\d+)/$', mainapp.views.template_operation),
    re_path(r'cards/(?P<number>\d+)/transactions/(?P<transaction_id>\d+)/$', mainapp.views.transaction_info),
    # Mainapp api
    path('api/cards/', mainapp.views.react_get_cards),

    # Frontend with react
    path("react/", include("frontend.urls")),

    # Admin
    path('admin/', admin.site.urls),
]
