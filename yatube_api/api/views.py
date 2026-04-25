from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from posts.models import Comment, Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class OptionalLimitOffsetPagination(LimitOffsetPagination):
    """Пагинация только при наличии limit или offset в запросе."""

    def paginate_queryset(self, queryset, request, view=None):
        params = request.query_params
        if 'limit' not in params and 'offset' not in params:
            return None
        return super().paginate_queryset(queryset, request, view=view)


class Return401UnauthenticatedMixin:
    """При отказе для неавторизованного пользователя возвращать 401."""

    def permission_denied(self, request, message=None, **kwargs):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
        super().permission_denied(request, message, **kwargs)


class PostViewSet(Return401UnauthenticatedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = OptionalLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(Return401UnauthenticatedMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = self.request.user.follower.all()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(following__username__icontains=search)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
