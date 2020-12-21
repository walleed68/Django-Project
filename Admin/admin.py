from django.contrib import admin
from .models import teacher,course,student,teachercourse,classes,studentcourses,mainadmin,customuser

# Register your models here.
admin.site.register(teacher)
admin.site.register(course)
admin.site.register(student)
admin.site.register(teachercourse)
admin.site.register(classes)
admin.site.register(studentcourses)
admin.site.register(mainadmin)
admin.site.register(customuser)