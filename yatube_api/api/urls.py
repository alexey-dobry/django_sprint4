from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
# Вложенный маршрут комментариев — первым, чтобы не перехватывал posts/<pk>/
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post-comments'
)
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follow')

v1_urlpatterns = [
    path('', include('djoser.urls.jwt')),  # jwt/create, refresh, verify
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
