from . import views
from django.urls import path

urlpatterns = [

    path('', views.teacherpage, name='teacher_page'),
    path('teacher', views.teacherpage, name='teacher_page1'),
    path('forgot_password', views.forgotpassword, name='teacher_forget_password_page'),
    path('login', views.login1, name = 'teacher_login_page'),
    path('dologin', views.dologin, name='teacher_do_login_page'),
    path('logout', views.logout_user, name='teacher_logout_page'),
    path('profile', views.profile, name='teacher_profile_page'),
    path('assigned_courses', views.assignedcourses, name='teacher_assigned_courses_page'),
    path('attendance', views.attendance, name='teacher_attendance_page'),
    path('mark_attendance',views.mark_attendances, name='teacher_mark_attendance_page'),
    path('assignmentclose/<int:id>', views.closeassignment, name='teacher_assignment_close_page'),
    path('marks/<int:id>', views.marks, name='teacher_marks_page'),
    path('assignment/<str:name>/<str:name2>', views.assignment, name='teacher_assignment_page'),
    path('attendence/<str:name>/<str:name2>', views.classattandance, name='teacher_attendance_page2'),


###*************###
### delete paths###
###*************###

path('delete_assignment/<int:id>',views.delete_assignment, name='teacher_id_delete_assignment_page'),


    ]