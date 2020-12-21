from django.contrib.auth import authenticate, logout,login
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from Admin.models import teacher,customuser,teachercourse,studentcourses,course,student,classes
from .models import Attendance,Assignment
from datetime import date
from Student.models import Marks




# Create your views here.

def teacherpage(request):
    students = 0
    i = None
    user1 = request.user
    teachers = get_object_or_404(teacher, email=user1.email)
    teachercourses = teachercourse.objects.filter(teacher_name = teachers.id)
    teachers1 = teachercourses.count()
    for teachercourse1 in teachercourses:
        if (i != teachercourse1.teacher_name):
            students = students + studentcourses.objects.filter(class_name = teachercourse1.class_name).distinct().count()
        i = teachercourse1.teacher_name
    args = {'teachers1':teachers1, 'students':students}


    return render(request, 'indext.html', args)


def login1(request):
    return render(request, 'logint.html')


def dologin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:

        user = authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            if user.is_active:
                if user.user_type == "2":
                    login(request, user)
                    return HttpResponseRedirect('teacher')
                else:
                    messages.error(request, 'please enter correct credentials', extra_tags=" error")
                    return HttpResponseRedirect('/teacher/login')
        else:
            messages.error(request, 'please enter correct credentials', extra_tags=" error")
            return HttpResponseRedirect('/teacher/login')
    return HttpResponseRedirect('/teacher/login')




def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/teacher/login')



def forgotpassword(request):

    try:
        if (request.POST):
            forgot = request.POST.get("forgotpass")
            teachers = teacher.objects.get(email=forgot)
            # send an email
            send_mail(
                'Credentials of Student Portal',  # subject
                'Here is your password : ' + teachers.passwd,  # message
                '',  # from email
                [teachers.email]  # to email
            )
        messages.success(request, 'We have mailed your password', extra_tags=" success")
        return render(request, 'forgot-password.html')

    except teacher.DoesNotExist:
        messages.error(request, 'Email Does NoT Exist', extra_tags=" error")
        return render(request, 'forgot-password.html')

def profile(request):
    user1 = request.user
    teachers = get_object_or_404(teacher, email=user1.email)
    teachers1 = get_object_or_404(customuser, username=user1.username)

    if (request.POST):
        teacher_name = request.POST.get("changename")
        email = request.POST.get("changeemail")
        password = request.POST.get("changepassword")

        profile_pic = request.FILES.get('changeimage', False)

        if (teacher_name != ""):
            teachers1.name = teacher_name
            teachers.teacher_name = teacher_name
        if (email != ""):
            teachers1.email = email
            teachers1.username = email
            teachers.email = email
        if (password != ""):
            teachers1.set_password(password)
            teachers.passwd = password
        if (profile_pic != False):
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            teachers.image = profile_pic_url
        teachers1.save()
        teachers.save()

    args = {'teachers': teachers}
    return render(request, 'profilet.html', args)

def assignedcourses(request):

    user1 = request.user
    teachers = get_object_or_404(teacher, email=user1.email)
    teachercourses = teachercourse.objects.filter(teacher_name=teachers.id)

    args = {'teachercourses': teachercourses}


    return render(request, 'tables3t.html', args)

def attendance(request):
    user1 = request.user
    teachers = get_object_or_404(teacher, email=user1.email)
    teachercourses = teachercourse.objects.filter(teacher_name=teachers.id)
    args = {'teachercourses': teachercourses, }

    return render(request, 'tables4t.html', args)


def classattandance(request,name,name2):
    classname = name
    coursename = name2
    courses = get_object_or_404(course,course_name = coursename)
    studentcourses1 = studentcourses.objects.filter(class_name=classname,course_name = courses.id)
    args = {'studentcourses1':studentcourses1,'classname':classname,'coursename':coursename }
    return render(request, 'tables5t.html', args)


@csrf_exempt
def mark_attendances(request):
    user1 = request.user
    teachers = get_object_or_404(teacher, email=user1.email)
    teachercourses = teachercourse.objects.filter(teacher_name=teachers.id)
    args = {'teachercourses': teachercourses, }

    if (request.POST):
        presents = request.POST.getlist('selected[]')
        absents = request.POST.getlist('selected1[]')
        class_name = request.POST.get('classname')
        course_name = request.POST.get('coursename')
        topic = request.POST.get('topic')
        dates = date.today()
        for present in presents:
            students = get_object_or_404(student,roll_number = present)
            courses = get_object_or_404(course,course_name = course_name)
            classes1 = get_object_or_404(classes,class_name = class_name)
            form_input = Attendance(class_name=classes1, course_name=courses, student_name=students, attendaces = "P" , lecture_date=dates , lecture_topic =topic)
            form_input.save()
        for absent in absents:
            classes1 = get_object_or_404(classes, class_name=class_name)
            students1 = get_object_or_404(student,roll_number = absent)
            courses1 = get_object_or_404(course, course_name=course_name)
            form_input = Attendance(class_name=classes1, course_name=courses1, student_name=students1,lecture_date=dates , lecture_topic =topic,
                                        attendaces="A")
            form_input.save()

    return render(request,'tables4t.html' , args)



