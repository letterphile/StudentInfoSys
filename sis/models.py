from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    choices = (
        ('STUDENT','Student'),
        ('TEACHER','Teacher'),
        ('ADMIN','Admin'),
    )
    usertype = models.CharField(max_length=50,choices=choices)

    def __str__(self):
        return self.username
class Batch(models.Model):
    year = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ('year',)
    def __str__(self):
        return str(self.year)
class Branch(models.Model):
    branch_name= models.CharField(max_length=50)
    branch_code = models.CharField(max_length=3)
    class Meta:
        ordering =  ('branch_name',)
    def __str__(self):
        return self.branch_name

class Semester(models.Model):
    semester_name = models.CharField(max_length = 10)
    semester_code = models.CharField(max_length = 2)
    class Meta:
        ordering = ('semester_code',)
    def __str__(self):
        return self.semester_name
        

class Course(models.Model):
    course_name = models.CharField(max_length= 45)
    course_code = models.CharField(max_length=7)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    branch = models.ManyToManyField(Branch)
    attendance = models.PositiveIntegerField(default=1)
    faculty  = models.ForeignKey('Faculty',null=True,on_delete=models.SET_NULL)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return self.course_name

class Student(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.user)

class Exam(models.Model):
    grades = (('O','O'),('A+','A+'),('A','A'),('B+','B+'),('C','C'),('D','D'),('P','P'))
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    grade  = models.CharField(max_length=2,choices=grades)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.course) +" "+ str(self.student)

class Faculty(models.Model):
    gender_choices = (('MALE','male'),('FEMALE','female'))
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    email = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    dob = models.DateField()
