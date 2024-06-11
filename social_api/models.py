import os
import pathlib
import uuid

from django.utils.text import slugify

from django.db import models

from users.models import CustomerUser


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.author.email)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/post_pics", filename)


class Post(models.Model):
    author = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=profile_image_file_path, blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.content[:30]


class Like(models.Model):
    liker = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("liker", "post")
        ordering = ["-created_at"]
