from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class customuser(AbstractUser):
    user_type_data = ((1,"mainadmin"),(2,"teacher"),(3,"student"))
    user_type = models.CharField(default=1,choices=user_type_data,max_length=10)


class mainadmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(customuser, on_delete=models.CASCADE)
    admin_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    image = models.FileField(default="logo.png")
    objects = models.Manager()
    def __str__(self):
        return self.admin_name



class teacher (models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(customuser, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    image = models.FileField(default="logo.png")
    father_name = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    objects = models.Manager()
    def __str__(self):
        return self.teacher_name


class student (models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(customuser, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    image = models.FileField(default="logo.png")
    previous_education = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    objects = models.Manager()
    def __str__(self):
        return self.student_name


class classes (models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    objects = models.Manager()
    def __str__(self):
        return self.class_name



class course (models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    course_ID = models.CharField(max_length=20)
    credit_hours = models.IntegerField()
    objects = models.Manager()
    def __str__(self):
        return self.course_name


class teachercourse (models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=20)
    teacher_name = models.ForeignKey(teacher,on_delete=models.CASCADE)
    course_name = models.ForeignKey(course,on_delete=models.CASCADE)
    objects = models.Manager()
    def __str__(self):
        return self.class_name



class studentcourses(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=20)
    student_name = models.ForeignKey(student,on_delete=models.CASCADE)
    student_roll_number = models.CharField(max_length=100)
    course_name = models.ForeignKey(course,on_delete=models.CASCADE)
    objects = models.Manager()
    def __str__(self):
        return self.class_name



@receiver(post_save,sender=customuser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            mainadmin.objects.create(admin=instance)
        if instance.user_type==2:
            teacher.objects.create(admin=instance)
        if instance.user_type==3:
            student.objects.create(admin=instance)
@receiver(post_save,sender=customuser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.mainadmin.save()
    if instance.user_type==2:
        instance.teacher.save()
    if instance.user_type==3:
        instance.student.save()