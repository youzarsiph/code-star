# Generated by Django 5.1 on 2024-09-11 06:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        db_index=True,
                        default="Untitled chat",
                        help_text="Chat title",
                        max_length=64,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        db_index=True,
                        default="Untitled chat",
                        help_text="Chat description",
                        max_length=512,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Date created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Last update"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Chat owner",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
