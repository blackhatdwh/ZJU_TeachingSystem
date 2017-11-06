from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.CharField(max_length=20)
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.school_id = instance.username
    instance.profile.save()

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    experience = models.TextField(blank=True)
    research = models.TextField(blank=True)
    style = models.TextField(blank=True)
    publication = models.TextField(blank=True)
    honor = models.TextField(blank=True)
    contact = models.TextField(blank=True)
    other = models.TextField(blank=True)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    plan = models.TextField(blank=True)
    book = models.TextField(blank=True)
    background = models.TextField(blank=True)
    exam = models.TextField(blank=True)
    knowledge = models.TextField(blank=True)
    project = models.TextField(blank=True)

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time = models.TextField(blank=True)

class Teaches(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)

class Join(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)

class Information(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()

class Message(models.Model):
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()

class Resource(models.Model):
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    files = models.FileField(upload_to='resource/')
    simple_file = models.FileField(upload_to='resource/')

class Link(models.Model):
    name = models.CharField(max_length=20)
    address = models.URLField()

class Homework(models.Model):
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    files = models.FileField(upload_to='resource/homework/')
    ddl = models.DateTimeField()

class Finish(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    upload_time = models.DateTimeField()
    files = models.FileField(upload_to='homework/')
    score = models.IntegerField()
    evaluation = models.TextField()
