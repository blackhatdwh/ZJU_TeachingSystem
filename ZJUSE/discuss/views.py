from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from display.models import *
from statistics import mean
import datetime, os, csv, json

# Create your views here.

def index(request):
	x = GroupList.objects.filter(name='Public')
	if(len(x)==0):
		g = GroupList()
		g.name="Public"
		g.save()
	if request.user.is_authenticated():
		return redirect(reverse('user_discuss_index'))
	else:
		return redirect(reverse('guest_discuss_index'))

def user_discuss_index(request):
	if request.user.is_authenticated():
		if request.user.groups.all().first().name == 'Teacher':
			teacher = Teacher.objects.get(user=request.user)
			ty = '老师'
		elif request.user.groups.all().first().name == 'Student':
			teacher = Student.objects.get(user=request.user)
			ty = '同学'
		g=GroupList.objects.get(name='Public')
		postslist = Posts.objects.filter(group=g).order_by('p_time')
		context = {
			'user': teacher,
			'postslist': postslist,
			'ty': ty,
			'group_id': g.g_id,
		}
		return render(request, 'user_discuss_index.html', context)
	else:
		#you are not a teacher!
		return HttpResponse('<script>alert("你不是用户！");location.replace("/guest");</script>')


def guest_discuss_index(request):
	g=GroupList.objects.get(name='Public')
	postslist = Posts.objects.filter(group=g).order_by('p_time')
	context = {
		'postslist': postslist,
	}
	return render(request, 'guest_discuss_index.html', context)

def posts_detail(request, posts_id, page):
	if request.user.is_authenticated() and request.user.groups.all().first().name == 'Student':
		u = Student.objects.get(user=request.user)
	elif request.user.is_authenticated() and request.user.groups.all().first().name == 'Teacher':
		u = Teacher.objects.get(user=request.user)
	else:
		u = '游客'
	posts = Posts.objects.get(p_id=posts_id)
	pc = posts.p_rc/10+1
	if(posts.p_rc<10):
		replylist = Reply.objects.filter(post=posts).order_by('r_time')
	else:
		n = int(page)
		replylist = Reply.objects.filter(post=posts, r_rk__gte=(n-1)*10, r_rk__lt=n*10).order_by('r_time')
	if request.user == posts.user:
		authority = True
	else:
		authority = False
	ffp=int(page)-2
	fp=int(page)-1
	np=int(page)+1
	nnp=int(page)+2
	return render(request, 'posts_detail.html', {'posts': posts, 'authority': authority, 'replylist':replylist, 'user':u, 'page':int(page), 'pc':pc, 'ffp':ffp, 'fp':fp, 'np':np, 'nnp':nnp})

def posts_public(request,group_id):
	if request.user.is_authenticated():
		pu = request.user
	print(request)
	title = request.POST['title']
	content = request.POST['content']
	newp = Posts()
	newp.user = pu
	newp.p_name = title
	newp.p_content = content
	newp.p_read = 0
	key = group_id
	newp.group = GroupList.objects.get(g_id=int(key))
	newp.p_time = timezone.localtime(timezone.now())
	newp.save()
	replylist=[]
	return render(request, 'posts_detail.html', {'posts': newp, 'authority': True, 'replylist':replylist, 'user':pu})

def posts_delete(request,post_id):
	post = Posts.objects.get(p_id = post_id)
	x = post.group.g_id
	post.delete()
	if x == 1:
		s = '<script>alert("删除成功！");location.replace("/forum/");</script>'
	else:
		s = '<script>alert("删除成功！");location.replace("/forum/group_detail/'+str(x)+'/");</script>'
	return HttpResponse(s)

def posts_reply(request,post_id):
	newr = Reply()
	if request.user.is_authenticated():
		pu = request.user
		newr.user = pu
	else:
		pu = '游客'
		newr.guest = pu
	x = Posts.objects.get(p_id=post_id)
	x.p_rc=x.p_rc+1
	x.save()
	pc = int(x.p_rc/10+1)
	newr.post = x
	newr.r_content = request.POST['content']
	newr.r_time = timezone.localtime(timezone.now())
	newr.r_rk=x.p_rc
	newr.save()
	s = '<script>alert("回复成功！");location.replace("/forum/posts_detail/'+str(x.p_id)+'/'+str(pc)+'");</script>'
	return HttpResponse(s)

