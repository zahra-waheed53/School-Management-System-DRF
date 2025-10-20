from rest_framework import viewsets
from django.db.models import Count
from api.serializers import *


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

class AcademicTermViewSet(viewsets.ModelViewSet):
    queryset = AcademicTerm.objects.prefetch_related('academic_year').all()
    serializer_class = AcademicTermSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeachingSubjectSerializer
    # def get_queryset(self):
    #     queryset = TeacherSubject.objects.prefetch_related('')