from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Post, Group, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet written from the documentation,
    the only thing is that the permissions are written explicitly.
    To create a post by the author, we take from whom the request came from.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet written from the documentation,
    the only thing is that the permissions are written explicitly.

    To create a comment by the author, we take from who the request came from.
    For a linear connection of a comment with a post,
    we pull on the primary key.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return post.comments


class GroupViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    ModelViewSet written from the documentation.  Only GET or POST method.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    ModelViewSet written from the documentation. Only GET or POST method.
    """
    serializer_class = FollowSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    filter_backends = [SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        get_object_or_404(User, pk=self.request.user.pk)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return user.following
