from django.contrib import admin
from .models import Service, Employee, Permission

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Service, ServiceAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'service')

admin.site.register(Employee, EmployeeAdmin)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'is_approved', 'date_send','bool')

admin.site.register(Permission, PermissionAdmin)
