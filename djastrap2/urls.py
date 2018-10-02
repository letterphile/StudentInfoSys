"""djastrap2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from sis.views import * 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',show_home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('student_view/', view_students,name='view_students'),
    path('student_registration/',reg_student,name='reg_student'),
    path('faculty_view/',view_faculty,name='view_faculty'),
    path('faculty_registration/',reg_faculty,name='ref_faculty'),
    path('view_subjects/',view_subjects,name='view_subjects'),
    path('subject_registration/',reg_subjects,name='reg_subjects'),
    path('score/',score,name='score')
]
