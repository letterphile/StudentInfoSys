from django.urls import path
from . import views
app_name = 'sis'

urlpatterns = [
    path('',views.home,name='home'),
    path('admin/',views.admin,name='admin'),
    path('staff/',views.staff,name='staff'),
    path('hod/',views.hod,name='hod'),
    path('student/',views.student,name='student'),
    path('student_registration/',views.student_reg,name='student_reg'),
    path('student_view/',views.student_view,name='student_view'),
    path('score/',views.score,name='score'),
    path('faculty_registration/',views.faculty_reg,name="faculty_reg"),
    path('faculty_view/',views.faculty_view,name='faculty_view'),
    path('subject_registration/',views.subject_reg,name='subject_reg'),
    path('view_subjects/',views.subject_view,name='subject_view'),
]