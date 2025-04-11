from rest_framework import serializers
from .models import *

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
    section = serializers.SerializerMethodField()
    class Meta:
        model = Teacher
        fields = '__all__'

    def get_section(self, obj):
        return [sections.name for sections in obj.section.all()]

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    #     return obj.section.name
    class Meta:
        model = Staff
        fields = '__all__'
