from celery import shared_task
from django.utils import timezone
from social_api.models import Post
from django.contrib.auth import get_user_model


@shared_task
def create_scheduled_post(content, author_id, image=None, hashtags=None):
    User = get_user_model()
    author = User.objects.get(id=author_id)
    Post.objects.create(
        author=author,
        content=content,
        created_at=timezone.now(),
        image=image,
        hashtags=hashtags,
    )
