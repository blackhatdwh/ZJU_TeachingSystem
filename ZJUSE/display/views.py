from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import *

from statistics import mean
import datetime, os, csv, json
from .utils import GenerateDate, GenerateCourseAndClassDict, homework_status



# Create your views here.


def log_in(request):
    # post
    if request.method == 'POST':
        form = NamePass(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('guest_index')+'?fail')
    return redirect(reverse('index'))

#done
def log_out(request):
    logout(request)
    return redirect(reverse('index'))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePass(request.POST)
        if form.is_valid():
            old_passwd = form.cleaned_data['old_passwd']
            new_passwd_1 = form.cleaned_data['new_passwd_1']
            new_passwd_2 = form.cleaned_data['new_passwd_2']
            if check_password(old_passwd, request.user.password):
                if new_passwd_1 == new_passwd_2:
                    request.user.set_password(new_passwd_1)
                    request.user.save()
                    return redirect(reverse('logout'))
                else:
                    return HttpResponse(r"<script>alert('两次密码不同!');</script>")
            else:
                return HttpResponse(r"<script>alert('旧密码错误!');</script>")
        else:
            return HttpResponse(r"<script>alert('failed!');</script>")
        return redirect(reverse('index'))
    else:
        form = ChangePass()
        context = {
                'form': form,
                }
        return render(request, 'display/change_password.html', context)

@login_required
def set_password_question(request):
    if request.method == 'POST':
        form = PasswordQuestionForm(request.POST)
        if form.is_valid():
            request.user.profile.question = PasswordQuestion.objects.get(question=form.cleaned_data['question'])
            request.user.profile.answer = form.cleaned_data['answer']
            request.user.profile.save()
        else:
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Add succeeded!')
    else:
        form = PasswordQuestionForm()
        context = {
            'form': form,
        }
        return render(request, 'display/set_password_question.html', context)

@login_required
def change_password_using_question(request):
    if request.method == 'POST':
        form = ChangePassUsingQuestion(request.POST)
        if form.is_valid():
            if request.user.profile.question == PasswordQuestion.objects.get(question=form.cleaned_data['question']):
                if request.user.profile.answer == form.cleaned_data['answer']:
                    if form.cleaned_data['new_passwd_1'] == form.cleaned_data['new_passwd_2']:
                        request.user.set_password(form.cleaned_data['new_passwd_1'])
                        return redirect(reverse('logout'))
        return HttpResponse('<script>alert("failed!");</script>')
    else:
        form = ChangePassUsingQuestion()
        context = {
            'form': form,
        }
        return render(request, 'display/change_password_using_question.html', context)



#done
def index(request):
    if request.user.is_authenticated() and request.user.profile.answer == '':
        return redirect(reverse('set_password_question'))
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        return redirect(reverse('teacher_index'))
    elif request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        return redirect(reverse('student_index'))
    else:
        return redirect(reverse('guest_index'))
    
