from django.urls import path 
from django.contrib import admin
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name="login"),
    path('layout/register/', views.register_user, name="register"),
    path('users/complaint/', views.report_complaint, name="complaint"),
    path('users/account-setting/', views.account_setting, name="account_setting"),
    path('users/complaint-history/', views.complaint_history, name="complaint_history"),
    path('users/dashboard/', views.dashboard, name="dashboard"),
    path('administrator/manage/', views.manage_users, name="manage_users"),
    path('logout/', views.logout_view, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)