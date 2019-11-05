from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .models import Student, Faculty, Course, Subject, Question, Test
from django.http import HttpResponse


def index(request):
    try:
        if request.session['no_session']==1:
            context = {'message': 'Please Login'}
            return render(request, 's_login.html', context)
        else:
            return render(request, 's_login.html', {})
    except:
        context = {}
        return render(request, 's_login.html', context)



def sDash(request):
    if request.session.get('email', None) :
        lv_dbdata = Student.objects.get(email=request.session.get('email', None))
        context = {
            'username': lv_dbdata.fname
        }
        print('------------>>>>', context)
        return render(request, 'sdash.html', context)
    else:
        request.session['no_session'] = '1'
        return redirect('index')


@csrf_exempt
def sLogin(request):
    if request.method == 'POST':
        lv_email = request.POST.get("email")
        lv_password = request.POST.get("password")
        dbQuery = Student.objects.filter(email=lv_email)
        if dbQuery.count() == 1:
            print(">>>>> [INFO] ", lv_email, lv_password)
            request.session['email'] = lv_email
            return redirect('Dashboard')
            # return redirect('Dashboard', lv_fname)
        else:
            return HttpResponse("Invalid Credentials")
    else:
        return redirect('index')


def logout_request(request):
    logout(request)
    request.session['no_session'] = 0
    return redirect("index")
#     messages.info(request, "Logged out successfully!")


def faculty_login(request):
    if request.method == 'POST':
        lv_email = request.POST.get("email")
        lv_password = request.POST.get("password")
        dbQuery = Faculty.objects.filter(email=lv_email)
        if dbQuery.count() == 1:
            print(">>>>> [INFO] ", lv_email, lv_password)
            request.session['f_email'] = lv_email
            lv_dbdata = Faculty.objects.get(email=request.session.get('f_email', None))
            request.session['f_username'] = lv_dbdata.fname
            return redirect('Fac_Dash')
            # return redirect('Dashboard', lv_fname)
        else:
            return render(request, 'fac_login.html', {'message': 'Invalid Credentials'})
    else:
        try:
            if request.session['no_session'] == 1:
                return render(request, 'fac_login.html', {'message': 'Please Login'})
            else:
                return render(request, 'fac_login.html', {})
        except:
            return render(request, 'fac_login.html', {})
    return render(request, 'fac_login.html', {})


def fac_dash(request):
    if request.session.get('f_email', None) :
        lv_dbdata = Faculty.objects.get(email=request.session.get('f_email', None))
        context = {
            'username': lv_dbdata.fname,
            'admin': lv_dbdata.admin
        }
        print('------------>>>>', context)
        return render(request, 'fdash.html', context)
    else:
        request.session['no_session'] = '1'
        return redirect('faculty')


def student_list(request):
    if request.session.get('f_email', None):
        try:
            if request.session['message_code']:
                pass
        except:
            request.session['message_code'] = 0
        lv_dbdata = Student.objects.all()
        lv_userdata = Faculty.objects.get(email=request.session.get('f_email', None))
        context = {'student_list': lv_dbdata,
                   'message_code': request.session['message_code'],
                   'username': lv_userdata.fname,
                   'admin': lv_userdata.admin}
        if request.session.get('flag', None) == 1:
            request.session['message_code'] = 0
        return render(request, 'fstudent_list.html', context)
    else:
        request.session['no_session'] = '1'
        return redirect('faculty')


@csrf_exempt
def create_student(request):
    if request.session.get('f_email', None) and request.method == 'POST':
        lv_email = request.POST.get("email")
        lv_fname = request.POST.get("fname")
        lv_lname = request.POST.get("lname")
        lv_password = request.POST.get("password")
        dbQuery = Student.objects.filter(email=lv_email)
        if dbQuery.count() > 0:
            print(">>>>> [ERROR] already exists -> ", lv_email, lv_password)
            request.session['message_code'] = 3
            request.session['flag'] = 1
            return redirect('student_list')
        elif dbQuery.count() == 0:
            s1 = Student(email=lv_email, fname=lv_fname, lname=lv_lname, password=lv_password)
            s1.save()
            dbQuery = Student.objects.filter(email=lv_email)
            if dbQuery.count()==1:
                request.session['message_code'] = 1
                request.session['flag'] = 1
                return redirect('student_list')
            else:
                request.session['message_code'] = 2
                request.session['flag'] = 1
                return redirect('student_list')
    else:
        return redirect('faculty')


