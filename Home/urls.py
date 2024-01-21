from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home/", views.index, name='home'),
    path("login/", views.login_page, name='login_page'),
    path("documentation/", views.documentation, name='documentation'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("upload/", views.upload_file, name='upload_file'),
    path("dataframe_summary/", views.dataframe_summary, name='dataframe_summary'),
    path("save_to_db/", views.save_to_database, name="save_to_database"),
    path("enable_dashboard_items/", views.enable_dashboard_items, name="enable_dashboard_items"),
    path("dev/", views.dev, name='dev'),
    path("signup/", views.signup_page, name='signup_page'),
    path("welcome/", views.welcome, name='welcome'),

]
