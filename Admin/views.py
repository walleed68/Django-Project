from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import teacher,course,student,teachercourse,classes,studentcourses,mainadmin,customuser
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from Teacher.models import Attendance,Assignment
from Student.models import Marks
from Admin.EmailBackEnd import EmailBackEnd


# Create your views here.





def adminpage(request):

    teachers = teacher.objects.all().count()
    students = student.objects.all().count()
    courses = course.objects.all().count()
    mainadmins = mainadmin.objects.all().count()
    args = { 'courses':courses,'students':students,'teachers':teachers , 'mainadmins':mainadmins}

    return render(request, 'index.html', args)



def login1(request):
    return render(request, 'login.html')

def dologin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:

        user = authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))



        if user != None:

            if user.is_active:
                if user.user_type == "1":
                    login(request, user)
                    return HttpResponseRedirect('admin')
                else:
                    messages.error(request, 'please enter correct credentials', extra_tags=" error")
                    return HttpResponseRedirect('/admin/login')
        else:
            messages.error(request, 'please enter correct credentials', extra_tags=" error")
            return HttpResponseRedirect('/admin/login')

    return HttpResponseRedirect('/admin/login')



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/admin/login')


def forgotpassword(request):
    try:
        if(request.POST):
            forgot = request.POST.get("forgotpass")
            admins = mainadmin.objects.get(email=forgot)
            # send an email
            send_mail(
                'Credentials of Student Portal',  # subject
                'Here is your password : ' + admins.passwd,  # message
                '',  # from email
                [admins.email]  # to email
            )
            messages.success(request, 'We have mailed your password', extra_tags=" success")


        return render(request, 'forgot-password.html')
    except mainadmin.DoesNotExist:
        messages.error(request, 'Email Does NoT Exist', extra_tags=" error")
        return render(request,'forgot-password.html')


def profile(request):


    user1 = request.user
    admins = get_object_or_404(mainadmin, email=user1.email)
    admins1 = get_object_or_404(customuser,username=user1.email)

    if(request.POST):
        admin_name = request.POST.get("changename")
        email = request.POST.get("changeemail")
        password = request.POST.get("changepassword")

        profile_pic = request.FILES.get('changeimage',False)

        if(admin_name != ""):
            admins1.name = admin_name
            admins.admin_name = admin_name
        if(email != ""):
            admins1.email = email
            admins1.username = email
            admins.email = email
        if(password != ""):
            admins1.set_password(password)
            admins.passwd = password
        if(profile_pic != False):
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            admins.image = profile_pic_url
        admins1.save()
        admins.save()

    args={'admins':admins}
    return render(request, 'profile.html',args)



def createadmin (request):
    admin = mainadmin.objects.all()

    if (request.POST):
        name = request.POST.get("adminname")
        email = request.POST.get("adminemail")
        password = request.POST.get("adminpassword")


        if (name != "" and  email != "" and password != "" ):

            for admin1 in admin:
                if (admin1.email == email):
                    messages.error(request, 'Duplicate Entries', extra_tags=" error")
                    break
            else:
                form_input = customuser.objects.create_user(username=email, email=email, password=password, user_type=1)
                form_input.mainadmin.admin_name = name
                form_input.mainadmin.passwd = password
                form_input.mainadmin.email = email
                form_input.save()
                messages.success(request, 'Support Admin Added Successfully', extra_tags= " success")

        else:
            messages.error(request, 'please fill-out all fields', extra_tags= " error")



    return render(request, 'table15.html')



def createteacher(request):
    teachers = teacher.objects.all()
    if(request.POST):

        teacher_name = request.POST.get("teachername")
        father_name = request.POST.get("teacherfathername")
        email = request.POST.get("teacheremail")
        education = request.POST.get("teachereducation")
        address = request.POST.get("teacheraddress")
        city = request.POST.get("teachercity")
        status = request.POST.get("teacherstatus")
        department = request.POST.get("teacherdepartment")
        password = request.POST.get("teacherpassword")

        if (teacher_name != "" and father_name != "" and email != "" and education != "" and address != "" and city != "" and status != "" and department != "" and password != "" ):
            for teacher1 in teachers:
                if(teacher1.email == email):
                    messages.error(request, 'Duplicate Entries', extra_tags=" error")
                    break
            else:
                form_input = customuser.objects.create_user(username=email, email=email, password=password, user_type=2)
                form_input.teacher.teacher_name = teacher_name
                form_input.teacher.email = email
                form_input.teacher.passwd = password
                form_input.teacher.father_name = father_name
                form_input.teacher.education = education
                form_input.teacher.status = status
                form_input.teacher.address = address
                form_input.teacher.city = city
                form_input.teacher.department = department
                form_input.save()
                messages.success(request, 'Teacher Added Successfully', extra_tags= " success")

        else:
            messages.error(request, 'please fill-out all fields', extra_tags= " error")

    return render(request, 'tables4.html')



