from rest_framework.viewsets import ModelViewSet
from .models import Student, Teacher, Staff
from .serializers import *

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    serializer_class = TeacherSerializer

class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.select_related('user').all()
    serializer_class = StaffSerializer