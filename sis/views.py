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
from django.contrib.postgres.search import TrigramSimilarity
# Create your views here.
def show_home(request):
    if  not request.user.is_anonymous:
        log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
        log.save()
        if request.user.usertype == 'STUDENT':
            return redirect('view_user',username=request.user.username)
    logs = Logs.objects.all()
    return render(request,'home.html',{'logs':logs})
@login_required(login_url='/accounts/login')
def view_students(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    students = Student.objects.all()
    return render(request,'StudView.html',{'students':students})

@login_required(login_url='/accounts/login')
def view_faculty(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')
    return render(request,'FacView.html')

@login_required(login_url='/accounts/login')
def view_subjects(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    return render(request,'SubView.html')

@login_required(login_url='/accounts/login')
def reg_student(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

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

        s = CustomUser(first_name=first_name,last_name=last_name,username=username,usertype='STUDENT',name=first_name+' '+last_name)
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
            log = Logs(user=request.user,activity="record inserted",place="<Student> Table")
            log.save()
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
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    return render(request,'SubEntry.html')

@login_required(login_url='/accounts/login')
def reg_faculty(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()
    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')

    return render(request,'FacReg.html')

@login_required(login_url='/accounts/login')
def view_user(request,username):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()
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
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
 
    s= get_object_or_404(CustomUser,username=username)
    user_name= s.username
    s.delete()
    log = Logs(user=request.user,activity="record deleted",place="<CustomUser> Table")
    log.save()

    return render(request,'del_user.html',{'user_name':user_name})

@login_required(login_url='/accounts/login')
def edit_user(request,username):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

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
        name = first_name+" "+last_name
        roll_num = request.POST.get('roll')
        password = request.POST.get('password')
        sem = request.POST.get('semester')
        branch = request.POST.get('branch')
        batch = request.POST.get('batch')
        s.first_name = first_name
        s.last_name= last_name
        s.name = name
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
        log = Logs(user=request.user,activity="record edited",place="<Student> Table")
        log.save()

    return render(request,'StudReg.html',{'first_name':first_name,'last_name':last_name,'roll_num':roll_num,
    'password':password,'sem':sem,'sem_id':sem_id,'branch_code':branch_code,'branch':branch,'batch':str(batch),'user_id':userid,'f_action':f_action,
    'branches':branches,'semesters':semesters,'batches':batches})

@login_required(login_url='/accounts/login')
def view_result(request,username):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.username != username and request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
    cuser = get_object_or_404(CustomUser,username=username)
    flag = False
    req_user = request.user
    if req_user.usertype == 'ADMIN':
        flag = True #Used to render the page according to the type of the user
    stud = Student.objects.get(user=cuser)
    results = Exam.objects.filter(student=stud)
    #variables to store results of each semester
    s1_results=[]
    s2_results=[]
    s3_results=[]
    s4_results=[]
    s5_results=[]
    s6_results=[]
    s7_results=[]
    s8_results=[]

    #variables to store each semester
    s1 = Semester.objects.get(semester_code='s1')
    s2 = Semester.objects.get(semester_code='s2')
    s3 = Semester.objects.get(semester_code ='s3')
    s4 = Semester.objects.get(semester_code='s4')
    s5 = Semester.objects.get(semester_code='s5')
    s6 = Semester.objects.get(semester_code='s6')
    s7 = Semester.objects.get(semster_code = 's7')
    s8 = Semester.objects.get(semster_code = 's8')

    #getting courses of each semester
    s1_courses = Course.objects.filter(semester = s1)
    s2_courses = Course.objects.filter(semester = s2)
    s3_courses = Course.objects.filter(semester = s3)
    s4_courses = Course.objects.filter(semester = s4)
    s5_courses = Course.objects.filter(semester = s5)
    s6_courses = Course.objects.filter(semester = s6)
    s7_courses = Course.objects.filter(semester = s7)
    s8_courses = Course.objects.filter(semester = s8)

    #Retrieving all results by courses
    for course in s1_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s1_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue
    for course in s2_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s2_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue

    for course in s3_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s3_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue

    for course in s4_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s4_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue

    for course in s5_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s5_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue


    for course in s6_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s6_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue

    for course in s7_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s7_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue

    for course in s8_courses:
        try:
            #appends each result of 's1 courses'  of 'student' to 's1 results' 
            s8_results.append(results.get(course=course))
        except ObjectDoesNotExist:
            continue


    return render (request,'view_result.html',{'s1':s1_results,'s2':s2_results,'s3':s3_results,'s4':s4_results,'s5':s5_results,'s6':s6_results,'s7':s7_results,'s8':s8_results,'flag':flag})

@login_required(login_url='/accounts/login')
def form_upload(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
    marklists = MarkList.objects.all()
    print(marklists)
    if request.method == 'POST':
        form = MarkListForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            form.save()
            log = Logs(user=request.user,activity="file uploaded",place="<MarkList> Table")
            log.save()

    else:
        form = MarkListForm()
    return render(request, 'form_upload.html', {
        'form': form,'marklists':marklists
    })

@login_required(login_url='/accounts/login')
def process(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')
    marklists = MarkList.objects.all()
    return render(request,'process.html',{'marklists':marklists})

@login_required(login_url='/accounts/login')
def process_file(request,id,semid):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
        return render(request,'no_auth.html')

    marklist = MarkList.objects.get(id=id)
    file_path = os.path.join(settings.BASE_DIR,'media/{}'.format(marklist.document.name))
    print(file_path)
    matches=ptot(file_path)
    print(matches)
    writetodb(matches,semid) 
    log = Logs(user=request.user,activity="Record Inserted",place="<Exam> Table")
    log.save()

    return redirect('process')

@login_required(login_url='/accounts/login')
def not_auth(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    return render(request,'no_auth.html')

@login_required(login_url='/accounts/login')
def search(request):
    log = Logs(user=request.user,activity="visited",place=request.build_absolute_uri())
    log.save()

    if request.user.usertype != 'ADMIN':
       return render(request,'no_auth.html')
    query=""
    query = request.GET.get('query')
    if query is None:
        query = ""
    print(query)
    results = CustomUser.objects.annotate(
    similarity=TrigramSimilarity('name',query),
    ).filter(similarity__gt=0.0).order_by('-similarity')
    if query == "":
        results = CustomUser.objects.all()
    print(results)
    return render(request,'search2.html',{'results':results,'query':query})