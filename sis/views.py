from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
# Create your views here.
def show_home(request):
    return render(request,'home.html')
@login_required(login_url='/accounts/login')
def view_students(request):
    students = Student.objects.all()
    return render(request,'StudView.html',{'students':students})

@login_required(login_url='/accounts/login')
def view_faculty(request):
    return render(request,'FacView.html')

@login_required(login_url='/accounts/login')
def view_subjects(request):
    return render(request,'SubView.html')

@login_required(login_url='/accounts/login')
def reg_student(request):
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
        username+='{}{}0{}'.format(batch[2:],branch.upper(),roll_num)

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
    return render(request,'SubEntry.html')

@login_required(login_url='/accounts/login')
def reg_faculty(request):
    return render(request,'FacReg.html')

@login_required(login_url='/accounts/login')
def view_user(request,username):
    s = get_object_or_404(CustomUser,username=username)
    return render(request,'view_student.html',{'user':s})

@login_required(login_url='/accounts/login')
def del_user(request,username):
    s= get_object_or_404(CustomUser,username=username)
    user_name= s.username
    s.delete()
    return render(request,'del_user.html',{'user_name':user_name})

@login_required(login_url='/accounts/login')
def edit_user(request,username):
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

