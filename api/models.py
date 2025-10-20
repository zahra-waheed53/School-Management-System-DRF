from django.db import models
from django.conf import settings
from api.enums import ACADEMIC_TERM

class AcademicYear(models.Model):
    name = models.CharField(max_length=100, unique=True)
    current = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.current:
            AcademicYear.objects.exclude(pk=self.pk).update(current=False)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AcademicTerm(models.Model):
    name = models.CharField(max_length=100, choices=ACADEMIC_TERM)
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, related_name='academic_term', default=1)
    current = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.current:
            AcademicTerm.objects.exclude(pk=self.pk).update(current=False)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Classes(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    incharge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incharge_classes', limit_choices_to={'role': 'teacher'})

    def student_count(self):
        return self.students.count()

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
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='academic_year_results')
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name='academic_term_results')
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='class_results')
    subject = models.ManyToManyField(Subject,through='SubjectMarks', related_name='subject_results')
    total_marks = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    obtained_marks = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    is_passed = models.BooleanField(default=True)
    rank = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.student:
            self.classes = self.student.classes
        self.academic_year = AcademicYear.objects.filter(current=True).first()
        self.academic_term = AcademicTerm.objects.filter(current=True).first()

        return super().save(*args, **kwargs)


    def __str__(self):
        return self.student.username


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_subject', limit_choices_to={'role': 'teacher'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)