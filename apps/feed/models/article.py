import uuid

from django.db import models

from ..managers import ArticleManager


class Article(models.Model):
    objects = ArticleManager

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField(
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    link = models.TextField(
        null=True,
        blank=True
    )
    category = models.TextField(
        null=True,
        blank=True
    )
    comments = models.TextField(
        null=True,
        blank=True
    )
    guid = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField(
        null=True,
        blank=True
    )
