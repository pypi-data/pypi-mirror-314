from django.contrib.postgres.fields import ArrayField
from django.db import models
from wbcore.models import WBModel


class NewsSource(WBModel):
    class Type(models.TextChoices):
        RSS = "RSS", "RSS"
        EMAIL = "EMAIL", "EMAIL"

    type = models.CharField(default=Type.RSS, choices=Type.choices, max_length=6)
    title = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, unique=True, blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=16), default=list, blank=True)
    image = models.URLField(blank=True, null=True)
    description = models.TextField(default="", blank=True)
    author = models.CharField(max_length=255, default="")
    clean_content = models.BooleanField(default=False)
    url = models.URLField(
        blank=True,
        null=True,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbnews:sourcerepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{title}}"

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbnews:source"
