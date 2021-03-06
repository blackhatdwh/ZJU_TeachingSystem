from django import forms
from .models import *
from .utils import TimeSelectorWidget
from datetime import datetime

class DeleteForm(forms.Form):
    confirm = forms.CharField(widget=forms.HiddenInput())

class NamePass(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput())

class ChangePass(forms.Form):
    old_passwd = forms.CharField(label="原密码", widget=forms.PasswordInput())
    new_passwd_1 = forms.CharField(label="新密码", widget=forms.PasswordInput())
    new_passwd_2 = forms.CharField(label="确认密码", widget=forms.PasswordInput())

class PasswordQuestionForm(forms.Form):
    question = forms.ModelChoiceField(label="密保问题", queryset=PasswordQuestion.objects.all())
    answer = forms.CharField(label="答案")

class ChangePassUsingQuestion(forms.Form):
    question = forms.ModelChoiceField(label="密保问题", queryset=PasswordQuestion.objects.all())
    answer = forms.CharField(label="答案")
    new_passwd_1 = forms.CharField(label="新密码", widget=forms.PasswordInput())
    new_passwd_2 = forms.CharField(label="确认密码", widget=forms.PasswordInput())

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['user']
        labels = {
                'name': '姓名', 'experience': '教学经验', 'research': '研究成果', 'style': '教学风格',
                'publication': '出版作品', 'honor': '所获荣誉', 'contact': '联系方式', 'other': '备注',
                }
        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'experience': forms.Textarea(attrs={'class': 'form-control'}),
                'research': forms.Textarea(attrs={'class': 'form-control'}),
                'style': forms.Textarea(attrs={'class': 'form-control'}),
                'publication': forms.Textarea(attrs={'class': 'form-control'}),
                'honor': forms.Textarea(attrs={'class': 'form-control'}),
                'contact': forms.Textarea(attrs={'class': 'form-control'}),
                'other': forms.Textarea(attrs={'class': 'form-control'}),
                }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = []
        labels = {
                'name': '课程名称', 'plan': '教学计划', 'book': '教材', 'background': '国际国内背景',
                'exam': '考核方式', 'knowledge': '前置知识', 'project': '大作业',
                }
        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'plan': forms.Textarea(attrs={'class': 'form-control'}),
                'book': forms.Textarea(attrs={'class': 'form-control'}),
                'background': forms.Textarea(attrs={'class': 'form-control'}),
                'exam': forms.Textarea(attrs={'class': 'form-control'}),
                'knowledge': forms.Textarea(attrs={'class': 'form-control'}),
                'project': forms.Textarea(attrs={'class': 'form-control'}),
                }

class NotificationForm(forms.Form):
    course = forms.ModelChoiceField(label="课程", queryset=Course.objects.all(), required=False)
    clazz = forms.ModelChoiceField(label="班级", queryset=Class.objects.all())
    title = forms.CharField(label="标题", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="内容", widget=forms.Textarea(attrs={'class': 'form-control'}))

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['teacher', 'title', 'content', 'attached_file', 'pub_date']
        widgets = {'teacher': forms.HiddenInput(),
                'pub_date': forms.HiddenInput(),
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'content': forms.Textarea(attrs={'class': 'form-control'}),
                }
        labels = {
                'title':'标题',
                'content':'内容',
                'attached_file':'附件',
                }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude = []
        widgets = {
                'course': forms.HiddenInput(),
                'pub_date': forms.HiddenInput(),
                'uploader': forms.HiddenInput(),
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control'}),
                }
        labels = {
                'title': '标题',
                'description': '简介',
                'attached_file': '文件',
                'simple_file': '简化文件',
                }
    def __init__(self, *args, **kwargs):
        required = True
        try:
            required = kwargs.pop('required')
        except:
            pass
        super(ResourceForm, self).__init__(*args, **kwargs)
        print(required)
        if required == False:
            self.fields['attached_file'].required = False

class HomeworkForm(forms.ModelForm):
    course = forms.ModelChoiceField(label="课程", queryset=Course.objects.all(), required=False)
    ddl_date = forms.DateField(widget=forms.SelectDateWidget)
    ddl_time = forms.TimeField(widget=TimeSelectorWidget())
    class Meta:
        model = Homework
        exclude = []
        widgets = {
                'pub_date': forms.HiddenInput(),
                'ddl': forms.HiddenInput(),
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'content': forms.Textarea(attrs={'class': 'form-control'}),
                'weight': forms.TextInput(attrs={'class': 'form-control'}),
                }
        labels = {
                'clazz': '班级',
                'title': '标题',
                'content': '内容',
                'attached_file': '附件',
                'weight': '权重',
                'ddl_date': '截止时间',
                'ddl_time': '',
                }
    def save(self, commit=True):
        return super(HomeworkForm, self).save(commit=commit)

    
class StudentUploadHomeworkForm(forms.ModelForm):
    class Meta:
        model = Finish
        exclude = ['score', 'evaluation', 'checked']
        widgets = {
                'student': forms.HiddenInput(),
                'homework': forms.HiddenInput(),
                'upload_time': forms.HiddenInput(),
                }

class TeacherCheckHomework(forms.ModelForm):
    class Meta:
        model = Finish
        exclude = ['student', 'homework', 'upload_time', 'upload_file', 'checked']

class AddStudentToSystemForm(forms.Form):
    namelist = forms.FileField()

class AddStudentToClassForm(forms.Form):
    clazz = forms.ModelChoiceField(label="班级", queryset=Class.objects.all())
    namelist = forms.FileField()