def createstudent(request):
    students = student.objects.all()
    if(request.POST):
        student_name = request.POST.get("studentname")
        father_name = request.POST.get("studentfathername")
        email = request.POST.get("studentemail")
        previous_education = request.POST.get("studentpreviouseducation")
        roll_number = request.POST.get("studentrollno")
        address = request.POST.get("studentaddress")
        city = request.POST.get("studentcity")
        department = request.POST.get("studentdepartment")
        password = request.POST.get("studentpassword")

        if ( student_name != "" and father_name != "" and email != "" and previous_education != "" and roll_number != "" and address != "" and city != "" and department != "" and password != "" ):
            for student1 in students:
                if (student1.email == email or student1.roll_number == roll_number):
                    messages.error(request, 'Duplicate Entries', extra_tags=" error")
                    break
            else:
                form_input = customuser.objects.create_user(username=roll_number,  email=email, password=password, user_type=3)
                form_input.student.student_name=student_name
                form_input.student.email = email
                form_input.student.passwd= password
                form_input.student.father_name=father_name
                form_input.student.previous_education=previous_education
                form_input.student.roll_number=roll_number
                form_input.student.address=address
                form_input.student.city=city
                form_input.student.department=department

                form_input.save()
                messages.success(request, 'Student Added Successfully', extra_tags= " success")

        else:
            messages.error(request, 'please fill-out all fields', extra_tags= " error")


    return render(request, 'tables6.html')


def createcourse(request):
    course1 = course.objects.all()
    if(request.POST):
        course_name = request.POST.get("coursename")
        course_ID = request.POST.get("courseid")
        credit_hours = request.POST.get("credithours")

        if (course_name != "" and course_ID != "" and credit_hours != "" ):

            for course2 in course1:
                if(course2.course_ID == course_ID or course2.course_name ==course_name):
                    messages.error(request, 'Dublicate Entries', extra_tags=" error")
                    break
            else:
                form_input = course(course_name=course_name, course_ID=course_ID, credit_hours=credit_hours)
                form_input.save()
                messages.success(request, 'Course Added Successfully', extra_tags=" success")

        else:
            messages.error(request, 'please fill-out all fields' , extra_tags= " error")

    return render(request, 'tables8.html')


def createclass(request):
    class1 = classes.objects.all()
    if(request.POST):
        class_name = request.POST.get("classname")
        session = request.POST.get("selectsession")
        semester = request.POST.get("semester")

        if (class_name != "" and session != "" and semester != ""):
            for class2 in class1:
                if (class2.class_name == class_name):
                    messages.error(request, 'Duplicate Entries', extra_tags=" error")
                    break
            else:
                form_input = classes( class_name=class_name, semester=semester, session=session)
                form_input.save()
                messages.success(request, 'Class Added Successfully' , extra_tags= " success")

        else:
            messages.error(request, 'please fill-out all fields', extra_tags= " error")

    return render(request, 'tables12.html')



def sendcredentials(request):
    teachers = teacher.objects.all()
    args = {'teachers':teachers}
    if(request.POST):
        teacher_name = request.POST.get('selectteacher')
        teachers1 = get_object_or_404(teacher,teacher_name=teacher_name)
        messages.success(request, 'Credentials Send Successfully', extra_tags= " success")
        # send an email
        send_mail(
            'Credentials of Student Portal', # subject
            'Here is your username : ' + teachers1.email + ' and here is your password : ' + teachers1.passwd, # message
            '', # from email
            [ teachers1.email ] # to email
        )

    return render(request, 'tables3.html', args)




def teachercourses(request):
    teachercourses = teachercourse.objects.all()
    args = {'teachercourses': teachercourses}
    return render(request, 'tables.html', args)

def studentnewcourses(request):
    students = student.objects.all()
    students1 = student.objects.values('department').distinct()
    students2 = student.objects.all()

    if(request.POST):
        studentname = request.POST.get("studentsearch")
        departmentname = request.POST.get("selectdepartment")
        if (departmentname != "Select Department"):
            students = student.objects.filter(department = departmentname)
        if (studentname != ""):
            students = student.objects.filter(student_name = studentname)

    #pagination code

    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    args = {'posts':posts, 'students1':students1, 'students2':students2}
    return render(request, 'tables11.html',args)


