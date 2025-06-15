from django.urls import path 
from django.contrib import admin
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name="login"),
    path('layout/register/', views.register_user, name="register"),
    path('administrator/', views.admin_login, name="admin_login"),
    path('administrator/signup/', views.admin_signup, name="admin_signup"),
    path('administrator/logout/', views.admin_logout, name="admin_logout"),
    path('administrator/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('administrator/manage/', views.manage_users, name="manage_users"),
    path('administrator/edit-user/<int:user_id>/', views.edit_user, name="edit_user"),
    path('administrator/manage-complaints/', views.manage_complaints, name="manage_complaints"),
    path('administrator/view-complaint/<int:complaint_id>/', views.view_complaint, name='view_complaint'),
    path('administrator/update-complaint-status/<int:complaint_id>/', views.update_complaint_status, name='update_complaint_status'),
    path('users/complaint/', views.report_complaint, name="complaint"),
    path('users/account-setting/', views.account_setting, name="account_setting"),
    path('users/complaint-history/', views.complaint_history, name="complaint_history"),
    path('users/dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('administrator/generate-admin-report/', views.generate_admin_report, name='generate_admin_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)