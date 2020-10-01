from django.urls import path

from .views import UserCreateView, UserAuthView

urlpatterns = [
	path('', UserCreateView.as_view(), name='user_create'),
	path('auth/', UserAuthView.as_view(), name='user_auth'),
]