def teachernewcourse(request):
    teachers = teacher.objects.all()
    teachers1 = teacher.objects.values('department').distinct()
    teachers2 = teacher.objects.all()

    if (request.POST):
        teacher_name = request.POST.get("teachersearch")
        departmentname = request.POST.get("selectdepartment")
        if (departmentname != "Select Department"):
            teachers = teacher.objects.filter(department=departmentname)
        if (teacher_name != ""):
            teachers = teacher.objects.filter(teacher_name=teacher_name)

    # pagination code

    paginator = Paginator(teachers, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    args = {'posts': posts, 'teachers1': teachers1, 'teachers2': teachers2}
    return render(request, 'tables14.html', args)


def studentnewcoursename(request,id):
    students = get_object_or_404(student,id=id)
    if (request.POST):
        studentcourse = studentcourses.objects.filter(student_name=students.id)
        class_name = request.POST.get("selectclass")
        course_name = request.POST.get("selectcourse")
        course1 = get_object_or_404(course, course_name=course_name)
        for studentcourse1 in studentcourse:
            if (studentcourse1.course_name == course1):
                messages.error(request, 'Duplicate Entries', extra_tags=" error")
                break
        else:
            form_input = studentcourses(class_name=class_name, course_name=course1, student_name=students,
                                        student_roll_number=students.roll_number)
            form_input.save()
            messages.success(request, 'Course Assigned Successfully', extra_tags=" success")

    courses = course.objects.all()
    class1 = classes.objects.all()
    studentcourse = studentcourses.objects.filter(student_name=students.id)
    args = {'students': students, 'class1': class1, 'courses': courses, 'studentcourse': studentcourse}

    return render(request, 'tables2.html', args)



def teachernewcoursename(request,id):
    teachers = get_object_or_404(teacher, id=id)

    if (request.POST):
        teachercourses = teachercourse.objects.filter(teacher_name=teachers.id)
        class_name = request.POST.get("selectclass")
        course_name = request.POST.get("selectcourse")
        course1 = get_object_or_404(course,course_name=course_name)

        for teachercourses1 in teachercourses:
            if (teachercourses1.course_name == course1 and teachercourses1.class_name == class_name):
                messages.error(request, 'Duplicate Entries', extra_tags=" error")
                break
        else:
            form_input = teachercourse(class_name=class_name, course_name=course1, teacher_name=teachers)
            form_input.save()
            messages.success(request, 'Course Assigned Successfully', extra_tags= " success")


    courses = course.objects.all()
    class1 = classes.objects.all()
    teachercourses = teachercourse.objects.filter(teacher_name=teachers.id)

    args = {'teachers': teachers, 'class1': class1, 'courses': courses, 'teachercourses': teachercourses}

    return render(request, 'tables10.html',args)


def resetsession(request):

    if (request.POST):
        session2 = request.POST.get('session1')
        if(session2 == "Session Reset"):
            teachercourses1 = teachercourse.objects.all()
            studentcourses1 = studentcourses.objects.all()
            assignment1 = Assignment.objects.all()
            attendance1 = Attendance.objects.all()
            marks1 = Marks.objects.all()
            teachercourses1.delete()
            studentcourses1.delete()
            assignment1.delete()
            attendance1.delete()
            marks1.delete()
            messages.success(request, 'Session Reset Successfully', extra_tags=" success")
        else:
            messages.error(request, 'Please Enter the correct Phrase', extra_tags=" error")


    return render(request,'tables16.html')



def deleteclass(request):
    class1 = classes.objects.all()
    args = {'class1': class1}
    return render(request, 'tables13.html',args)


def deleteteacher(request):
    teachers = teacher.objects.all()
    args = {'teachers': teachers}
    return render(request, 'tables5.html',args)


def deletestudent(request):
    students = student.objects.all()
    args = {'students': students}
    return render(request, 'tables7.html',args)


def deletecourse(request):
    courses = course.objects.all()
    args = {'courses':courses}
    return render(request, 'tables9.html',args)


###*************###
### delete views###
###*************###



def delete_course(request,id):

    courses = get_object_or_404(course,id=id)
    courses.delete()
    messages.error(request, 'Course deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_student(request,id):

    students = get_object_or_404(student,id=id)
    customusers = get_object_or_404(customuser,username=students.roll_number)
    customusers.delete()
    messages.error(request, 'Student deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_teacher(request,id):

    teachers = get_object_or_404(teacher,id=id)
    customusers = get_object_or_404(customuser,username=teachers.email)
    customusers.delete()
    messages.error(request, 'Teacher deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_teachercourses(request,id):
    teachercourses = get_object_or_404(teachercourse,id=id)
    teachercourses.delete()
    messages.error(request, 'Course deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_classes(request,id):
    class1 = get_object_or_404(classes,id=id)
    class1.delete()
    messages.error(request, 'Class deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_studentcourses(request,id):
    studentcourse = get_object_or_404(studentcourses,id=id)
    studentcourse.delete()
    messages.error(request, 'Course deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








