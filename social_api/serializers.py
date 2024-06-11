from rest_framework import serializers
from social_api.models import Post, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "content", "created_at", "image", "hashtags")


class LikeSerializer(serializers.ModelSerializer):
    liker = serializers.ReadOnlyField(source="liker.username")

    class Meta:
        model = Like
        fields = ["id", "liker", "created_at"]
