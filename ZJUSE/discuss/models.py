from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class GroupList(models.Model):
	g_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20)
	host = models.ForeignKey(User,related_name='group_host' ,on_delete=models.CASCADE, null=True)
	user = models.ManyToManyField(User)

class Posts(models.Model):
	user = models.ForeignKey(User,related_name='posts_user' ,on_delete=models.CASCADE)
	p_id = models.AutoField(primary_key=True)
	p_name = models.CharField(max_length=20,null=False)
	p_content = models.CharField(max_length=3000)
	p_time = models.DateTimeField()
	p_read = models.IntegerField()
	p_rc = models.IntegerField(default=0)
	group = models.ForeignKey(GroupList,related_name='posts_group', on_delete=models.CASCADE)

class Reply(models.Model):
	user = models.ForeignKey(User,related_name='reply_user',on_delete=models.CASCADE)
	guest = models.CharField(max_length=10,null=True)
	post = models.ForeignKey(Posts,related_name='reply_posts', on_delete=models.CASCADE)
	r_id = models.AutoField(primary_key=True)
	r_content = models.CharField(max_length=3000)
	r_time = models.DateTimeField()
	r_rk = models.IntegerField(default=0)

class Iviation(models.Model):
	fr = models.ForeignKey(User,related_name='iviation_from',on_delete=models.CASCADE)
	to = models.ForeignKey(User,related_name='iviation_to',on_delete=models.CASCADE)
	group = models.ForeignKey(GroupList,related_name='iviation_group',on_delete=models.CASCADE)
	i_content = models.CharField(max_length=3000)

