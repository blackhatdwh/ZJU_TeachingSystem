from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import *

from statistics import mean
import datetime

def homework_status(student, homework):
    homework.status = 'normal'
    if Finish.objects.filter(student=student, homework=homework).exclude(upload_time__isnull=True).count() == 0:
        homework.status = 'done'
    elif homework.ddl - timezone.localtime(timezone.now()) < datetime.timedelta(hours=12) and timezone.localtime(timezone.now()) < homework.ddl:
        homework.status = 'emergency'
    if timezone.localtime(timezone.now()) > homework.ddl:
        homework.status = 'disabled'
    return homework


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
                return HttpResponse(r"<script>alert('failed!');</script>")
    return redirect(reverse('index'))

#done
def log_out(request):
    logout(request)
    return redirect(reverse('index'))

#done
def index(request):
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
        notification_set = Notification.objects.filter(publisher=teacher)
        teaches_set = Teaches.objects.filter(teacher=teacher)
        class_set = set()
        for teaches in teaches_set:
            class_set.add(teaches.clazz)
        homework_set = Homework.objects.filter(clazz__in=class_set)
        for homework in homework_set:
            unchecked_set = Finish.objects.filter(homework=homework, score__isnull=True)
            checked_set = Finish.objects.filter(homework=homework).exclude(score__isnull=True)
            if len(unchecked_set) == 0:
                homework.check_status = '批改完成'
            elif len(checked_set) == 0:
                homework.check_status = '未批改'
            else:
                homework.check_status = '未批改完成'
        article_set = Article.objects.filter(teacher=teacher)

        context = {
            'teacher': teacher,
            'notification_set': notification_set,
            'class_set': class_set,
            'homework_set': homework_set,
            'article_set': article_set,
        }
        return render(request, 'display/teacher_index.html', context)
    else:
        #you are not a teacher!
        return redirect(reverse('index'))

#done
def teacher_my_class(request, class_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
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
                }
        return render(request, 'display/teacher_my_class.html', context)
    else:
        #you are not a teacher!
        return redirect(reverse('index'))

