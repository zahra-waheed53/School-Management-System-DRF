from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from api.serializers import TeachingSubjectSerializer, ClassSerializer
from api.models import TeacherSubject

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'date_of_birth', 'date_joined', 'address', 'phone', 'image', 'role', 'classes', 'designation']

class StudentSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'date_joined', 'address', 'phone', 'image', 'classes', 'role']

class TeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'date_joined', 'address', 'phone', 'image', 'designation', 'subjects', 'role']

    def get_subjects(self, obj):
        subjects = obj.teacher_subject.all()
        return TeachingSubjectSerializer(subjects, many=True).data