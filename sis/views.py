from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def admin(request):
    login_name = 'Administrator Login'
    context = {'login_name':login_name}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = 'aswin4400@gmail.com'
        passw = 'password'
        if username == email and password == passw :
            return render(request,'adminhome.html')
    return render(request,'adminlogin.html',context) 

def hod(request):
    login_name = 'HOD Login'
    context = {'login_name':login_name}
    return render(request,'hodlogin.html',context)
def staff(request):
    login_name = 'Staff Login'
    context = {'login_name':login_name}
    return render(request,'stafflogin.html',context)
def student(request):
    login_name='Student Login'
    context = {'login_name':login_name}
    return render(request,'studentlogin.html',context)

def student_reg(request):
    return render(request,'StudReg.html')

def student_view(request):
    return render(request,'StudView.html')

def score(request):
    return render(request,'Score.html')

def faculty_reg(request):
    return render(request,'FacReg.html')

def subject_reg(request):
    return render(request,'SubEntry.html')

def subject_view(request):
    return render(request,'SubView.html')

def faculty_view(request):
    return render(request,'FacView.html')