def assignment(request,name,name2):
    try:
        classname = name
        coursename = name2
        class1 = get_object_or_404(classes, class_name=classname)
        course1 = get_object_or_404(course, course_name=coursename)
        assignment1 = Assignment.objects.filter(class_name=class1, course_name=course1)

        if(request.POST):
            assignment_name = request.POST.get('assignmentname')
            total_marks = request.POST.get('totalmarks')
            file = request.FILES.get('file')
            end_date = request.POST.get('enddate')
            if(assignment_name != "" and total_marks != "" and file != None and end_date !="" ):
                form_input = Assignment(assignment_name=assignment_name, total_marks =total_marks, file=file, end_date=end_date,
                                       status="Open", submission="Not Submitted",class_name=class1, course_name=course1)
                form_input.save()
                messages.success(request, 'Assignment Added Successfully', extra_tags=" success")
            else:
               messages.error(request, 'Please Fill-Out All Fields', extra_tags=" error")
    except:
        messages.error(request, ' Please Enter Correct Marks', extra_tags=" error")

    args = {'assignment1': assignment1}

    return render(request, 'tablest.html' , args)

def closeassignment(request,id):
    assignment1 = get_object_or_404(Assignment,id=id)
    class1 = get_object_or_404(classes, class_name=assignment1.class_name)
    course1 = get_object_or_404(course, course_name=assignment1.course_name)
    marks1 = Marks.objects.filter(assignment_name=assignment1)
    studentcourses1 = studentcourses.objects.filter(class_name=class1, course_name=course1)
    if (assignment1.status == "Closed"):
        messages.error(request, 'Assignment Already Closed ', extra_tags=" error")
    else:
        assignment1.status ="Closed"
        assignment1.save()
        messages.success(request, 'Assignment Closed Successfully', extra_tags=" success")

        for students1 in studentcourses1:
            students2 = get_object_or_404(student, roll_number=students1.student_roll_number)
            if not marks1:
                form_input = Marks(student_name=students2, assignment_name=assignment1,
                                   total_marks=assignment1.total_marks,
                                   file=None, obtained_marks="Not Marked", submission="Not Submitted", class_name=class1,
                                   course_name=course1, student_roll_number=students2.roll_number)
                form_input.save()
            else:
                for marks2 in marks1:
                    if (students2 == marks2.student_name):
                        pass
                    else:
                        form_input = Marks(student_name=students2, assignment_name=assignment1, total_marks=assignment1.total_marks,
                                       file=None, obtained_marks="Not Marked", submission="Not Submitted", class_name=class1,
                                       course_name=course1, student_roll_number=students2.roll_number)
                        form_input.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def marks(request,id):
    assignment1 = get_object_or_404(Assignment, id=id)
    class1 = get_object_or_404(classes, class_name=assignment1.class_name)
    course1 = get_object_or_404(course, course_name=assignment1.course_name)
    studentcourses1 = studentcourses.objects.filter(class_name = class1,course_name = course1)
    marks1 = Marks.objects.filter(class_name = class1, course_name = course1, assignment_name = assignment1)
    args = {'marks1':marks1 ,'studentcourses1':studentcourses1}
    if(request.POST):
        student1 = request.POST.get('selectstudent')
        obtmarks = request.POST.get('obtmarks')
        if( int(obtmarks) > assignment1.total_marks or int(obtmarks) <= 0):
            messages.error(request,' Please Enter Correct Marks', extra_tags=" error")
        else:
            marks2 = get_object_or_404(Marks, assignment_name=assignment1,student_roll_number = student1)
            marks2.obtained_marks = obtmarks
            marks2.save()
            messages.success(request, student1+' Marks Added Successfully', extra_tags=" success")
    return render(request, 'studentt.html',args)



###*************###
### delete views###
###*************###


def delete_assignment(request,id):

    assignment1 = get_object_or_404(Assignment,id=id)
    assignment1.delete()
    messages.error(request, 'Assignment deleted Successfully', extra_tags=" error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