def group_list(request):
	if request.user.is_authenticated():
		u = request.user
		if request.user.groups.all().first().name == 'Teacher':
			ty = '老师'
		elif request.user.groups.all().first().name == 'Student':
			ty = '同学'
	else:
		return redirect(reverse('discuss_index'))
	grouplist = GroupList.objects.filter(user = u)
	invlist = Iviation.objects.filter(to = u)
	return render(request, 'user_discuss_group.html',{'grouplist':grouplist,'user':u,'ty':ty,'invlist':invlist})
	
def group_add(request):
	if request.user.is_authenticated():
		u = request.user
	else:
		return redirect(reverse('discuss_index'))
	newg = GroupList()
	newg.name = request.POST['title']
	newg.host = u
	newg.save()
	newg.user.add(u)
	return redirect(reverse('group_list'))

def group_quit(request,group_id):
	if request.user.is_authenticated():
		u = request.user
	else:
		return redirect(reverse('discuss_index'))
	g = GroupList.objects.get(g_id = group_id)
	if g.host == u:
		return HttpResponse('<script>alert("小组主持人不能退出小组！");location.replace("/forum/group_list");</script>')
	else:
		g.user.remove(u)
		return redirect(reverse('group_list'))

def group_delete(request,group_id):
	if request.user.is_authenticated():
		u = request.user
	else:
		return redirect(reverse('discuss_index'))
	g = GroupList.objects.get(g_id = group_id)
	if g.host == u:
		memberlist = g.user.all()
		if(len(memberlist)>1):
			s = '<script>alert("小组内还有成员无法删除！");location.replace("/forum/group_detail/'+str(g.g_id)+'/");</script>'
			return HttpResponse(s)
		else:
			g.delete()
			return redirect(reverse('group_list'))
	else:
		return HttpResponse('<script>alert("你不是小组主持人！");location.replace("/forum/");</script>')

def group_detail(request,group_id):
	if request.user.is_authenticated():
		u = request.user
	else:
		return redirect(reverse('discuss_index'))
	g = GroupList.objects.get(g_id = group_id)
	host = g.host
	if host == u:
		authority=True
	else:
		authority=False
	memlist = g.user.all()
	memberlist=[]
	for mem in memlist:
		if mem.groups.all().first().name == 'Teacher':
			member = Teacher.objects.get(user=mem)
		elif mem.groups.all().first().name == 'Student':
			member = Student.objects.get(user=mem)
		memberlist.append(member)

	postlist = Posts.objects.filter(group=g).order_by('p_time')
	content={
		'user':u,
		'group':g,
		'host':host,
		'authority':authority,
		'memberlist':memberlist,
		'postlist':postlist,
	}
	return render(request, 'group_detail.html',content)

def invitation_accept(request,invid):
	inv = Iviation.objects.get(id=invid)
	inv.group.user.add(request.user)
	inv.delete()
	return redirect(reverse('group_list'))

def invitation_add(request):
	if request.user.is_authenticated():
		u = request.user
	else:
		return redirect(reverse('discuss_index'))
	rid = request.POST['ID']
	r = User.objects.filter(username = rid)
	if len(r) == 0:
		HttpResponse('<script>alert("该用户不存在！");location.replace("/forum/");</script>')
	else:
		rec = User.objects.get(username = rid)
		newinv = Iviation()
		newinv.fr = u
		newinv.to = rec
		newinv.i_content = request.POST['content']
		newinv.group = GroupList.objects.get(g_id=request.POST['group_id'])
		newinv.save()
		s = '<script>alert("邀请已发送！");location.replace("/forum/group_detail/'+str(newinv.group.g_id)+'/");</script>'
		return HttpResponse(s)
