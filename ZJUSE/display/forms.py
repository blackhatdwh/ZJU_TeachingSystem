from django import forms

class NamePass(forms.Form):
    username = forms.CharField(label="用户名", max_length=100)
    password = forms.CharField(label="密码", max_length=100, widget=forms.PasswordInput())

class TeacherDescription(forms.Form):
    name = forms.CharField(label="姓名", max_length=50)
    experience = forms.CharField(label="教学经历", widget=forms.Textarea)
    research = forms.CharField(label="科研成果", widget=forms.Textarea)
    style = forms.CharField(label="教学风格", widget=forms.Textarea)
    publication = forms.CharField(label="出版作品", widget=forms.Textarea)
    honor = forms.CharField(label="所获荣誉", widget=forms.Textarea)
    contact = forms.CharField(label="联系方式", widget=forms.Textarea)
    other = forms.CharField(label="备注", widget=forms.Textarea)

class CourseDescription(forms.Form):
    name = forms.CharField(max_length=50)
    plan = forms.CharField(widget=forms.Textarea)
    book = forms.CharField(widget=forms.Textarea)
    background = forms.CharField(widget=forms.Textarea)
    exam = forms.CharField(widget=forms.Textarea)
    knowledge = forms.CharField(widget=forms.Textarea)
    project = forms.CharField(widget=forms.Textarea)
