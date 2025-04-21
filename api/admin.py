from django.contrib import admin
from api.models import *

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'current']

@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'current']

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'student_count']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'student_class', 'incharge', 'student_count']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SubjectMarkInline(admin.TabularInline):
    model = SubjectMarks
    extra = 1

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    inlines = [SubjectMarkInline]
    list_display = ['student', 'academic_year', 'academic_term', 'section']
    readonly_fields = ['academic_year', 'academic_term', 'section', 'student_class', 'total_marks', 'obtained_marks']

    def save_model(self, request, obj, form, change):
        # Auto-fill fields before saving
        if obj.student:
            obj.section = obj.student.section
            obj.student_class = obj.student.section.student_class
        obj.academic_year = AcademicYear.objects.filter(current=True).first()
        obj.academic_term = AcademicTerm.objects.filter(current=True).first()
        obj.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        subject_marks = obj.subject_marks_result.all()
        obj.total_marks = sum(m.total_marks for m in subject_marks)
        obj.obtained_marks = sum(m.obtained_marks for m in subject_marks)
        obj.save()

@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'section']