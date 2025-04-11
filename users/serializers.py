from rest_framework import serializers
from .models import *
from api.serializers import TeachingSubjectSerializer
from api.models import TeacherSubject

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'date_of_birth', 'date_joined', 'address', 'phone', 'image')

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    section = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'

    def get_section(self, obj):
        return obj.section.name

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'attendance', 'designation', 'subjects']

    def get_subjects(self, obj):
        subjects = TeacherSubject.objects.filter(teacher=obj)
        return TeachingSubjectSerializer(subjects, many=True).data

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Staff
        fields = '__all__'
