from rest_framework import serializers
from api.models import *

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class AcademicTermSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.SerializerMethodField()
    class Meta:
        model = AcademicTerm
        fields = ['id', 'name', 'current','academic_year', 'academic_year_name']

    def get_academic_year_name(self, obj):
        return obj.academic_year.name

class ClassSerializer(serializers.ModelSerializer):
    total_students = serializers.IntegerField(read_only=True)
    incharge_name = serializers.CharField(source='incharge.username', read_only=True)
    class Meta:
        model = Classes
        fields = ['id', 'name', 'section', 'incharge', 'incharge_name', 'total_students']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectMarks
        fields = ['id', 'subject', 'total_marks', 'obtained_marks']

class ResultSerializer(serializers.ModelSerializer):
    subject_marks = SubjectMarksSerializer(source='subject_marks_result', many=True)
    class Meta:
        model = Result
        fields = ['id', 'student', 'academic_year', 'academic_term', 'classes', 'subject_marks', 'total_marks', 'obtained_marks', 'is_passed', 'rank']
        read_only_fields = ['academic_year', 'academic_term', 'classes', 'total_marks', 'obtained_marks']

    def create(self, validated_data):
        subject_marks_data = validated_data.pop('subject_marks')
        student = validated_data.get('student')
        if student:
            validated_data['classes'] = student.classes
        validated_data['academic_year'] = AcademicYear.objects.filter(current=True).first()
        validated_data['academic_term'] = AcademicTerm.objects.filter(current=True).first()

        result = Result.objects.create(**validated_data)

        for mark_data in subject_marks_data:
            SubjectMarks.objects.create(result=result, **mark_data)

        result.total_marks = sum(marks['total_marks'] for marks in subject_marks_data)
        result.obtained_marks = sum(marks['obtained_marks'] for marks in subject_marks_data)
        result.save()

        return result

    def update(self, instance, validated_data):
        subject_marks_data = validated_data.pop('subject_marks', [])

        instance.student = validated_data.get('student', instance.student)
        instance.classes = instance.student.classes
        instance.academic_year = AcademicYear.objects.filter(current=True).first()
        instance.academic_term = AcademicTerm.objects.filter(current=True).first()
        instance.save()

        if subject_marks_data:
            instance.subject_marks.all().delete()
            for marks in subject_marks_data:
                SubjectMarks.objects.create(result=instance, **marks)

        instance.total_marks = sum(marks['total_marks'] for marks in subject_marks_data)
        instance.obtained_marks = sum(marks['obtained_marks'] for marks in subject_marks_data)
        instance.save()

        return instance


class TeachingSubjectSerializer(serializers.ModelSerializer):
    classes = serializers.CharField(source='classes.name')
    subject = serializers.CharField(source='subject.name')

    class Meta:
        model = TeacherSubject
        fields = ['classes', 'subject']