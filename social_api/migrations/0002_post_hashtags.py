# Generated by Django 5.0.6 on 2024-06-11 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="hashtags",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]