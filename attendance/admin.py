from django.contrib import admin
from .models import FaceEncoding, Attendance, SchoolTiming


@admin.register(SchoolTiming)
class SchoolTimingAdmin(admin.ModelAdmin):
    list_display = ['name', 'arrival_time', 'late_threshold', 'dismissal_time', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    fieldsets = (
        ('Timing Information', {
            'fields': ('name', 'is_active')
        }),
        ('School Hours', {
            'fields': ('arrival_time', 'late_threshold', 'dismissal_time')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FaceEncoding)
class FaceEncodingAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'marked_at']
    list_filter = ['status', 'marked_at']
    search_fields = ['user__username']
    readonly_fields = ['marked_at']
