from django.urls import path

from .views import UserCreateView, UserAuthView, UserActivityView

urlpatterns = [
	path('', UserCreateView.as_view(), name='user_create'),
	path('auth/', UserAuthView.as_view(), name='user_auth'),
	path('activity/', UserActivityView.as_view(), name='user_activity'),
]
