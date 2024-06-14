from datetime import datetime, timedelta
from django.db.models import Q
from drf_spectacular import openapi
from drf_spectacular.utils import OpenApiParameter, extend_schema

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="author_email",
                type=openapi.OpenApiTypes.STR,
                description="Filter posts by author's email.",
            ),
            OpenApiParameter(
                name="hashtags",
                type=openapi.OpenApiTypes.STR,
                description="Filter posts by hashtags.",
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        """
        Get a list of posts.
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def schedule_post_creation(self, request):
        """
        Schedule a post creation.
        """
        content = request.data.get("content")
        hashtags = request.data.get("hashtags", "")
        eta = datetime.utcnow() + timedelta(
            minutes=int(request.data.get("delay_minutes", 1))
        )
        create_scheduled_post.apply_async((content, request.user.id, hashtags), eta=eta)
        return Response({"status": "Post creation scheduled"})


class LikeAPIView(generics.CreateAPIView, mixins.DestroyModelMixin):
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type=openapi.OpenApiTypes.STR,
                description="Filter likes by user.",
            ),
            OpenApiParameter(
                name="post",
                type=openapi.OpenApiTypes.STR,
                description="Filter likes by post.",
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        """
        Get a list of likes.
        """
        return super().list(request, *args, **kwargs)


class LikedPost(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        likes = Like.objects.filter(liker=self.request.user)
        liked_posts = [like.post for like in likes]
        return liked_posts


class LikerAPIView(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs["pk"])
        return Like.objects.filter(liker=user, post=post)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="liker",
                type=openapi.OpenApiTypes.STR,
                description="Filter likes by liker.",
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        """
        Get a list of likers.
        """
        return super().list(request, *args, **kwargs)


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
