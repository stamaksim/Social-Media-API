from rest_framework import serializers
from social_api.models import Post, Like, Comment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Post
        fields = ("id", "content", "author", "created_at", "image", "hashtags")


class LikeSerializer(serializers.ModelSerializer):
    liker = serializers.ReadOnlyField(source="liker.id")

    class Meta:
        model = Like
        fields = ["id", "liker", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Comment
        fields = ["id", "text", "owner", "post", "parent"]
