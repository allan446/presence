from django.urls import path
from . import views

urlpatterns =[
    path('/', views.login, name='login'),
    #path('permissions/', views.permissions, name='permissions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit_permission/', views.submit_permission, name='submit_permission'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('permissions-service/', views.permissions_service, name='permissions_service'),
    path('login/', views.logIn, name='login'),  # Changed path from '' to 'login/'
    path('approve_permission/<int:permission_id>/', views.approve_permission, name='approve_permission'),
    path('approve_permission_chef/<int:permission_id>/', views.approve_permission_chef, name='approve_permission_chef'),
    path('reject_permission/<int:permission_id>/', views.reject_permission, name='reject_permission'),
    path('reject_permission_chef/<int:permission_id>/', views.reject_permission_chef, name='reject_permission_chef'),
    path('permission_history/', views.permission_history, name='permission_history'),
    path('edit_permission/edit/<int:permission_id>/', views.edit_permission, name='edit_permission'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('services/', views.service_list, name='service_list'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('delete_permission/<int:permission_id>/', views.delete_permission, name='delete_permission'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('change-password/', views.change_password, name='change_password'),
    path('service_calendar/<int:service_id>/', views.service_calendar, name='service_calendar'),
    path('api/service-calendar/', views.service_calendar, name='service_calendar'),
    #path('service_calendar/<int:service_id>/', views.service_calendar, name='service_calendar')
    path('profile/', views.profile, name='profile'),
    #path('login/', views.logout, name='logout'),
]