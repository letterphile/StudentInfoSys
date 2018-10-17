from django import template
from datetime import timedelta
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
@register.simple_tag
def local_time(time):
    new_time = time + timedelta(seconds=19800)
    new_time = str(new_time)[:-13]
    return new_time