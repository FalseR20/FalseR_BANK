from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as authviews

from mainapp import views

urlpatterns = [
    path('', views.index),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('register/', views.register),
    # path('create/', views.create),
    # path('delete/', views.delete),

    path('admin/', admin.site.urls),
]
