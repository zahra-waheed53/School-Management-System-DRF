from django.db import models
from users.models import Student, Teacher
from .utils import ACADEMIC_TERM

class AcademicYear(models.Model):
    name = models.CharField(max_length=100)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AcademicTerm(models.Model):
    name = models.CharField(max_length=100, choices=ACADEMIC_TERM)
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, related_name='academic_term', default=1)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StudentClass(models.Model):
    name = models.CharField(max_length=100)

    def student_count(self):
        return sum(section.student.count() for section in self.student_sections.all())
    student_count.short_description = 'Total students'

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='student_sections')
    incharge = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_sections')

    def student_count(self):
        return self.student.count()
    student_count.short_description = 'Total students'

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubjectMarks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_marks')
    result = models.ForeignKey('Result', on_delete=models.CASCADE, related_name='subject_marks_result')
    total_marks = models.DecimalField(max_digits=10, decimal_places=2)
    obtained_marks = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.subject.name+'--'+str(self.total_marks)+'--'+str(self.obtained_marks)

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='academic_year_results')
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name='academic_term_results')
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='student_results')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_results')
    subject = models.ManyToManyField(Subject,through='SubjectMarks', related_name='subject_results')
    total_marks = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    obtained_marks = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    is_passed = models.BooleanField(default=True)
    rank = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.student:
            self.section = self.student.section
            self.student_class = self.student.section.student_class
        self.academic_year = AcademicYear.objects.filter(current=True).first()
        self.academic_term = AcademicTerm.objects.filter(current=True).first()

        return super().save(*args, **kwargs)


    def __str__(self):
        return self.student.user.username


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)