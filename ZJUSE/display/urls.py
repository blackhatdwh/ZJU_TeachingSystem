from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^set_password_question/$', views.set_password_question, name='set_password_question'),
    url(r'^change_password_using_question/$', views.change_password_using_question, name='change_password_using_question'),

    url(r'^add_student_to_system/$', views.add_student_to_system, name='add_student_to_system'),
    url(r'^add_student_to_class/$', views.add_student_to_class, name='add_student_to_class'),

    url(r'^course/(?P<course_id>[0-9]+)/$', views.course_detail, name='course_detail'),
    url(r'^course/(?P<course_id>[0-9]+)/modify/$', views.modify_course, name='modify_course'),
    url(r'^resource/(?P<resource_id>[0-9]+)/$', views.resource_detail, name='resource_detail'),
    url(r'^course/(?P<course_id>[0-9]+)/resource/add/$', views.add_resource, name='add_resource'),
    url(r'^resource/(?P<resource_id>[0-9]+)/modify/$', views.modify_resource, name='modify_resource'),
    url(r'^resource/(?P<resource_id>[0-9]+)/delete/$', views.delete_resource, name='delete_resource'),

    url(r'^teacher_description/(?P<user_id>[0-9]+)/$', views.teacher_description, name='teacher_description'),

    url(r'^article/(?P<article_id>[0-9]+)/$', views.article_detail, name='article_detail'),
    url(r'^article/add/$', views.add_article, name='add_article'),
    url(r'^article/(?P<article_id>[0-9]+)/modify/$', views.modify_article, name='modify_article'),
    url(r'^article/(?P<article_id>[0-9]+)/delete/$', views.delete_article, name='delete_article'),

    url(r'^notification/(?P<notification_id>[0-9]+)/$', views.notification_detail, name='notification_detail'),
    url(r'^notification/add/$', views.add_notification, name='add_notification'),
    url(r'^notification/(?P<notification_id>[0-9]+)/modify/$', views.modify_notification, name='modify_notification'),
    url(r'^notification/(?P<notification_id>[0-9]+)/delete/$', views.delete_notification, name='delete_notification'),


    url(r'modify_teacher_description/$', views.modify_teacher_description, name='modify_teacher_description'),

    url(r'^teacher/$', views.teacher_index, name='teacher_index'),
    url(r'^teacher/class/(?P<class_id>[0-9]+)/$', views.teacher_my_class, name='teacher_class'),
    url(r'^teacher/homework/(?P<homework_id>[0-9]+)/$', views.teacher_check_homework, name='teacher_check_homework'),
    url(r'^teacher/homework/add/$', views.add_homework, name='add_homework'),
    url(r'^teacher/homework/(?P<homework_id>[0-9]+)/modify/$', views.modify_homework, name='modify_homework'),
    url(r'^teacher/homework/(?P<homework_id>[0-9]+)/delete/$', views.delete_homework, name='delete_homework'),
    url(r'^teacher/homework/check/(?P<finish_id>[0-9]+)/$', views.teacher_check_detail, name='teacher_check_detail'),

    url(r'^student/$', views.student_index, name='student_index'),
    url(r'^student/class/(?P<class_id>[0-9]+)/$', views.student_my_class, name='student_class'),
    url(r'^student/homework/(?P<homework_id>[0-9]+)/$', views.student_view_homework, name='student_view_homework'),
    url(r'^student/homework/upload/(?P<finish_id>[0-9]+)/$', views.student_upload_homework, name='student_upload_homework'),

    url(r'^guest/$', views.guest_index, name='guest_index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
