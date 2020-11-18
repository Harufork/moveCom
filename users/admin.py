from django.contrib import admin
from .models import Profile, Employee, EmployeeRole, Notification

admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Employee)
admin.site.register(EmployeeRole)
