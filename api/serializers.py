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
    total_students = serializers.SerializerMethodField()
    class Meta:
        model = StudentClass
        fields = ['id', 'name', 'total_students']

    def get_total_students(self, obj):
        return obj.student_count()


class SectionSerializer(serializers.ModelSerializer):
    student_class = serializers.SerializerMethodField()
    incharge_teacher = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'name', 'student_class', 'incharge_teacher', 'total_students']

    def get_student_class(self, obj):
        if hasattr(self, 'student_class'):
            return self.student_class
        self.student_class = obj.student_class.name
        return self.student_class

    def get_incharge_teacher(self, obj):
        if hasattr(self, 'incharge_teacher'):
            return self.incharge_teacher
        self.incharge_teacher = obj.incharge.user.username
        return self.incharge_teacher

    def get_total_students(self, obj):
        return obj.student_count()

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
        fields = ['id', 'student', 'academic_year', 'academic_term', 'student_class', 'section', 'subject_marks', 'total_marks', 'obtained_marks', 'is_passed', 'rank']
        read_only_fields = ['academic_year', 'academic_term', 'section', 'student_class', 'total_marks', 'obtained_marks']

    def create(self, validated_data):
        subject_marks_data = validated_data.pop('subject_marks')
        student = validated_data.get('student')
        if student:
            validated_data['section'] = student.section
            validated_data['student_class'] = student.student_class
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
        instance.section= instance.student.section
        instance.student_class = instance.section.student_class
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
    section = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = TeacherSubject
        fields = ['section', 'subject']

    def get_section(self, obj):
        if hasattr(self, 'section'):
            return self.section
        self.section = obj.section.name
        return self.section

    def get_subject(self, obj):
        if hasattr(self, 'subject'):
            return self.subject
        self.subject = obj.subject.name
        return self.subject