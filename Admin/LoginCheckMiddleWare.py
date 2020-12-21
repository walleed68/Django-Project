from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user

        if user.is_authenticated:
            if user.is_active:
                if user.user_type == "1":
                    if modulename == "Admin.views" or modulename == "django.views.static":
                        pass
                    else:
                        return HttpResponseRedirect(reverse("main_admin_page"))
                elif user.user_type == "2":
                    if modulename == "Teacher.views" or modulename == "django.views.static":
                        pass
                    else:
                        return HttpResponseRedirect(reverse("teacher_page"))
                elif user.user_type == "3":
                    if modulename == "Student.views" or modulename == "django.views.static":
                        pass
                    else:
                        return HttpResponseRedirect(reverse("student_page"))
        else:

            if request.path == reverse("login_page") or request.path == reverse("do_login_page") or request.path == reverse("teacher_login_page") or request.path == reverse("teacher_do_login_page") or request.path == reverse("student_login_page") or request.path == reverse("student_do_login_page") or request.path == reverse("student_forget_password_page") or request.path == reverse("teacher_forget_password_page") or request.path == reverse("forgot_password_page"):
                pass
            elif modulename == "Admin.views":
                return HttpResponseRedirect(reverse("login_page"))
            elif modulename == "Teacher.views":
                return HttpResponseRedirect(reverse("teacher_login_page"))
            elif modulename == "Student.views":
                return HttpResponseRedirect(reverse("student_login_page"))