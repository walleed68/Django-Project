
from django.db import models
from Admin.models import course,student,classes
# Create your models here.


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    lecture_topic = models.CharField(max_length=100)
    lecture_date = models.CharField(max_length=100)
    class_name = models.ForeignKey(classes,on_delete=models.CASCADE)
    course_name = models.ForeignKey(course,on_delete=models.CASCADE)
    student_name = models.ForeignKey(student,on_delete=models.CASCADE)
    attendaces = models.CharField(max_length=2)
    def __str__(self):
        return self.lecture_topic


class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    file = models.FileField()
    end_date = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    submission = models.CharField(max_length=50)
    class_name = models.ForeignKey(classes,on_delete=models.CASCADE)
    course_name = models.ForeignKey(course,on_delete=models.CASCADE)
    def __str__(self):
        return self.assignment_name
