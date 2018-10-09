from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
def show_home(request):
    return render(request,'home.html')
@login_required(login_url='/accounts/login')
def view_students(request):
    return render(request,'StudView.html')

@login_required(login_url='/accounts/login')
def view_faculty(request):
    return render(request,'FacView.html')

@login_required(login_url='/accounts/login')
def view_subjects(request):
    return render(request,'SubView.html')

@login_required(login_url='/accounts/login')
def reg_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        roll_num = request.POST.get('roll')
        password = request.POST.get('password')
        sem = request.POST.get('semester')
        branch = request.POST.get('branch')
        batch = request.POST.get('batch')
        username='PJR'
        username+='{}{}0{}'.format(batch,branch,roll_num)

        s = CustomUser(first_name=first_name,last_name=last_name,username=username,usertype='STUDENT')
        s.save()
        s.set_password(password)
        s.save()
        batch = Batch.objects.get(year=int('20'+batch))
        branch = Branch.objects.get(branch_code__startswith=branch)
        sem  = Semester.objects.get(id=int(sem))
        s = Student(user=s,branch=branch,semester=sem,batch=batch)
        s.save()

    return render(request,'StudReg.html')

@login_required(login_url='/accounts/login')
def score(request):
    return render(request,'Score.html')

@login_required(login_url='/accounts/login')
def reg_subjects(request):
    return render(request,'SubEntry.html')

@login_required(login_url='/accounts/login')
def reg_faculty(request):
    return render(request,'FacReg.html')
