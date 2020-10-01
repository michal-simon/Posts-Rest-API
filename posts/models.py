from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=100, verbose_name='Title')
	description = models.TextField(verbose_name='Description')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


class PostLike(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

	class Meta:
		verbose_name = 'Post Like'
		verbose_name_plural = 'Post Likes'
