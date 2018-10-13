from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .forms import *
from pdftotext import *
from pattern import *
import os
from django.conf import settings
# Create your views here.
def show_home(request):
    if  not request.user.is_anonymous:
        if request.user.usertype == 'STUDENT':
            return redirect('view_user',username=request.user.username)
    return render(request,'home.html')
@login_required(login_url='/accounts/login')
def view_students(request):
    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    students = Student.objects.all()
    return render(request,'StudView.html',{'students':students})

@login_required(login_url='/accounts/login')
def view_faculty(request):
    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')
    return render(request,'FacView.html')

@login_required(login_url='/accounts/login')
def view_subjects(request):
    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    return render(request,'SubView.html')

@login_required(login_url='/accounts/login')
def reg_student(request):

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    f_action=1
    semesters = Semester.objects.all()
    batches = Batch.objects.all()
    branches = Branch.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        roll_num = request.POST.get('roll')
        password = request.POST.get('password')
        sem = request.POST.get('semester')
        branch = request.POST.get('branch')
        batch = request.POST.get('batch')
        username='PJR'
        username+='{}{}{}'.format(batch[2:],branch.upper()[:-1],str(roll_num).zfill(3))

        s = CustomUser(first_name=first_name,last_name=last_name,username=username,usertype='STUDENT')
        try :
            s.save()
            s.set_password(password)
            s.save()
            batch = Batch.objects.get(year=int(batch))
            branch = Branch.objects.get(branch_code__startswith=branch)
            sem  = Semester.objects.get(id=int(sem))
            s = Student(user=s,branch=branch,semester=sem,batch=batch)
            s.rollnumber = roll_num
            s.save()
            return render(request,'regresult.html',{'flag':True,'student':s,'f_action':f_action})

        except IntegrityError:
            return render(request,'regresult.html',{'flag':False,'f_action':f_action})
    first_name=""
    last_name=""
    roll_num=""
    password=""
    sem=""
    sem_id=""
    branch=""
    batch=""
    return render(request,'StudReg.html',{'first_name':first_name,'last_name':last_name,'roll_num':roll_num,
    'password':password,'sem':sem,'sem_id':sem_id,'branch':branch,'batch':batch,'f_action':f_action,
    'semesters':semesters,'branches':branches,'batches':batches})

@login_required(login_url='/accounts/login')
def score(request):
    return render(request,'Score.html')

@login_required(login_url='/accounts/login')
def reg_subjects(request):
    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    return render(request,'SubEntry.html')

@login_required(login_url='/accounts/login')
def reg_faculty(request):
    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')

    return render(request,'FacReg.html')

@login_required(login_url='/accounts/login')
def view_user(request,username):
    if  request.user.usertype != 'ADMIN' and request.user.username != username:
        return render(request,'no_auth.html')
    s = get_object_or_404(CustomUser,username=username)
    req_user = request.user
    flag=False 
    if req_user.usertype == 'ADMIN':
        flag = True 
    print(flag)
    print(req_user.usertype)
    return render(request,'view_student.html',{'user':s,'flag':flag})

@login_required(login_url='/accounts/login')
def del_user(request,username):
    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
 
    s= get_object_or_404(CustomUser,username=username)
    user_name= s.username
    s.delete()
    return render(request,'del_user.html',{'user_name':user_name})

