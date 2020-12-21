from . import views
from django.urls import path

urlpatterns = [

    path('', views.adminpage, name='main_admin_page'),
    path('admin',views.adminpage, name='main_admin_page2'),
    path('forgot_password',views.forgotpassword, name='forgot_password_page'),
    path('login',views.login1, name='login_page'),
    path('profile',views.profile, name='profile_page'),
    path('teacher_courses',views.teachercourses, name='teacher_courses_page'),
    path('student_new_course',views.studentnewcourses, name='assign_student_subject_page'),
    path('send_credentials',views.sendcredentials, name='send_credential_page'),
    path('create_teacher',views.createteacher, name='create_teacher_page'),
    path('delete_teacher',views.deleteteacher, name='delete_teacher_page'),
    path('create_student',views.createstudent, name='create_student_page'),
    path('delete_student',views.deletestudent, name='delete_student_page'),
    path('create_course',views.createcourse, name='create_course_page'),
    path('delete_course',views.deletecourse, name='delete_course_page'),
    path('teacher_new_courses',views.teachernewcourse, name='assign_teacher_course_page'),
    path('create_classes',views.createclass, name='create_class_page'),
    path('delete_classes',views.deleteclass, name='delete_class_page'),
    path('reset_session',views.resetsession, name='reset_session_page'),
    path('dologin', views.dologin, name='do_login_page'),
    path('logout', views.logout_user, name='logout_page'),
    path('create_support_admin', views.createadmin, name='create_admin_page'),
    path('student_new_course/<int:id>',views.studentnewcoursename, name='name_student_new_course_page'),
    path('teacher_new_course/<int:id>', views.teachernewcoursename, name='name_teacher_new_course_page'),

###*************###
### delete paths###
###*************###

    path('delete_course/<int:id>',views.delete_course, name='id_delete_course_page'),
    path('delete_student/<int:id>',views.delete_student, name='id_delete_student_page'),
    path('delete_teacher/<int:id>',views.delete_teacher, name='id_delete_teacher_page'),
    path('delete_teacher_courses/<int:id>',views.delete_teachercourses, name='id_delete_teacher_courses_page'),
    path('delete_classes/<int:id>',views.delete_classes, name='id_delete_class_page'),
    path('delete_student_courses/<int:id>',views.delete_studentcourses, name='id_delete_student_courses_page'),









]