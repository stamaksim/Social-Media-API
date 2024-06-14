from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from social_api.models import Post, Comment, CustomerUser


class CommentTest(APITestCase):
    def setUp(self):
        self.user = CustomerUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        # Clean up any existing data to start fresh
        Comment.objects.all().delete()

        self.post = Post.objects.create(author=self.user, content="Test content")

        # Create comments for testing
        self.comment1 = Comment.objects.create(
            post=self.post, owner=self.user, text="Test comment 1"
        )
        self.comment2 = Comment.objects.create(
            post=self.post, owner=self.user, text="Test comment 2"
        )
        self.comment3 = Comment.objects.create(
            post=self.post, owner=self.user, text="Test comment 3"
        )
        self.comment4 = Comment.objects.create(
            post=self.post, owner=self.user, text="Test comment 4"
        )

    def test_list_comments(self):
        response = self.client.get(reverse("social_api:comment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Adjusted to check for all comments

    def test_create_comment(self):
        data = {"text": "New comment", "post": self.post.pk}
        response = self.client.post(reverse("social_api:comment-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 5)

    def test_retrieve_comment(self):
        response = self.client.get(
            reverse("social_api:comment-detail", kwargs={"pk": self.comment1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.comment1.text)

    def test_delete_comment(self):
        response = self.client.delete(
            reverse("social_api:comment-detail", kwargs={"pk": self.comment1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 3)