#done
def teacher_index(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        notification_set = Notification.objects.filter(publisher=teacher).order_by('-pub_date')
        teaches_set = Teaches.objects.filter(teacher=teacher)
        class_set = set()
        for teaches in teaches_set:
            class_set.add(teaches.clazz)
        homework_set = Homework.objects.filter(clazz__in=class_set).order_by('-pub_date')
        for homework in homework_set:
            unchecked_set = Finish.objects.filter(homework=homework, checked=False)
            checked_set = Finish.objects.filter(homework=homework, checked=True)
            if timezone.localtime(timezone.now()) < homework.ddl:
                homework.check_status = '尚未截止'
            elif len(unchecked_set) == 0:
                homework.check_status = '批改完成'
            elif len(checked_set) == 0:
                homework.check_status = '未批改'
            else:
                homework.check_status = '未批改完成'
        article_set = Article.objects.filter(teacher=teacher).order_by('-pub_date')

        message = request.get_full_path().split('?')[-1]

        context = {
            'teacher': teacher,
            'notification_set': notification_set,
            'class_set': class_set,
            'homework_set': homework_set,
            'article_set': article_set,
            'message': message,
        }
        return render(request, 'display/teacher_index.html', context)
    else:
        #you are not a teacher!
        return redirect(reverse('index'))

#done
def teacher_my_class(request, class_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        clazz = Class.objects.get(id=class_id)
        course = clazz.course
        notification_set = Notification.objects.filter(clazz=clazz)
        homework_set = Homework.objects.filter(clazz=clazz)
        resource_set = Resource.objects.filter(course=course)
        context = {
                'class': clazz,
                'notification_set': notification_set,
                'homework_set': homework_set,
                'resource_set': resource_set,
                'teacher': teacher,
                }
        return render(request, 'display/teacher_my_class.html', context)
    else:
        #you are not a teacher!
        return redirect(reverse('index'))

@login_required
def add_homework(request):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        return redirect(reverse('index'))
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['pub_date'] = timezone.localtime(timezone.now())
        request.POST['ddl'] = GenerateDate(request.POST)

        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
            #return HttpResponse('<script>alert("failed!");</script>')
        newly_added_homework = Homework.objects.order_by('-id').first()
        clazz = newly_added_homework.clazz
        join_set = Join.objects.filter(clazz=clazz)
        for join in join_set:
            finish = Finish(student=join.student, homework=newly_added_homework)
            finish.save()
        #return HttpResponse('Add succeeded!')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'pub_date': None,
                'ddl': None,
                }
        form = HomeworkForm(initial=initial)
        course_and_class_dict = GenerateCourseAndClassDict(teacher)
        context = {
            'teacher': teacher,
            'form': form,
            'course_and_class_dict': json.dumps(course_and_class_dict),
        }
        return render(request, 'display/add_homework.html', context)

@login_required
def modify_homework(request, homework_id):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        return redirect(reverse('index'))
    homework = Homework.objects.get(id=homework_id)
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['pub_date'] = timezone.localtime(timezone.now())
        request.POST['ddl'] = GenerateDate(request.POST)

        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework.clazz = form.cleaned_data['clazz']
            homework.title = form.cleaned_data['title']
            homework.content = form.cleaned_data['content']
            try:
                homework.attached_file = request.FILES['attached_file']
            except:
                pass
            homework.pub_date = form.cleaned_data['pub_date']
            homework.weight = form.cleaned_data['weight']
            homework.ddl = form.cleaned_data['ddl']
            homework.save()
        else:
            #return HttpResponse('<script>alert("failed!");</script>')
            return redirect(reverse('teacher_index')+'?fail')
        #return HttpResponse('Add succeeded!')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'clazz': homework.clazz,
                'title': homework.title,
                'content': homework.content,
                'attached_file': homework.attached_file,
                'weight': homework.weight,
                'ddl': homework.ddl,
                'ddl_date': homework.ddl.date,
                'ddl_time': homework.ddl.time,
                }
        form = HomeworkForm(initial=initial)
        context = {
            'form': form,
            'homework': homework,
        }
        return render(request, 'display/modify_homework.html', context)


@login_required
def delete_homework(request, homework_id):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        return redirect(reverse('index'))
    homework = Homework.objects.get(id=homework_id)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm'] == 'True':
                homework.delete()
        else:
            #return HttpResponse('<script>alert("failed!");</script>')
            return redirect(reverse('teacher_index')+'?fail')
        #return HttpResponse('Add succeeded!')
        return redirect(reverse('teacher_index')+'?success')
    else:
        form = DeleteForm(initial={'confirm': 'True'})
        context = {
            'form': form,
            'homework': homework,
        }
        return render(request, 'display/delete_homework.html', context)


