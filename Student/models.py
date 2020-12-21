from django.db import models
from Admin.models import course,classes,student
from Teacher.models import Assignment

# Create your models here.


class Marks(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.ForeignKey(student,on_delete=models.CASCADE)
    student_roll_number = models.CharField(max_length=100)
    assignment_name = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    obtained_marks = models.CharField(max_length=100)
    file = models.FileField()
    submission = models.CharField(max_length=50)
    class_name = models.ForeignKey(classes,on_delete=models.CASCADE)
    course_name = models.ForeignKey(course,on_delete=models.CASCADE)
    def __str__(self):
        return self.student_roll_number