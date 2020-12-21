from django.urls import path

from . import views

urlpatterns = [

    path('', views.student1, name='student_page'),
    path('student', views.student1, name='student_page1'),
    path('forgot_password', views.forgotpassword, name='student_forget_password_page'),
    path('login', views.login1, name='student_login_page'),
    path('dologin', views.dologin, name='student_do_login_page'),
    path('logout', views.logout_user, name='student_logout_page'),
    path('profile', views.profile, name='student_profile_page'),
    path('assigned_courses', views.assignedcourses, name='student_assigned_courses_page'),
    path('assignment', views.assignment, name='student_assignment_page'),
    path('pending_assignment', views.pendingassignment, name='student_pending_assignment_page'),
    path('marks/<int:id>', views.marks, name='student_marks_page'),
    path('attendance/<str:name>/<str:name2>', views.attendance1, name='student_attendance_page')

    ]