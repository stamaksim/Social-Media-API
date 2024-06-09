import os.path
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/profile_pics", filename)


class CustomerUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.ImageField(
        upload_to=profile_image_file_path, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    followers = models.ManyToManyField(
        "self", blank=True, related_name="user_followers", symmetrical=False
    )
    following = models.ManyToManyField(
        "self", blank=True, related_name="user_following", symmetrical=False
    )

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