#done
def teacher_check_homework(request, homework_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        homework = Homework.objects.get(id=homework_id)
        finished_set = Finish.objects.filter(homework=homework).exclude(upload_time__isnull=True)
        unfinished_set = Finish.objects.filter(homework=homework, upload_time__isnull=True)
        context = {
                'class': homework.clazz,
                'finished_set': finished_set,
                'unfinished_set': unfinished_set,
                }
        return render(request, 'display/teacher_check_homework.html', context)
    else:
        #you are not a teacher
        return redirect(reverse('index'))

#done
def teacher_check_detail(request, finish_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        finish = Finish.objects.get(id=finish_id)
        context = {
                'student': finish.student,
                'finish': finish,
                }
        return render(request, 'display/teacher_check_detail.html', context)
    else:
        #you are not a teacher
        return redirect(reverse('index'))

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
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Add succeeded!')
    else:
        form = NotificationForm(initial={'operation': 'add'})
        context = {
            'form': form,
            'teacher': teacher,
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
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Modify succeeded!')
    else:
        initial = {
                'operation': 'modify',
                'clazz': notification.clazz,
                'title': notification.title,
                'content': notification.content,
                }
        form = NotificationForm(initial=initial)
        context = {
            'form': form,
            'teacher': teacher,
            'notification': notification,
        }
        return render(request, 'display/modify_notification.html', context)

def delete_notification(request, notification_id):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
        notification = Notification.objects.get(id=notification_id)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['operation'] == 'delete':
                notification.delete()
        else:
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('delete succeeded!')
    else:
        initial = {
                'operation': 'delete',
                'course': notification.clazz.course,
                'clazz': notification.clazz,
                'title': notification.title,
                'content': notification.content,
                }
        form = NotificationForm(initial=initial)
        context = {
            'form': form,
            'notification': notification,
        }
        return render(request, 'display/delete_notification.html', context)



#partly done
def student_index(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
        student = Student.objects.get(user=request.user)
        join_set = Join.objects.filter(student=student)
        class_set = set()
        for join in join_set:
            class_set.add(join.clazz)
        notification_set = Notification.objects.filter(clazz__in=class_set)
        homework_set = Homework.objects.filter(clazz__in=class_set)
        for h in homework_set:
            h = homework_status(student, h)
        article_set = Article.objects.all()
        context = {
            'student': student,
            'notification_set': notification_set,
            'class_set': class_set,
            'homework_set': homework_set,
            'article_set': article_set,
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
            notification_set = Notification.objects.filter(clazz=requested_clazz)
            homework_set = Homework.objects.filter(clazz=requested_clazz)
            for h in homework_set:
                h = homework_status(student, h)
            finish_set = Finish.objects.filter(student=student, homework__in=homework_set)
            homework_average_score = 0
            for f in finish_set:
                homework_average_score += f.score * f.homework.weight
            homework_average_score /= len(finish_set)
            resource_set = Resource.objects.filter(course=course)
            context = {
                    'class': requested_clazz,
                    'notification_set': notification_set,
                    'homework_set': homework_set,
                    'homework_average_score': homework_average_score,
                    'resource_set': resource_set,
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
        resource_set = Resource.objects.filter(course=clazz__course)
        context = {
                'class': clazz,
                'resource_set': resource_set,
                }
        return render(request, 'display/student_others_class.html', context)
    else:
        #you are not a student!
        return redirect(reverse('index'))

#partly done
def student_homework(request, homework_id):
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
            this_student_finish = Finish.objects.get(student=student)
            try:
                average_score = mean(score_list)
                rank = score_list.index(this_student_finish.score) + 1
            # len(score_list)=0
            except TypeError:
                average_score = 0
                rank = 0
            context = {
                    'class': homework.clazz,
                    'homework': homework,
                    'finish': this_student_finish,
                    'average_score': average_score,
                    'rank': rank,
                    'total': len(score_list)
                    }
            return render(request, 'display/student_view_homework.html', context)
    else:
        return redirect(reverse('index'))


#partly done
def guest_index(request):
    if not request.user.is_authenticated():
        teacher_set = Teacher.objects.all()
        form = NamePass()
        course_set = Course.objects.all()
        context = {
            'course_set': course_set,
            'teacher_set': teacher_set,
            'form': form,
        }
        return render(request, 'display/guest_index.html', context)
    else:
        return redirect(reverse('index'))

#done
def teacher_description(request, user_id):
    teacher = Teacher.objects.get(user__id=user_id)
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
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Modify succeeded!')
    else:
        initial = {
                'name': teacher.name,
                'experience': teacher.experience,
                'research': teacher.research,
                'style': teacher.style,
                'publication': teacher.publication,
                'honor': teacher.honor,
                'contact': teacher.contact,
                'other': teacher.other,
                }
        form = TeacherForm(initial=initial)
        context = {
            'form': form,
            'teacher': teacher,
        }
        return render(request, 'display/modify_teacher_description.html', context)

#done
def course_description(request, course_id):
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
    context = {
            'course': course,
            'resource_set': resource_set,
            'teacher_and_class_list': teacher_and_class_list,
            }
    return render(request, 'display/course_description.html', context)

@login_required
def modify_course_description(request, course_id):
    course = Course.objects.get(id=course_id)
    class_set = Class.objects.filter(course=course)
    teaches_set = Teaches.objects.filter(clazz__in=class_set)
    teacher_set = set()
    # all teachers who teaches this course
    for teaches in teaches_set:
        teacher_set.add(teaches.teacher)
    # if the request user does not teaches this course, redirect
    for teacher in teacher_set:
        if request.user == teacher.user:
            return HttpResponse("<script>alert('yes you can!')</script>")
            break
    return redirect(reverse('index'))

#done
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'display/article_detail.html', {'article': article})

def add_article(request):
    if request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
        teacher = Teacher.objects.get(user=request.user)
    else:
        #you are not a teacher
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #title = form.cleaned_data['title']
            #content = form.cleaned_data['content']
            #new_notification = Notification(clazz=clazz, title=title, content=content, pub_date=timezone.localtime(timezone.now()), publisher=teacher)
            #new_notification.save()
        else:
            return HttpResponse('<script>alert("failed!");</script>')
        return HttpResponse('Add succeeded!')
    else:
        form = ArticleForm(initial={'teacher': teacher, 'pub_date': timezone.localtime(timezone.now())})
        context = {
            'form': form,
            'teacher': teacher,
        }
        return render(request, 'display/add_article.html', context)

#done
def course_list(request):
    course_set = Course.objects.all()
    return render(request, 'display/course_list.html', {'course_set': course_set})

#done
def teacher_list(request):
    teacher_set = Teacher.objects.all()
    return render(request, 'display/teacher_list.html', {'teacher_set': teacher_set})

#done
def notification_detail(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    return render(request, 'display/notification_detail.html', {'notification': notification})

