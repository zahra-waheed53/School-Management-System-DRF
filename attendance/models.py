from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class SchoolTiming(models.Model):
    name = models.CharField(max_length=100, default="Default School Timing")
    arrival_time = models.TimeField(default='08:00:00', help_text="Expected arrival time")
    late_threshold = models.TimeField(default='08:30:00', help_text="After this time, attendance is marked as late")
    dismissal_time = models.TimeField(default='15:00:00', help_text="School dismissal time")
    is_active = models.BooleanField(default=True, help_text="Only one timing can be active at a time")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_timings'
    )

    class Meta:
        ordering = ['-is_active', '-created_at']
        verbose_name = 'School Timing'
        verbose_name_plural = 'School Timings'

    def __str__(self):
        return f"{self.name} - {'Active' if self.is_active else 'Inactive'}"

    def clean(self):
        if self.arrival_time and self.late_threshold:
            if self.late_threshold <= self.arrival_time:
                raise ValidationError({
                    'late_threshold': "Late threshold must be after arrival time"
                })
        
        if self.late_threshold and self.dismissal_time:
            if self.dismissal_time <= self.late_threshold:
                raise ValidationError({
                    'dismissal_time': "Dismissal time must be after late threshold"
                })
        
        if not self.is_active and self.pk:
            active_count = SchoolTiming.objects.filter(is_active=True).exclude(pk=self.pk).count()
            if active_count == 0:
                raise ValidationError({
                    'is_active': "Cannot deactivate. At least one timing must be active. "
                                "Activate another timing first."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        
        if self.is_active:
            SchoolTiming.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        
        super().save(*args, **kwargs)

    @classmethod
    def get_active_timing(cls):
        timing = cls.objects.filter(is_active=True).first()
        if not timing:
            timing = cls.objects.create(
                name="Default School Timing",
                is_active=True
            )
        return timing


class FaceEncoding(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='face_encoding')
    encoding = models.BinaryField()
    face_image = models.ImageField(upload_to='faces/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Face encoding for {self.user.username}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'Leave'),
        ('short_leave', 'Short Leave'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-marked_at']
        unique_together = ('user', 'marked_at')

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.marked_at.date()}"