@login_required(login_url='/accounts/login')
def edit_user(request,username):

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')
    semesters = Semester.objects.all()
    batches = Batch.objects.all()
    branches = Branch.objects.all()
    s=get_object_or_404(CustomUser,username=username)
    first_name=s.first_name
    last_name=s.last_name
    roll_num=s.student_set.get(user=s).rollnumber
    password=""
    sem=s.student_set.get(user=s).semester
    sem_id=sem.id
    branch=s.student_set.get(user=s).branch
    branch_code = branch.branch_code
    batch=s.student_set.get(user=s).batch
    userid=s.username
    f_action = 0
    if request.method == 'POST':
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        roll_num = request.POST.get('roll')
        password = request.POST.get('password')
        sem = request.POST.get('semester')
        branch = request.POST.get('branch')
        batch = request.POST.get('batch')
        s.first_name = first_name
        s.last_name= last_name
        if password != "":
            s.set_password(password)
        s.save()
        stud = s.student_set.get(user=s)
        batch = Batch.objects.get(year=int(batch))
        branch = Branch.objects.get(branch_code__startswith=branch)
        branch_code =branch.branch_code
        sem  = Semester.objects.get(id=int(sem))
        sem_id = sem.id
        stud.semester = sem
        stud.batch = batch
        stud.branch = branch
        stud.rollnumber = roll_num
        stud.save()
    return render(request,'StudReg.html',{'first_name':first_name,'last_name':last_name,'roll_num':roll_num,
    'password':password,'sem':sem,'sem_id':sem_id,'branch_code':branch_code,'branch':branch,'batch':str(batch),'user_id':userid,'f_action':f_action,
    'branches':branches,'semesters':semesters,'batches':batches})

@login_required(login_url='/accounts/login')
def view_result(request,username):
    if request.user.username != username and request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
    cuser = get_object_or_404(CustomUser,username=username)
    flag = False
    req_user = request.user
    if req_user.usertype == 'ADMIN':
        flag = True
    stud = Student.objects.get(user=cuser)
    results = Exam.objects.filter(student=stud)
    s1=None
    s2=None
    s3=None
    s4=None
    s5=None
    s6=None
    s7=None
    s8=None

    if results.filter(semester=Semester.objects.get(semester_code='s3')).count() is not 0:
        s3 = results.filter(semester=Semester.objects.get(semester_code='s3'))
    if results.filter(semester=Semester.objects.get(semester_code='s1')).count() is not 0:
        s1 = results.filter(semester=Semester.objects.get(semester_code='s1'))
    if results.filter(semester=Semester.objects.get(semester_code='s2')).count() is not 0:
        s2 = results.filter(semester=Semester.objects.get(semester_code='s2'))
    if results.filter(semester=Semester.objects.get(semester_code='s4')).count() is not 0:
        s4 = results.filter(semester=Semester.objects.get(semester_code='s4'))
    if results.filter(semester=Semester.objects.get(semester_code='s5')).count() is not 0:
        s5 = results.filter(semester=Semester.objects.get(semester_code='s5'))

    if results.filter(semester=Semester.objects.get(semester_code='s6')).count() is not 0:
        s6 = results.filter(semester=Semester.objects.get(semester_code='s6'))

    if results.filter(semester=Semester.objects.get(semester_code='s7')).count() is not 0:
        s7 = results.filter(semester=Semester.objects.get(semester_code='s7'))
    if results.filter(semester=Semester.objects.get(semester_code='s8')).count() is not 0:
        s8 = results.filter(semester=Semester.objects.get(semester_code='s8'))

    return render (request,'view_result.html',{'s1':s1,'s2':s2,'s3':s3,'s4':s4,'s5':s5,'s6':s6,'s7':s7,'s8':s8,'flag':flag})

@login_required(login_url='/accounts/login')
def form_upload(request):
    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
    marklists = MarkList.objects.all()
    print(marklists)
    if request.method == 'POST':
        form = MarkListForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            form.save()
    else:
        form = MarkListForm()
    return render(request, 'form_upload.html', {
        'form': form,'marklists':marklists
    })

@login_required(login_url='/accounts/login')
def process(request):
    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')
    marklists = MarkList.objects.all()
    return render(request,'process.html',{'marklists':marklists})

@login_required(login_url='/accounts/login')
def process_file(request,id,semid):
    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    marklist = MarkList.objects.get(id=id)
    file_path = os.path.join(settings.BASE_DIR,'media/{}'.format(marklist.document.name))
    print(file_path)
    matches=ptot(file_path)
    print(matches)
    writetodb(matches,semid) 
    return redirect('process')

@login_required(login_url='/accounts/login')
def not_auth(request):
    return render(request,'no_auth.html')