from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from Admin.models import student,customuser,studentcourses,course,classes
from Teacher.models import Attendance,Assignment
from .models import Marks

# Create your views here.
def student1(request):
    user1 = request.user
    students = get_object_or_404(student,roll_number = user1.username )
    studentscourses = studentcourses.objects.filter(student_name = students).count()

    args = {'students':students, 'studentscourses':studentscourses }



    return render(request, 'indexs.html' , args)


def login1(request):
    return render(request, 'logins.html')



def dologin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:

        user = authenticate(request, username=request.POST.get("email"),
                            password=request.POST.get("password"))
        if user != None:
            if user.is_active:
                if user.user_type == "3":
                    login(request, user)
                    return HttpResponseRedirect('student')
                else:
                    messages.error(request, 'please enter correct credentials', extra_tags=" error")
                    return HttpResponseRedirect('/student/login')
        else:
            messages.error(request, 'please enter correct credentials', extra_tags=" error")
            return HttpResponseRedirect('/student/login')
    return HttpResponseRedirect('/student/login')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/student/login')



def forgotpassword(request):
    try:
        if (request.POST):
            forgot = request.POST.get("forgotpass")
            students = student.objects.get(email=forgot)
            # send an email
            send_mail(
                'Credentials of Student Portal',  # subject
                'Here is your password : ' + students.passwd,  # message
                '',  # from email
                [students.email]  # to email
            )
            messages.success(request, 'We have mailed your password', extra_tags=" success")
        return render(request, 'forgot-password.html')
    except student.DoesNotExist:
        messages.error(request, 'Email Does NoT Exist', extra_tags=" error")
        return render(request, 'forgot-password.html')




def profile(request):
    user1 = request.user
    students = get_object_or_404(student, roll_number=user1.username)
    students1 = get_object_or_404(customuser, username=user1.username)
    if (request.POST):
        student_name = request.POST.get("changename")
        email = request.POST.get("changeemail")
        password = request.POST.get("changepassword")

        profile_pic = request.FILES.get('changeimage', False)

        if (student_name != ""):
            students1.name = student_name
            students.student_name = student_name
        if (email != ""):
            students1.email = email
            students.email = email
        if (password != ""):
            students1.set_password(password)
            students.passwd = password
        if (profile_pic != False):
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            students.image = profile_pic_url
        students.save()
        students1.save()

    args = {'students':students}

    return render(request, 'profiles.html', args)


def assignedcourses(request):
    user1 = request.user
    students = get_object_or_404(student, roll_number=user1.username)
    studentscourses = studentcourses.objects.filter(student_name=students)


    args = {'studentscourses':studentscourses }


    return render(request, 'tables3s.html',args)

def attendance1(request,name,name2):
    classname = name
    coursename = name2
    courses = get_object_or_404(course, course_name = coursename)
    class1 = get_object_or_404(classes,class_name = classname)
    attendances = Attendance.objects.filter(class_name = class1 , course_name = courses.id)
    attendances1 = Attendance.objects.filter(class_name = class1 , course_name = courses.id, attendaces = "P").count()
    attendances2 = Attendance.objects.filter(class_name=class1, course_name= courses.id, attendaces="A").count()
    attendances3 = attendances.count()
    if(attendances3 == 0):
        attendances4 = 100
    else:
        attendances4 = (attendances1 * 100)/attendances3
    args = {'attendances': attendances, 'attendances1':attendances1, 'attendances2':attendances2, 'attendances3':attendances3, 'attendances4':attendances4 }

    return render(request, 'tables4s.html', args)

def assignment(request):
    user1=request.user
    student1 = get_object_or_404(student, roll_number=user1.username)
    students = get_object_or_404(studentcourses, student_name=student1)
    class1 = get_object_or_404(classes, class_name=students.class_name)
    course1 = get_object_or_404(course, course_name=students.course_name)
    assignment1 = Assignment.objects.filter(class_name=class1, course_name=course1)
    args = {'assignment1':assignment1}
    return render(request, 'tables5s.html',args)

def pendingassignment(request):
    try:
        user1 = request.user
        student1 = get_object_or_404(student, roll_number=user1.username)
        students = get_object_or_404(studentcourses, student_name=student1)
        class1 = get_object_or_404(classes, class_name=students.class_name)
        course1 = get_object_or_404(course, course_name=students.course_name)
        assignment1 = Assignment.objects.filter(class_name=class1, course_name=course1, status="Open", submission = "Not Submitted")

        if (request.POST):
            assignment2 = request.POST.get('selectassignment')
            file = request.FILES.get('file')
            if(assignment2 != None and file != None ):
                assignment3 = get_object_or_404(Assignment, assignment_name=assignment2, class_name=class1,
                                            course_name=course1)
                assignment3.submission = "Submitted"
                assignment3.save()
                form_input = Marks( student_name = student1, assignment_name=assignment3, total_marks=assignment3.total_marks, file=file,obtained_marks = "Not Marked" , submission="Submitted", class_name=class1, course_name=course1, student_roll_number=student1.roll_number)
                form_input.save()
                messages.success(request, 'Assignment submitted Successfully', extra_tags=" success")
            else:
                messages.error(request, 'Please Select All fields Correctly', extra_tags=" error")

        args = {'assignment1': assignment1}
        return render(request, 'students.html', args)
    except:
        if(request.POST):
            messages.error(request, 'No Assignment Assigned', extra_tags=" error")

        return render(request, 'students.html')
def marks(request,id):
    marks3 = 0
    marks4 = 0
    studentcourse1 = get_object_or_404(studentcourses, id=id)
    user1 = request.user
    student1 = get_object_or_404(student, roll_number=user1.username)
    course1 = get_object_or_404(course, course_name = studentcourse1.course_name)
    marks1 = Marks.objects.filter(student_name = student1, course_name = course1)
    for marks2 in marks1:
        if (marks2.obtained_marks != "Not Marked"):
            marks3 = marks3 + marks2.total_marks
            marks4 = marks4 + int(marks2.obtained_marks)

    args = {'marks1':marks1, 'marks3':marks3, 'marks4':marks4 }
    return render(request, 'tabless.html',args)