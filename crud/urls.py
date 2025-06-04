from django.urls import path 
from django.contrib import admin
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name="login"),
    path('layout/login/', views.login_view, name="login"),
    path('include/sidebar/', views.sidebar_view, name="sidebar"),
    path('users/add/', views.add_user, name="add_user"),
    path('users/complaint/', views.report_complaint, name="complaint"),
    path('admin/manage/', views.manage_users, name="manage_users"),
]