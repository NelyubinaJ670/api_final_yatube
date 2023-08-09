from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import (PostSerializer,
                          GroupSerializer,
                          CommentSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет эндпоинта posts/. Посты."""
    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет эндпоинта groups/. Группы."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет эндпоинта posts/.../comments/. Комментарии."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )
        return post_id.comments.select_related('author')

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )
        serializer.save(author=self.request.user, post=post)


class FollowViewSet (viewsets.ModelViewSet):
    """Вьюсет эндпоинта follow/. Подписки. """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
