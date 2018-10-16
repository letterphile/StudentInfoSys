from pdftotext import *
from sis.models import *
from django.core.exceptions import ObjectDoesNotExist
def writetodb(match,semid):
    a = []
    matches = match
    for i in matches:
	    a.append([i.group(1),i.group(2),i.group(3)])
	
    for j in a:
	    j[2] = j[2].split(', ')
	    j[2] = j[2][1:]
	    j[2].append(j[1])
	    del j[1]
    #sem = Semester.objects.get(id=int(semid))
    new_pattern = r'(\w+)\((\w+[+]?)\)'
    new_pattern = re.compile(new_pattern)
    for i in a:
	    #print(i[0])
        try:
            cuser = CustomUser.objects.get(username=i[0])
            stud = Student.objects.get(user=cuser)
        except ObjectDoesNotExist:
            continue
        for j in i[1]:
            s = new_pattern.finditer(j)
            for k in s:
                try:
                    c = Course.objects.get(course_code=k.group(1))
                except ObjectDoesNotExist:
                    continue
                try:
                    e = Exam.objects.get(student=stud,course=c)
                    if (k.group(2) != 'Absent'):
                        e.grade = k.group(2)
                    e.save()
                    print("already exist so re writing...")
                except ObjectDoesNotExist:
                    continue
            #print("{} : {} ".format(k.group(1),k.group(2)))​