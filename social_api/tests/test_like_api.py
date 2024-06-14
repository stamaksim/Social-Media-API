from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from social_api.models import Post, Like


class LikeAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_like_post(self):
        post = Post.objects.create(author=self.user, content="Test post")
        url = reverse("social_api:like-create", args=[post.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(liker=self.user, post=post).exists())

    def test_unlike_post(self):
        post = Post.objects.create(author=self.user, content="Test post")
        like = Like.objects.create(liker=self.user, post=post)
        url = reverse("social_api:like-create", args=[post.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(liker=self.user, post=post).exists())

    def test_cannot_like_twice(self):
        post = Post.objects.create(author=self.user, content="Test post")
        Like.objects.create(liker=self.user, post=post)
        url = reverse("social_api:like-create", args=[post.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_unlike_if_not_liked(self):
        post = Post.objects.create(author=self.user, content="Test post")
        url = reverse("social_api:like-create", args=[post.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
