from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_of_birth', 'address', 'phone']

@admin.register(Student)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attendance', 'section']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attendance']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'designation']