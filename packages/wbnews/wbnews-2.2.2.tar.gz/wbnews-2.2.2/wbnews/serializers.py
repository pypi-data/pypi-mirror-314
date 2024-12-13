from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse
from wbcore import serializers as wb_serializers

from .models import News, NewsSource


class SourceRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbnews:source-detail")

    class Meta:
        model = NewsSource
        fields = ("id", "title", "_detail")


class SourceModelSerializer(wb_serializers.ModelSerializer):
    title = wb_serializers.CharField(read_only=True, label=_("Title"))
    identifier = wb_serializers.CharField(read_only=True, label=_("Identifier"))
    image = wb_serializers.CharField(read_only=True)
    description = wb_serializers.CharField(read_only=True, label=_("Description"))
    author = wb_serializers.CharField(read_only=True, label=_("Author"))
    updated = wb_serializers.DateTimeField(read_only=True, label=_("Updated"))

    @wb_serializers.register_resource()
    def news(self, instance, request, user):
        return {"news": reverse("wbnews:source-news-list", args=[instance.id], request=request)}

    class Meta:
        model = NewsSource
        fields = ("id", "title", "identifier", "image", "description", "author", "updated", "_additional_resources")


class NewsRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbnews:news-detail")

    class Meta:
        model = News
        fields = ("id", "datetime", "title", "_detail")


class NewsModelSerializer(wb_serializers.ModelSerializer):
    _source = SourceRepresentationSerializer(source="source")
    image_url = wb_serializers.ImageURLField()

    @wb_serializers.register_resource()
    def open_link(self, instance, request, user):
        if instance.link:
            return {"open_link": instance.link}
        return {}

    # link = wb_serializers.URL()
    class Meta:
        model = News
        fields = (
            "id",
            "datetime",
            "title",
            "description",
            "summary",
            "link",
            "language",
            "image_url",
            "source",
            "_source",
            "_additional_resources",
        )


class NewsRelationshipModelSerializer(wb_serializers.ModelSerializer):
    sentiment = wb_serializers.IntegerField(required=False)
    analysis = wb_serializers.TextField(required=False)

    class Meta:
        model = News
        fields = (
            "id",
            "datetime",
            "sentiment",
            "analysis",
            "title",
            "description",
            "summary",
        )
