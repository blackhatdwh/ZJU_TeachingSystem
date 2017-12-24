from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^course_description/(?P<course_id>[0-9]+)/$', views.course_description, name='course_description'),
    url(r'^teacher_description/(?P<user_id>[0-9]+)/$', views.teacher_description, name='teacher_description'),
    url(r'^article/(?P<article_id>[0-9]+)', views.article_detail, name='article_detail'),
    url(r'^notification/(?P<notification_id>[0-9]+)/$', views.notification_detail, name='notification_detail'),
    url(r'modify_teacher_description/$', views.modify_teacher_description, name='modify_teacher_description'),
    url(r'modify_course_description/(?P<course_id>[0-9]+)/$', views.modify_course_description, name='modify_course_description'),
    url(r'^teacher/$', views.teacher_index, name='teacher_index'),
    url(r'^teacher/class/(?P<class_id>[0-9]+)/$', views.teacher_my_class, name='teacher_class'),
    url(r'^teacher/homework/(?P<homework_id>[0-9]+)/$', views.teacher_check_homework, name='teacher_check_homework'),
    url(r'^teacher/homework/check/(?P<homework_id>[0-9]+)/$', views.teacher_check_detail, name='teacher_check_detail'),

    url(r'^student/$', views.student_index, name='student_index'),
    url(r'^student/class/(?P<class_id>[0-9]+)/$', views.student_my_class, name='student_class'),
    url(r'^student/homework/(?P<homework_id>[0-9]+)/$', views.student_homework, name='student_homework'),

    url(r'^guest/$', views.guest_index, name='guest_index'),

]