@csrf_exempt
def delete_student(request):
    if request.session.get('f_email', None) and request.method == 'POST':
        lv_sid = request.POST.get("student_id")
        dbQuery = Student.objects.filter(id=lv_sid)
        if dbQuery.count() > 0:
            s1 = Student(id=lv_sid).delete()
            dbQuery = Student.objects.filter(id=lv_sid)
            if dbQuery.count()!=0:
                request.session['message_code'] = 2
                request.session['flag'] = 1
                return redirect('student_list')
            elif dbQuery.count()==0:
                request.session['message_code'] = 1
                request.session['flag'] = 1
                return redirect('student_list')
            return redirect('student_list')
    else:
        return redirect('faculty')


def f_admin(request):
    if request.session.get('f_email', None):
        try:
            if request.session['message_code']:
                pass
        except:
            request.session['message_code'] = 0
        lv_userdata = Faculty.objects.get(email=request.session.get('f_email', None))
        if lv_userdata.admin == '1':
            lt_facdata = Faculty.objects.all()
            context = {'faculty_list': lt_facdata,
                       'message_code': request.session['message_code'],
                       'username': lv_userdata.fname,
                       'admin': lv_userdata.admin}
            if request.session.get('flag', None) == 1:
                request.session['message_code'] = 0
            return render(request, 'f_admin.html', context)
        else:
            return redirect('fac_dash')
    else:
        request.session['no_session'] = '1'
        return redirect('faculty')
    return redirect('faculty')


@csrf_exempt
def create_faculty(request):
    if request.session.get('f_email', None) and request.method == 'POST':
        lv_email = request.POST.get("email")
        lv_fname = request.POST.get("fname")
        lv_lname = request.POST.get("lname")
        lv_password = request.POST.get("password")
        lv_admin = request.POST.get("adminright")
        dbQuery = Faculty.objects.filter(email=lv_email)
        if dbQuery.count() > 0:
            print(">>>>> [ERROR] already exists -> ", lv_email, lv_password)
            request.session['message_code'] = 3
            request.session['flag'] = 1
            return redirect('student_list')
        elif dbQuery.count() == 0:
            f1 = Faculty(email=lv_email, fname=lv_fname, lname=lv_lname, password=lv_password, admin=lv_admin)
            f1.save()
            dbQuery = Faculty.objects.filter(email=lv_email)
            if dbQuery.count()==1:
                request.session['message_code'] = 1
                request.session['flag'] = 1
                return redirect('f_admin')
            else:
                request.session['message_code'] = 2
                request.session['flag'] = 1
                return redirect('f_admin')
        else:
            return redirect('faculty')


def course_list(request):
    if request.session.get('f_email', None):
        try:
            if request.session['message_code']:
                pass
        except:
            request.session['message_code'] = 0
        lv_dbdata = Course.objects.all()
        lv_userdata = Faculty.objects.get(email=request.session.get('f_email', None))
        context = {'course_list': lv_dbdata,
                   'message_code': request.session['message_code'],
                   'username': lv_userdata.fname,
                   'admin': lv_userdata.admin}
        if request.session.get('flag', None) == 1:
            request.session['message_code'] = 0
        return render(request, 'fcourse_list.html', context)
    else:
        request.session['no_session'] = '1'
        return redirect('faculty')


