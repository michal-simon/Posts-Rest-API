from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer


class PostLikeApiView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request, post_id):
		pass

	def delete(self, request, post_id):
		pass


class PostModelViewSet(ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = Post
	serializer_class = PostSerializer

	def create(self, request, *args, **kwargs):
		post = request.data.copy()
		post['user'] = request.user.id
		serializer = self.serializer_class(data=post)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		return Response('Invalid request. Please provide a title and a description.', status=HTTP_400_BAD_REQUEST)
