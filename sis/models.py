from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    choices = (
        ('STUDENT','Student'),
        ('TEACHER','Teacher'),
        ('ADMIN','Admin'),
        ('HOD','HOD'),
    )
    usertype = models.CharField(max_length=50,choices=choices,default='STUDENT')
    user_slug = models.SlugField(max_length=25,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    def get_absolute_url(self):
        return reverse('view_user', kwargs={'username': self.username})

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
    branch_code = models.CharField(max_length=3,unique=True)
    hod = models.ForeignKey(CustomUser,on_delete = models.CASCADE,null=True)
    class Meta:
        ordering =  ('branch_name',)
    def __str__(self):
        return self.branch_name

class Semester(models.Model):
    semester_name = models.CharField(max_length = 10)
    semester_code = models.CharField(max_length = 2,unique=True)
    class Meta:
        ordering = ('semester_code',)
    def __str__(self):
        return self.semester_name
        

class Course(models.Model):
    course_name = models.CharField(max_length= 80)
    course_code = models.CharField(max_length=7,unique=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    branch = models.ManyToManyField(Branch)
    attendance = models.PositiveIntegerField(default=1)
    faculty  = models.ForeignKey('Faculty',null=True,on_delete=models.SET_NULL)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return self.course_name

class Student(models.Model):
    gender_choices=(('M','Male'),('F','Female'))
    rollnumber = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,choices=gender_choices,null=True)
    dob = models.DateField(null=True)
    pob  = models.CharField(max_length=50,null=True)
    address1 = models.TextField(null=True)
    address2 = models.TextField(null=True)
    city = models.CharField(max_length=20,null=True)
    pin = models.PositiveIntegerField(null=True)


    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.user)

class Exam(models.Model):
    grades = (('O','O'),('A+','A+'),('A','A'),('B+','B+'),('C','C'),('D','D'),('P','P'),('Absent','Absent'))
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    grade  = models.CharField(max_length=10,choices=grades)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.course) +" "+ str(self.student)

class Faculty(models.Model):
    gender_choices = (('MALE','male'),('FEMALE','female'))
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    dob = models.DateField()

class MarkList(models.Model):
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Logs(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    activity = models.CharField(max_length=25)
    place = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-time',)