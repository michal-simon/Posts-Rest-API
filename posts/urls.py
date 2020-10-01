from django.urls import path

from .views import PostModelViewSet, PostLikeApiView

urlpatterns = [
	path('', PostModelViewSet.as_view({'post': 'create'}), name='posts'),
	path('likes/', PostLikeApiView.as_view(), name='post_likes'),
]
