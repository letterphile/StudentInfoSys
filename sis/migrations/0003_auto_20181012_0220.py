# Generated by Django 2.0.7 on 2018-10-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0002_student_rollnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]