#done
def teacher_check_homework(request, homework_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        homework = Homework.objects.get(id=homework_id)
        finished_set = Finish.objects.filter(homework=homework).exclude(upload_time__isnull=True)
        unfinished_set = Finish.objects.filter(homework=homework, upload_time__isnull=True)
        context = {
                'homework': homework,
                'finished_set': finished_set,
                'unfinished_set': unfinished_set,
                'teacher': teacher,
                }
        return render(request, 'display/teacher_check_homework.html', context)
    else:
        #you are not a teacher
        return redirect(reverse('index'))

#done
@login_required
def teacher_check_detail(request, finish_id):
    if request.user.groups.all().first().name == 'Teacher':
        finish = Finish.objects.get(id=finish_id)
    else:
        #you are not a teacher
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = TeacherCheckHomework(request.POST)
        if form.is_valid():
            finish.score = int(form.cleaned_data['score'])
            finish.evaluation = form.cleaned_data['evaluation']
            finish.checked = True
            finish.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        teacher = Teacher.objects.get(user=request.user)
        initial = {
                'score': finish.score,
                'evaluation': finish.evaluation,
                }
        form = TeacherCheckHomework(initial=initial)
        context = {
                'student': finish.student,
                'finish': finish,
                'form': form,
                'teacher': teacher,
                }
        return render(request, 'display/teacher_check_detail.html', context)

def notification_detail(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if request.user == notification.publisher.user:
        authority = True
    else:
        authority = False
    return render(request, 'display/notification_detail.html', {'notification': notification, 'authority': authority})

def add_notification(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            clazz = form.cleaned_data['clazz']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            new_notification = Notification(clazz=clazz, title=title, content=content, pub_date=timezone.localtime(timezone.now()), publisher=teacher)
            new_notification.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        form = NotificationForm()
        course_and_class_dict = GenerateCourseAndClassDict(teacher)
        context = {
            'form': form,
            'teacher': teacher,
            'course_and_class_dict': json.dumps(course_and_class_dict),
        }
        return render(request, 'display/add_notification.html', context)

def modify_notification(request, notification_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        notification = Notification.objects.get(id=notification_id)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification.clazz = form.cleaned_data['clazz']
            notification.title = form.cleaned_data['title']
            notification.content = form.cleaned_data['content']
            notification.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'clazz': notification.clazz,
                'title': notification.title,
                'content': notification.content,
                }
        form = NotificationForm(initial=initial)
        course_and_class_dict = GenerateCourseAndClassDict(teacher)
        context = {
            'form': form,
            'teacher': teacher,
            'notification': notification,
            'course_and_class_dict': json.dumps(course_and_class_dict),
        }
        return render(request, 'display/modify_notification.html', context)

def delete_notification(request, notification_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    notification = Notification.objects.get(id=notification_id)
    if notification.publisher != teacher:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm'] == 'True':
                notification.delete()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        form = DeleteForm(initial={'confirm': 'True'})
        context = {
            'form': form,
            'notification': notification,
        }
        return render(request, 'display/delete_notification.html', context)

def resource_detail(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    if request.user.is_authenticated():
        access_authority = True
    else:
        access_authority = False
    if resource.uploader.user == request.user:
        modify_authority = True
    else:
        modify_authority = False
    context = {
            'access_authority': access_authority,
            'modify_authority': modify_authority,
            'resource': resource,
            }
    return render(request, 'display/resource_detail.html', context)



@login_required
def add_resource(request, course_id):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['pub_date'] = timezone.localtime()
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'course': course,
                'pub_date': None,
                'uploader': teacher,
                }
        form = ResourceForm(initial=initial)
        context = {
            'form': form,
            'course': course,
        }
        return render(request, 'display/add_resource.html', context)


@login_required
def modify_resource(request, resource_id):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    resource = Resource.objects.get(id=resource_id)
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['pub_date'] = timezone.localtime()
        form = ResourceForm(request.POST, request.FILES, required=False)
        if form.is_valid():
            resource.course = form.cleaned_data['course']
            resource.title = form.cleaned_data['title']
            resource.description = form.cleaned_data['description']
            try:
                resource.attached_file = request.FILES['attached_file']
            except:
                pass
            resource.pub_date = form.cleaned_data['pub_date']
            resource.uploader = form.cleaned_data['uploader']
            try:
                resource.simple_file = request.FILES['simple_file']
            except:
                resource.simple_file = None
            resource.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'course': resource.course,
                'title': resource.title,
                'description': resource.description,
                'attached_file': resource.attached_file,
                'simple_file': resource.simple_file,
                'pub_date': resource.pub_date,
                'uploader': teacher,
                }
        form = ResourceForm(initial=initial)
        context = {
            'form': form,
            'resource': resource,
        }
        return render(request, 'display/modify_resource.html', context)

@login_required
def delete_resource(request, resource_id):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    resource = Resource.objects.get(id=resource_id)
    if resource.uploader != teacher:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm'] == 'True':
                resource.delete()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        form = DeleteForm(initial={'confirm': 'True'})
        context = {
            'form': form,
            'resource': resource,
        }
        return render(request, 'display/delete_resource.html', context)

#partly done
def student_index(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        join_set = Join.objects.filter(student=student)
        class_set = set()
        for join in join_set:
            class_set.add(join.clazz)
        notification_set = Notification.objects.filter(clazz__in=class_set).order_by('-pub_date')
        homework_set = Homework.objects.filter(clazz__in=class_set).order_by('-pub_date')
        for h in homework_set:
            h = homework_status(student, h)
        article_set = Article.objects.all().order_by('-pub_date')
        message = request.get_full_path().split('?')[-1]
        context = {
            'student': student,
            'notification_set': notification_set,
            'class_set': class_set,
            'homework_set': homework_set,
            'article_set': article_set,
            'message': message,
        }
        return render(request, 'display/student_index.html', context)
    else:
        return redirect(reverse('index'))

#done
def student_my_class(request, class_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        requested_clazz = Class.objects.get(id=class_id)
        course = requested_clazz.course
        join_set = Join.objects.filter(student=student)
        this_students_class_set = set()
        for join in join_set:
            this_students_class_set.add(join.clazz)
        if requested_clazz in this_students_class_set:
            notification_set = Notification.objects.filter(clazz=requested_clazz).order_by('-pub_date')
            homework_set = Homework.objects.filter(clazz=requested_clazz)
            for h in homework_set:
                h = homework_status(student, h)
            finish_set = Finish.objects.filter(student=student, homework__in=homework_set)
            homework_average_score = 0
            for f in finish_set:
                homework_average_score += f.score * f.homework.weight
            homework_average_score /= len(finish_set)
            resource_set = Resource.objects.filter(course=course).order_by('-pub_date')
            context = {
                    'class': requested_clazz,
                    'notification_set': notification_set,
                    'homework_set': homework_set,
                    'homework_average_score': homework_average_score,
                    'resource_set': resource_set,
                    'student': student,
                    }
            return render(request, 'display/student_my_class.html', context)
        else:
            #you are not in this class!
            return student_others_class(request, class_id)
    else:
        #you are not a student!
        return redirect(reverse('index'))

#done
def student_others_class(request, class_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        clazz = Class.objects.get(id=class_id)
        course = clazz.course
        resource_set = Resource.objects.filter(course=course)
        context = {
                'class': clazz,
                'resource_set': resource_set,
                'student': student,
                }
        return render(request, 'display/student_others_class.html', context)
    else:
        #you are not a student!
        return redirect(reverse('index'))

#partly done
def student_view_homework(request, homework_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        homework = Homework.objects.get(id=homework_id)
        homework = homework_status(student, homework)
        this_homeworks_clazz = homework.clazz
        join_set = Join.objects.filter(student=student)
        this_students_class_set = set()
        for join in join_set:
            this_students_class_set.add(join.clazz)
        if this_homeworks_clazz in this_students_class_set:
            finish_set = Finish.objects.filter(homework=homework)
            score_list = []
            for f in finish_set:
                score_list.append(f.score)
            score_list.sort(reverse=True)
            this_student_finish = Finish.objects.get(student=student, homework=homework)
            try:
                average_score = mean(score_list)
                rank = score_list.index(this_student_finish.score) + 1
            # len(score_list)=0
            except TypeError:
                average_score = 0
                rank = 0

            initial = {
                    'student': student,
                    'homework': homework,
                    'upload_time': None,
                    }
            form = StudentUploadHomeworkForm(initial=initial)
            context = {
                    'class': homework.clazz,
                    'homework': homework,
                    'finish': this_student_finish,
                    'average_score': average_score,
                    'rank': rank,
                    'total': len(score_list),
                    'form': form,
                    'student': student,
                    }
            return render(request, 'display/student_view_homework.html', context)
    else:
        return redirect(reverse('index'))

@login_required
def student_upload_homework(request, finish_id):
    student = Student.objects.get(user=request.user)
    finish = Finish.objects.get(id=finish_id)
    if finish.student != student:
        return redirect(reverse('index'))
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['upload_time'] = timezone.localtime(timezone.now())
        form = StudentUploadHomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            finish.upload_file = request.FILES['upload_file']
            finish.upload_time = request.POST['upload_time']
            finish.checked = False
            finish.save()
        else:
            return redirect(reverse('student_index')+'?fail')
        return redirect(reverse('student_index')+'?success')
    else:
        return redirect(reverse('index'))


#partly done
def guest_index(request):
    if not request.user.is_authenticated():
        teacher_set = Teacher.objects.all()
        form = NamePass()
        course_set = Course.objects.all()
        message = request.get_full_path().split('?')[-1]
        context = {
            'course_set': course_set,
            'teacher_set': teacher_set,
            'form': form,
            'message': message,
        }
        return render(request, 'display/guest_index.html', context)
    else:
        return redirect(reverse('index'))

#done
def teacher_description(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teaches_set = Teaches.objects.filter(teacher=teacher)
    class_set = set()
    article_set = Article.objects.filter(teacher=teacher)
    for teaches in teaches_set:
        class_set.add(teaches.clazz)
    context = {
            'teacher': teacher,
            'class_set': class_set,
            'article_set': article_set,
            }
    return render(request, 'display/teacher_description.html', context)

@login_required
def modify_teacher_description(request):
    if request.user.groups.all().first().name != 'Teacher':
        return redirect(reverse('index'))
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher.name = form.cleaned_data['name']
            teacher.experience= form.cleaned_data['experience']
            teacher.research= form.cleaned_data['research']
            teacher.style= form.cleaned_data['style']
            teacher.publication= form.cleaned_data['publication']
            teacher.honor= form.cleaned_data['honor']
            teacher.contact= form.cleaned_data['contact']
            teacher.other= form.cleaned_data['other']
            teacher.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'name': teacher.name, 'experience': teacher.experience, 'research': teacher.research, 'style': teacher.style,
                'publication': teacher.publication, 'honor': teacher.honor, 'contact': teacher.contact, 'other': teacher.other,
                }
        form = TeacherForm(initial=initial)
        context = {
            'form': form,
            'teacher': teacher,
        }
        return render(request, 'display/modify_teacher_description.html', context)

#done
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.is_authenticated():
        resource_set = Resource.objects.filter(course=course)
    else:
        resource_set = Resource.objects.filter(course=course).exclude(simple_file__isnull=True)
    class_set = Class.objects.filter(course=course)
    teacher_and_class_list = []
    for clazz in class_set:
        teacher_set = set()
        teaches_set = Teaches.objects.filter(clazz=clazz)
        for teaches in teaches_set:
            teacher_set.add(teaches.teacher)
        teacher_and_class_list.append([teacher_set, clazz])

    add_resource_authority = False
    try:
        if request.user.groups.all().first().name == 'Teacher':
            add_resource_authority = True
    except:
        pass

    context = {
            'course': course,
            'resource_set': resource_set,
            'teacher_and_class_list': teacher_and_class_list,
            'add_resource_authority': add_resource_authority,
            }
    return render(request, 'display/course_detail.html', context)

@login_required
def modify_course(request, course_id):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course.name = form.cleaned_data['name']
            course.plan = form.cleaned_data['plan']
            course.book = form.cleaned_data['book']
            course.background = form.cleaned_data['background']
            course.exam = form.cleaned_data['exam']
            course.knowledge = form.cleaned_data['knowledge']
            course.project = form.cleaned_data['project']
            course.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'name': course.name,
                'plan': course.name,
                'book': course.book,
                'background': course.background,
                'exam': course.exam,
                'knowledge': course.knowledge,
                'project': course.project,
                }
        form = CourseForm(initial=initial)
        context = {
            'form': form,
            'course': course,
        }
        print(form)
        return render(request, 'display/modify_course.html', context)

#done
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.teacher.user == request.user:
        authority = True
    else:
        authority = False
    return render(request, 'display/article_detail.html', {'article': article, 'authority': authority})

def add_article(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['pub_date'] = timezone.localtime(timezone.now())
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        form = ArticleForm(initial={'teacher': teacher})
        context = {
            'form': form,
            'teacher': teacher,
        }
        return render(request, 'display/add_article.html', context)

def modify_article(request, article_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    article = Article.objects.get(id=article_id)
    if article.teacher != teacher:
        return redirect(reverse('index'))

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['pub_date'] = timezone.localtime(timezone.now())
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.pub_date = form.cleaned_data['pub_date']
            try:
                article.attached_file = request.FILES['attached_file']
            except:
                pass
            article.save()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        initial = {
                'teacher': article.teacher, 'title': article.title, 'content': article.content,
                'attached_file': article.attached_file, 'pub_date': article.pub_date,
                }
        form = ArticleForm(initial=initial)
        context = {
            'form': form, 'teacher': teacher, 'article': article,
        }
        return render(request, 'display/modify_article.html', context)

def delete_article(request, article_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    article = Article.objects.get(id=article_id)
    if article.teacher != teacher:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm'] == 'True':
                article.delete()
        else:
            return redirect(reverse('teacher_index')+'?fail')
        return redirect(reverse('teacher_index')+'?success')
    else:
        form = DeleteForm(initial={'confirm': 'True'})
        context = {
            'form': form,
            'teacher': teacher,
            'article': article,
        }
        return render(request, 'display/delete_article.html', context)

@login_required
def teacher_course_list(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        course_set = Course.objects.all()
        context = {
                'teacher': teacher,
                'course_set': course_set, 
                }
        return render(request, 'display/teacher_course_list.html', context)
    else:
        return redirect(reverse('index'))

@login_required
def student_course_list(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        course_set = Course.objects.all()
        context = {
                'student': student,
                'course_set': course_set, 
                }
        return render(request, 'display/student_course_list.html', context)
    else:
        return redirect(reverse('index'))

def guest_course_list(request):
    course_set = Course.objects.all()
    form = NamePass()
    context = {
            'course_set': course_set, 
            'form': form,
            }
    return render(request, 'display/guest_course_list.html', context)

@login_required
def teacher_teacher_list(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        teacher_set = Teacher.objects.all()
        context = {
                'teacher': teacher,
                'teacher_set': teacher_set, 
                }
        return render(request, 'display/teacher_teacher_list.html', context)
    else:
        return redirect(reverse('index'))

@login_required
def student_teacher_list(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        teacher_set = Teacher.objects.all()
        context = {
                'student': student,
                'teacher_set': teacher_set, 
                }
        return render(request, 'display/student_teacher_list.html', context)
    else:
        return redirect(reverse('index'))

def guest_teacher_list(request):
    teacher_set = Teacher.objects.all()
    form = NamePass()
    context = {
            'teacher_set': teacher_set, 
            'form': form,
            }
    return render(request, 'display/guest_teacher_list.html', context)

@login_required
def teacher_notification_list(request):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        notification_set = Notification.objects.filter(publisher=teacher).order_by('-pub_date')
        context = {
                'notification_set': notification_set, 
                'teacher': teacher,
        }
        return render(request, 'display/teacher_notification_list.html', context)
    else:
        return redirect(reverse('index'))

@login_required
def student_notification_list(request):
    if request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        join_set = Join.objects.filter(student=student)
        class_set = set()
        for join in join_set:
            class_set.add(join.clazz)
        notification_set = Notification.objects.filter(clazz__in=class_set).order_by('-pub_date')
    context = {
            'notification_set': notification_set, 
            'student': student,
    }
    return render(request, 'display/student_notification_list.html', context)

@login_required
def teacher_homework_list(request):
    if request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        teaches_set = Teaches.objects.filter(teacher=teacher)
        class_set = set()
        for teaches in teaches_set:
            class_set.add(teaches.clazz)
        homework_set = Homework.objects.filter(clazz__in=class_set).order_by('-pub_date')
        for homework in homework_set:
            unchecked_set = Finish.objects.filter(homework=homework, checked=False)
            checked_set = Finish.objects.filter(homework=homework, checked=True)
            if timezone.localtime(timezone.now()) < homework.ddl:
                homework.check_status = '尚未截止'
            elif len(unchecked_set) == 0:
                homework.check_status = '批改完成'
            elif len(checked_set) == 0:
                homework.check_status = '未批改'
            else:
                homework.check_status = '未批改完成'
        user = teacher
        is_teacher = True
        context = {
                'homework_set': homework_set, 
                'teacher': teacher,
                }
        return render(request, 'display/teacher_homework_list.html', context)

@login_required
def student_homework_list(request):
    if request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        join_set = Join.objects.filter(student=student)
        class_set = set()
        for join in join_set:
            class_set.add(join.clazz)
        homework_set = Homework.objects.filter(clazz__in=class_set).order_by('-pub_date')
        for h in homework_set:
            h = homework_status(student, h)
        context = {
                'homework_set': homework_set, 
                'student': student,
                }
        return render(request, 'display/student_homework_list.html', context)
    else:
        return redirect(reverse('index'))

@login_required
def teacher_article_list(request):
    if request.user.groups.all().first().name == 'Teacher':
        article_set = Article.objects.all()
        teacher = Teacher.objects.get(user=request.user)
        context = {
                'article_set': article_set,
                'teacher': teacher,
                }
        return render(request, 'display/teacher_article_list.html', context)
    else:
        return redirect(reverse('index'))

@login_required
def student_article_list(request):
    if request.user.groups.all().first().name == 'Student':
        article_set = Article.objects.all().order_by('-pub_date')
        student = Student.objects.get(user=request.user)
        context = {
                'article_set': article_set,
                'student': student,
                }
        return render(request, 'display/student_article_list.html', context)
    else:
        return redirect(reverse('index'))

def guest_article_list(request):
    article_set = Article.objects.all()
    form = NamePass()
    context = {
            'article_set': article_set,
            'form': form,
            }
    return render(request, 'display/guest_article_list.html', context)

def add_student_to_system(request):
    if not request.user.is_superuser:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = AddStudentToSystemForm(request.POST, request.FILES)
        if form.is_valid():
            namelist = request.FILES['namelist']
            with open('namelist.csv', 'wb') as f:
                for chunk in namelist.chunks():
                    f.write(chunk)
            with open('namelist.csv', 'r') as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                for row in reader:
                    name = row[0].strip()
                    school_id = row[1].strip()
                    user = User.objects.create_user(school_id, password='123456')
                    user.save()
                    Group.objects.get(name='Student').user_set.add(user)
                    student = Student(user=user, name=name)
                    student.save()
            os.system('rm namelist.csv')

        else:
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Add succeeded!')
    else:
        form = AddStudentToSystemForm()
        context = {
            'form': form,
        }
        return render(request, 'display/add_student_to_system.html', context)

def add_student_to_class(request):
    if not request.user.is_superuser:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = AddStudentToClassForm(request.POST, request.FILES)
        if form.is_valid():
            namelist = request.FILES['namelist']
            clazz = form.cleaned_data['clazz']
            try:
                homework_set = Homework.objects.filter(clazz=clazz)
            except:
                homework_set = set()
            with open('namelist.csv', 'wb') as f:
                for chunk in namelist.chunks():
                    f.write(chunk)
            with open('namelist.csv', 'r') as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                for row in reader:
                    school_id = row[0].strip()
                    student = Student.objects.get(user__username=school_id)
                    join = Join(student=student, clazz=clazz)
                    join.save()
                    for homework in homework_set:
                        finish = Finish(student=student, homework=homework)
                        finish.save()
            os.system('rm namelist.csv')

        else:
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Add succeeded!')
    else:
        form = AddStudentToClassForm()
        context = {
            'form': form,
        }
        return render(request, 'display/add_student_to_class.html', context)
