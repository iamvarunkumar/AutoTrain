from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path("",views.index, name='home'),
    path("login/", views.login, name='login'),
    path("documentation/", views.documentation, name='documentation'),
    path("dashboard/", views.dashboard, name='dashboard'),
]
