from rest_framework import serializers
from social_api.models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "author", "content", "created_at", "image", "hashtags")


class LikeSerializer(serializers.ModelSerializer):
    liker = serializers.ReadOnlyField(source="liker.username")

    class Meta:
        model = Like
        fields = ["id", "liker", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Comment
        fields = ["id", "text", "owner", "post", "parent"]
