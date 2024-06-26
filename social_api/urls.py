from django.urls import path, include
from rest_framework import routers
from social_api.views import (
    PostViewSet,
    LikeAPIView,
    LikedPost,
    CommentList,
    CommentDetail,
)

router = routers.DefaultRouter()
app_name = "social_api"


router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:pk>/like/", LikeAPIView.as_view(), name="like-create"),
    path("liked-posts/", LikedPost.as_view(), name="liked-posts"),
    path("comments/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
    path("comments/", CommentList.as_view(), name="comment-list"),
]
