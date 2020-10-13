from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import jwt
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
)
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from .models import UserRequest, REQUEST_SIGN_IN
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
            user = serializer.save()
            UserRequest.objects.create(
                user=user,
                post=request.data,
            )
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
                UserRequest.objects.create(
                    user=user,
                    post=request.data,
                    request_type=REQUEST_SIGN_IN,
                )
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    data = {
                        'token': token
                    }
                    return Response(data, status=HTTP_200_OK)
                except:
                    return Response('Oops, something went wrong', status=HTTP_500_INTERNAL_SERVER_ERROR)
        except (User.DoesNotExist, KeyError):
            return Response('Please provide correct an email and a password', status=HTTP_400_BAD_REQUEST)


class UserActivityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Returns user's last log-in and request time.
        :param request: an object that contains data about request (dict).
        :return: Response.
        """
        last_request = UserRequest.objects.filter(user=request.user).last()
        last_login = UserRequest.objects.filter(
            user=request.user, request_type=REQUEST_SIGN_IN).last()
        data = {}
        if last_request:
            data['last_request'] = last_request.time.strftime('%Y-%m-%d %H:%M')
        if last_login:
            data['last_login'] = last_login.time.strftime('%Y-%m-%d %H:%M')
        return JsonResponse(data, status=HTTP_200_OK)
