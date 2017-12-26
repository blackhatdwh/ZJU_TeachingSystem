from django import forms
from .models import *

class NamePass(forms.Form):
    username = forms.CharField(label="用户名", max_length=100)
    password = forms.CharField(label="密码", max_length=100, widget=forms.PasswordInput())

class TeacherForm(forms.Form):
    name = forms.CharField(label="姓名", max_length=50)
    experience = forms.CharField(label="教学经历", widget=forms.Textarea, required=False)
    research = forms.CharField(label="科研成果", widget=forms.Textarea, required=False)
    style = forms.CharField(label="教学风格", widget=forms.Textarea, required=False)
    publication = forms.CharField(label="出版作品", widget=forms.Textarea, required=False)
    honor = forms.CharField(label="所获荣誉", widget=forms.Textarea, required=False)
    contact = forms.CharField(label="联系方式", widget=forms.Textarea, required=False)
    other = forms.CharField(label="备注", widget=forms.Textarea, required=False)

class CourseForm(forms.Form):
    name = forms.CharField(label="课程名称", max_length=50)
    plan = forms.CharField(label="教学计划", widget=forms.Textarea, required=False)
    book = forms.CharField(label="教材", widget=forms.Textarea, required=False)
    background = forms.CharField(label="教材", widget=forms.Textarea, required=False)
    exam = forms.CharField(label="考核方式", widget=forms.Textarea, required=False)
    knowledge = forms.CharField(label="前置知识", widget=forms.Textarea, required=False)
    project = forms.CharField(label="大作业", widget=forms.Textarea, required=False)

class NotificationForm(forms.Form):
    operation = forms.CharField(widget=forms.HiddenInput(), required=False)
    course = forms.ModelChoiceField(label="课程", queryset=Course.objects.all())
    clazz = forms.ModelChoiceField(label="班级", queryset=Class.objects.all())
    title = forms.CharField(label="标题", max_length=50)
    content = forms.CharField(label="内容", widget=forms.Textarea)

class ArticleForm(forms.ModelForm):
    '''
    operation = forms.CharField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(label="标题", max_length=50)
    content = forms.CharField(label="内容", widget=forms.Textarea)
    attached_file = forms.FileField(required=False)
    '''
    class Meta:
        model = Article
        fields = ['teacher', 'title', 'content', 'attached_file', 'pub_date']
        widgets = {'teacher': forms.HiddenInput(),
                'pub_date': forms.HiddenInput(),
                }
