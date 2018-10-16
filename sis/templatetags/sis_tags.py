from django import template

register = template.Library()
def user_auth(user,logs):
        return {'user':user,'logs':logs}

register.inclusion_tag('home1.html')(user_auth)

def user_not_auth(user):
    return {'user':user}

register.inclusion_tag('index.html')(user_not_auth)

def student_user(user):
    return {'user':user}

register.inclusion_tag('index.html')(student_user)