@csrf_exempt
def create_course(request):
    if request.session.get('f_email', None) and request.method == 'POST':
        lv_name = request.POST.get("name")
        dbQuery = Course.objects.filter(co_name=lv_name)
        if dbQuery.count() > 0:
            print(">>>>> [ERROR] already exists -> ", lv_name)
            request.session['flag'] = 1
            request.session['message_code'] = 3
            return redirect('course_list')
        elif dbQuery.count() == 0:
            c1 = Course(co_name=lv_name)
            c1.save()
            dbQuery = Course.objects.filter(co_name=lv_name)
            if dbQuery.count()==1:
                request.session['message_code'] = 1
                request.session['flag'] = 1
                return redirect('course_list')
            else:
                request.session['message_code'] = 2
                request.session['flag'] = 1
                return redirect('course_list')
    else:
        return redirect('faculty')


def subject_list(request):
    if request.session.get('f_email', None):
        try:
            if request.session['message_code']:
                pass
        except:
            request.session['message_code'] = 0
        lv_dbdata = Subject.objects.all()
        lv_courses = Course.objects.all()
        lv_userdata = Faculty.objects.get(email=request.session.get('f_email', None))
        context = {'subject_list': lv_dbdata,
                   'course_list': lv_courses,
                   'message_code': request.session['message_code'],
                   'username': lv_userdata.fname,
                   'admin': lv_userdata.admin}
        if request.session.get('flag', None) == 1:
            request.session['message_code'] = 0
        return render(request, 'fsubject_list.html', context)
    else:
        request.session['no_session'] = '1'
        return redirect('faculty')


@csrf_exempt
def create_subject(request):
    if request.session.get('f_email', None) and request.method == 'POST':
        lv_name = request.POST.get("name")
        lv_course = request.POST.get("course_id")
        dbQuery = Subject.objects.filter(sub_name=lv_name)
        if dbQuery.count() > 0:
            print(">>>>> [ERROR] already exists -> ", lv_name)
            request.session['flag'] = 1
            request.session['message_code'] = 3
            return redirect('subject_list')
        elif dbQuery.count() == 0:
            sub1 = Subject(sub_name=lv_name, co_name=lv_course)
            sub1.save()
            dbQuery = Subject.objects.filter(sub_name=lv_name)
            if dbQuery.count()==1:
                request.session['message_code'] = 1
                request.session['flag'] = 1
                return redirect('subject_list')
            else:
                request.session['message_code'] = 2
                request.session['flag'] = 1
                return redirect('subject_list')
    else:
        return redirect('faculty')



def test_list(request):
    if request.session.get('f_email', None):
        try:
            if request.session['message_code']:
                pass
        except:
            request.session['message_code'] = 0
        lv_dbdata = Subject.objects.all()
        lv_courses = Course.objects.all()
        lv_tests = Test.objects.all()
        lv_userdata = Faculty.objects.get(email=request.session.get('f_email', None))
        context = {'subject_list': lv_dbdata,
                   'test_list': lv_tests,
                   'course_list': lv_courses,
                   'message_code': request.session['message_code'],
                   'username': lv_userdata.fname,
                   'admin': lv_userdata.admin}
        if request.session.get('flag', None) == 1:
            request.session['message_code'] = 0
        return render(request, 'ftest_list.html', context)
    else:
        request.session['no_session'] = '1'
        return redirect('faculty')


@csrf_exempt
def create_test(request):
    if request.session.get('f_email', None) and request.method == 'POST':
        lv_name = request.POST.get("name")
        lv_course = request.POST.get("course_id")
        lv_subject = request.POST.get("subject_id")
        dbQuery = Test.objects.filter(test_name=lv_name)
        if dbQuery.count() > 0:
            print(">>>>> [ERROR] already exists -> ", lv_name)
            request.session['flag'] = 1
            request.session['message_code'] = 3
            return redirect('test_list')
        elif dbQuery.count() == 0:
            test1 = Test(test_name=lv_name, sub_name=lv_subject, co_name=lv_course)
            test1.save()
            dbQuery = Test.objects.filter(test_name=lv_name)
            if dbQuery.count()==1:
                request.session['message_code'] = 1
                request.session['flag'] = 1
                return redirect('test_list')
            else:
                request.session['message_code'] = 2
                request.session['flag'] = 1
                return redirect('test_list')
    else:
        return redirect('faculty')

