from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import (
    CreateUserView,
    ManageUserView,
    LogoutView,
    UsersList,
    UserProfileView,
    FollowUnfollowView,
)

app_name = "users"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("profiles/", UsersList.as_view(), name="profile"),
    path("users/<str:email>/", UserProfileView.as_view(), name="user-profile"),
    path("follow-unfollow", FollowUnfollowView.as_view(), name="follow-unfollow"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
