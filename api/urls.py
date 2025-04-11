from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('academic-years', AcademicYearViewSet)
router.register('academic-terms', AcademicTermViewSet)
router.register('classes', ClassViewSet)
router.register('sections', SectionViewSet)
router.register('subjects', SubjectViewSet)
router.register('results', ResultViewSet)
router.register('teacher-subjects', TeacherSubjectViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
