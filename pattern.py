from pdftotext import *
from sis.models import *
from django.core.exceptions import ObjectDoesNotExist
def writetodb(match):
    a = []
    b = []
    matches = match
    for i in matches:
	    a.append([i.group(1),i.group(2),i.group(3)])
	
    for j in a:
	    j[2] = j[2].split(', ')
	    j[2] = j[2][1:]
	    j[2].append(j[1])
	    del j[1]
    sem = Semester.objects.get(semester_code='s3')
    new_pattern = r'(\w+)\((\w+[+]?)\)'
    new_pattern = re.compile(new_pattern)
    for i in a:
	    #print(i[0])
        try:
            print(i[0])
            cuser = CustomUser.objects.get(username=i[0])
            stud = Student.objects.get(user=cuser)
        except ObjectDoesNotExist:
            print("failed")
            continue
        for j in i[1]:
            s = new_pattern.finditer(j)
            for k in s:
                try:
                    c = Course.objects.get(course_code=k.group(1))
                except ObjectDoesNotExist:
                    c = Course.objects.create(course_code=k.group(1),course_name=k.group(1),semester=sem)
            
                try:
                    e = Exam.objects.get(student=stud,semester=sem,course=c)
                    e.grade = k.group(2)
                    e.save()
                    print("already exist so re writing...")
                except ObjectDoesNotExist:
                    e = Exam(student=stud,semester=sem,course=c,grade=k.group(2))
                    e.save()
                    print("adding new exam register..")
            #print("{} : {} ".format(k.group(1),k.group(2)))​