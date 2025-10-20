from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Prefetch
from .models import User
from .serializers import *

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

class StudentViewSet(ModelViewSet):
    queryset = User.objects.filter(role='student').select_related('classes').all()
    serializer_class = StudentSerializer

class TeacherViewSet(ModelViewSet):
    queryset = User.objects.filter(role='teacher').prefetch_related(Prefetch('teacher_subject', queryset=TeacherSubject.objects.select_related('classes', 'subject')))
    serializer_class = TeacherSerializer