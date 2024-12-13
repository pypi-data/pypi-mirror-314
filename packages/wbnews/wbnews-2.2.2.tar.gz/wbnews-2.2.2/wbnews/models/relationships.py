from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class NewsRelationship(models.Model):
    news = models.ForeignKey(to="wbnews.News", related_name="relationships", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    sentiment = models.PositiveIntegerField(null=True, blank=True)
    analysis = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.news.title} -> {self.content_object}"

    class Meta:
        verbose_name = "News Relationship"
        indexes = [models.Index(fields=["content_type", "object_id"])]
