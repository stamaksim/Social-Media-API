# Generated by Django 5.0.6 on 2024-06-14 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_api", "0006_remove_post_scheduled_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="hashtags",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
