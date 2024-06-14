from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from social_api.models import Post, Like, Comment
from social_api.serializers import (
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
)
from .permissions import IsOwnerReadOnly
from .tasks import create_scheduled_post


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ["hashtags", "author__email"]
    search_fields = ["content", "hashtags"]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(
            Q(author__in=following_users) | Q(author=user)
        ).order_by("-created_at")

    @action(detail=False, methods=["post"])
    def schedule_post_creation(self, request):
        content = request.data.get("content")
        hashtags = request.data.get("hashtags", "")
        eta = datetime.utcnow() + timedelta(
            minutes=int(request.data.get("delay_minutes", 1))
        )
        create_scheduled_post.apply_async((content, request.user.id, hashtags), eta=eta)
        return Response({"status": "Post creation scheduled"})


class LikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs["pk"])
        return Like.objects.filter(liker=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You have already liked this post")
        post = Post.objects.get(pk=self.kwargs["pk"])
        serializer.save(liker=self.request.user, post=post)

    def delete(self, request, *args, **kwargs):
        like = self.get_queryset().first()
        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError("You have never liked this post")


class LikedPost(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        likes = Like.objects.filter(liker=self.request.user)
        liked_post = [like.post for like in likes]
        return liked_post


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
