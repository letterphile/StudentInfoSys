from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

