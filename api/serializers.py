from rest_framework import serializers
from .models import *

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class AcademicTermSerializer(serializers.ModelSerializer):
    academic_year = serializers.SerializerMethodField()
    class Meta:
        model = AcademicTerm
        fields = ['id', 'name', 'current','academic_year']

    def get_academic_year(self, obj):
        return obj.academic_year.name

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    student_class = serializers.SerializerMethodField()
    incharge_teacher = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'name', 'student_class', 'incharge_teacher', 'total_students']

    def get_student_class(self, obj):
        return obj.student_class.name

    def get_incharge_teacher(self, obj):
        return obj.incharge.user.username

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class TeachingSubjectSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = TeacherSubject
        fields = ['section', 'subject']

    def get_section(self, obj):
        return obj.section.name

    def get_subject(self, obj):
        return obj.subject.name