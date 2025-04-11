from django.db import models
from users.models import Student, Teacher

class AcademicYear(models.Model):
    name = models.CharField(max_length=100)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name
ACADEMIC_TERM = (
    ("mid", 'Mid'),
    ("final", 'Final'),
)

class AcademicTerm(models.Model):
    name = models.CharField(max_length=100, choices=ACADEMIC_TERM)
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, related_name='academic_term', default=1)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StudentClass(models.Model):
    name = models.CharField(max_length=100)
    total_students = models.IntegerField()

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='student_sections')
    total_students = models.IntegerField()
    incharge = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_sections')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='academic_year_results')
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name='academic_term_results')
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='student_results')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_results')
    total_marks = models.DecimalField(max_digits=10, decimal_places=1)
    obtained_marks = models.DecimalField(max_digits=10, decimal_places=1)
    is_passed = models.BooleanField(default=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.student.user.username

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)