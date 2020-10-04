from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import jwt
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import (
	HTTP_201_CREATED,
	HTTP_400_BAD_REQUEST,
	HTTP_500_INTERNAL_SERVER_ERROR,
	HTTP_200_OK,
)
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from .serializers import UserSerializer


class UserCreateView(CreateAPIView):
	serializer_class = UserSerializer

	def create(self, request, *args, **kwargs):
		"""
		Creates new user.
		:param request: an object that contains data about request (dict).
		:param args: additional arguments (list).
		:param kwargs: additional key-value pair arguments (dict).
		:return: Response.
		"""
		user = request.data
		serializer = self.serializer_class(data=user)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		return Response(status=HTTP_400_BAD_REQUEST)


class UserAuthView(APIView):

	def post(self, request):
		"""
		Returns an auth token.
		:param request: an object that contains data about request (dict).
		:return: Response.
		"""
		try:
			username = request.data['username']
			password = request.data['password']
			user = User.objects.get(username=username, password=password)
			if user:
				try:
					payload = jwt_payload_handler(user)
					token = jwt.encode(payload, settings.SECRET_KEY)
					data = {
						'token': token
					}
					return Response(data, status=HTTP_200_OK)
				except:
					return Response('Oops, something went wrong', status=HTTP_500_INTERNAL_SERVER_ERROR)
		except (User.DoesNotExist, KeyError) as e:
			return Response('Please provide correct an email and a password', status=HTTP_400_BAD_REQUEST)
