from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class PasswordQuestion(models.Model):
    question = models.CharField(max_length=50)
    def __str__(self):
        return self.question

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.CharField(max_length=20)
    question = models.ForeignKey(PasswordQuestion, on_delete=models.CASCADE, blank=True, null=True)
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
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    plan = models.TextField(blank=True)
    book = models.TextField(blank=True)
    background = models.TextField(blank=True)
    exam = models.TextField(blank=True)
    knowledge = models.TextField(blank=True)
    project = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Teaches(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self):
        return self.teacher.name + ' ' + self.clazz.name

class Join(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self):
        return self.student.name + ' ' + self.clazz.name

class Article(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    attached_file = models.FileField(upload_to='article_file/', blank=True)
    pub_date = models.DateTimeField()
    def __str__(self):
        return self.title

class Notification(models.Model):
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField()
    publisher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    attached_file = models.FileField(upload_to='resource/')
    simple_file = models.FileField(upload_to='resource/', blank=True)
    pub_date = models.DateTimeField()
    uploader = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Link(models.Model):
    name = models.CharField(max_length=20)
    address = models.URLField()
    def __str__(self):
        return self.name

class Homework(models.Model):
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    attached_file = models.FileField(upload_to='resource/homework/', blank=True)
    pub_date = models.DateTimeField()
    weight = models.IntegerField()
    ddl = models.DateTimeField()
    def __str__(self):
        return self.title

class Finish(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(blank=True, null=True)
    upload_file = models.FileField(upload_to='homework/', blank=True)
    score = models.IntegerField(default=0)
    evaluation = models.TextField(blank=True)
    checked = models.BooleanField(default=True)
    def __str__(self):
        return self.student.name + ' ' + self.homework.title
