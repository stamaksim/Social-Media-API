from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from .serializers import FollowUnfollowSerializer, UserSerializer, LogoutSerializer
from django.http import Http404
from social_api.permissions import IsOwnerReadOnly

CustomerUser = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, pk):
        try:
            return CustomerUser.objects.get(id=pk)
        except CustomerUser.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = FollowUnfollowSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get("id")
            req_type = serializer.validated_data.get("type")

            current_user = request.user
            other_user = self.get_user(pk)

            if current_user == other_user:
                return Response(
                    {"detail": "You cannot follow/unfollow yourself."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if req_type == "follow":
                return self.follow_user(current_user, other_user)

            elif req_type == "unfollow":
                return self.unfollow_user(current_user, other_user)

            else:
                return Response(
                    {"detail": "Invalid request type."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def follow_user(self, current_user, other_user):
        if current_user.following.filter(id=other_user.id).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user.following.add(other_user)
        other_user.followers.add(current_user)
        return Response({"Following": "Following success!"}, status=status.HTTP_200_OK)

    def unfollow_user(self, current_user, other_user):
        if not current_user.following.filter(id=other_user.id).exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user.following.remove(other_user)
        other_user.followers.remove(current_user)
        return Response({"Unfollow": "Unfollow success!"}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        user = request.user
        followers = user.followers.all()
        following = user.following.all()

        followers_data = UserSerializer(followers, many=True).data
        following_data = UserSerializer(following, many=True).data

        return Response(
            {"followers": followers_data, "following": following_data},
            status=status.HTTP_200_OK,
        )


class UsersList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = CustomerUser.objects.all()
        username = self.request.query_params.get("username")
        email = self.request.query_params.get("email")
        bio = self.request.query_params.get("bio")

        if username:
            queryset = queryset.filter(username__icontains=username)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if bio:
            queryset = queryset.filter(bio__icontains=bio)

        return queryset


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerReadOnly)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
