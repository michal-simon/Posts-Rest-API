from rest_framework import serializers

from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'title', 'description', 'user')


class PostLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostLike
		fields = ('id', 'post', 'user')
