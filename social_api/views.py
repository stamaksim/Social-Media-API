from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from social_api.models import Post, Like
from social_api.serializers import PostSerializer, LikeSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ["hashtags", "author__email"]
    search_fields = ["content", "hashtags"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=[user] + list(following_users))


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
