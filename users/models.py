from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to="images/")
    is_suspended = models.BooleanField(default=False)
    role = models.CharField(choices=[('admin', 'Admin'), ('student', 'Student'), ('teacher', 'Teacher'), ('staff', 'Staff')], max_length=20)
    classes = models.ForeignKey('api.Classes', on_delete=models.CASCADE, related_name="students", null=True, blank=True)
    designation = models.CharField(max_length=100, default="", blank=True)
    teacher_classes = models.ManyToManyField('api.Classes', through='api.TeacherSubject', related_name="class_teachers", blank=True)

    def __str__(self):
        return self.username