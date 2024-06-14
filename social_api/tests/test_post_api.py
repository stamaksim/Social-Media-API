from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from social_api.models import Post

POST_URL = reverse("social_api:post-list")


def detail_url(post_id):
    return reverse("social_api:post-detail", args=[post_id])


def sample_post(author, **params):
    defaults = {"content": "Test content"}
    defaults.update(params)
    return Post.objects.create(author=author, **defaults)


class UnauthenticatedPostApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPostApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        sample_post(author=self.user)
        res = self.client.get(POST_URL)
        posts = Post.objects.all()
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), posts.count())

    def test_create_post(self):
        payload = {"content": "New post content"}
        res = self.client.post(POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post_id = res.data["id"]
        post_from_response = Post.objects.get(id=post_id)

        for key in payload:
            self.assertEqual(payload[key], getattr(post_from_response, key))

    def test_delete_post(self):
        post = sample_post(author=self.user)
        url = detail_url(post.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())
