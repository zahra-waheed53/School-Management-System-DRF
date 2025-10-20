from django.contrib import admin
from .models import *
from api.models import TeacherSubject

class TeacherSubjectInline(admin.TabularInline):
    model = TeacherSubject
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'date_of_birth', 'address', 'phone', 'classes']
    list_filter = ['role']
    inlines = [TeacherSubjectInline]
    
    def get_inlines(self, request, obj):
        # Only show TeacherSubjectInline for teachers
        if obj and obj.role == 'teacher':
            return [TeacherSubjectInline]
        return []