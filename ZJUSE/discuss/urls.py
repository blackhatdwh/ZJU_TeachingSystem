from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index,name='discuss_index'),
    url(r'^user_discuss_index', views.user_discuss_index,name='user_discuss_index'),
    url(r'^guest_discuss_index', views.guest_discuss_index,name='guest_discuss_index'),
    url(r'^posts_detail/(.+)/(.+)/$', views.posts_detail,name='posts_detail'),
    url(r'^posts_public/(.+)/$', views.posts_public,name='posts_public'),
    url(r'^posts_delete/(.+)/$', views.posts_delete,name='posts_delete'),
    url(r'^posts_reply/(.+)/$', views.posts_reply,name='posts_reply'),
    url(r'^group_list', views.group_list,name='group_list'),
    url(r'^group_add', views.group_add,name='group_add'),
    url(r'^group_quit/(.+)/$', views.group_quit,name='group_quit'),
    url(r'^group_delete/(.+)/$', views.group_delete,name='group_delete'),
    url(r'^group_detail/(.+)/$', views.group_detail,name='group_detail'),
    url(r'^invitation_add', views.invitation_add,name='invitation_add'),
    url(r'^invitation_accept/(.+)/$', views.invitation_accept,name='invitation_accept'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
