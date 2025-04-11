from django.contrib import admin
from .models import *
from api.models import TeacherSubject, Section

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_of_birth', 'address', 'phone']

@admin.register(Student)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attendance', 'section']

class TeacherSubjectInline(admin.TabularInline):
    model = TeacherSubject
    extra = 1

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attendance']
    inlines = [TeacherSubjectInline]

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'designation']