from django.urls import path
from rest_framework import routers

from .views import PostViewSet, PostLikeApiView

router = routers.SimpleRouter()
router.register(r'', PostViewSet, basename='posts')

urlpatterns = [
	path('likes/<int:pk>/', PostLikeApiView.as_view(), name="likes"),
]
urlpatterns += router.urls
