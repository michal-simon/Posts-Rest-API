from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Post, PostLike
from .serializers import PostSerializer


class PostLikeApiView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request, pk=None):
		"""
		Creates a post like.
		:param request: an object that contains data about request (dict).
		:param pk: id of post (int).
		:return: Response.
		"""
		PostLike.objects.get_or_create(post_id=pk, user=request.user)
		return Response('Created.', status=HTTP_201_CREATED)

	def delete(self, request, pk=None):
		"""
		Deletes a post like.
		:param request: an object that contains data about request (dict).
		:param pk: id of post (int).
		:return: Response.
		"""
		like = get_object_or_404(PostLike, post_id=pk, user=request.user)
		like.delete()
		return Response('Deleted.', status=HTTP_200_OK)


class PostViewSet(ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def create(self, request, *args, **kwargs):
		"""
		Creates a post.
		:param request: object that contains data about request (dict).
		:param args: Additional args (list).
		:param kwargs: Additional key-value args (dict).
		:return: Response.
		"""
		post = request.data.copy()
		post['user'] = request.user.id
		serializer = self.serializer_class(data=post)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		return Response('Invalid request. Please provide a title and a description.', status=HTTP_400_BAD_REQUEST)
