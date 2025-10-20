from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaceEncodingViewSet, AttendanceViewSet, SchoolTimingViewSet

router = DefaultRouter()
router.register(r'face', FaceEncodingViewSet, basename='face-encoding')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'timing', SchoolTimingViewSet, basename='school-timing')

urlpatterns = [
    path('', include(router.urls)),
]