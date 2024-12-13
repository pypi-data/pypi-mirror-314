from functools import reduce
from operator import or_

from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Q, Subquery
from django.utils.functional import cached_property
from wbcore import viewsets
from wbcore.content_type.utils import get_ancestors_content_type
from wbnews.models import News, NewsRelationship, NewsSource
from wbnews.serializers import (
    NewsModelSerializer,
    NewsRelationshipModelSerializer,
    NewsRepresentationSerializer,
    SourceModelSerializer,
    SourceRepresentationSerializer,
)

from .buttons import NewsButtonConfig
from .display import (
    NewsDisplayConfig,
    NewsRelationshipDisplayConfig,
    NewsSourceDisplayConfig,
    SourceDisplayConfig,
)
from .endpoints import NewsEndpointConfig, NewsSourceEndpointConfig
from .titles import (
    NewsRelationshipTitleConfig,
    NewsSourceModelTitleConfig,
    NewsTitleConfig,
    SourceModelTitleConfig,
)


class NewsRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = News.objects.all()
    serializer_class = NewsRepresentationSerializer
    filterset_fields = {"title": ["icontains"]}
    ordering_fields = ["datetime"]
    ordering = ["-datetime"]
    search_fields = ["title", "description"]


class SourceRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = NewsSource.objects.all()
    serializer_class = SourceRepresentationSerializer
    filterset_fields = {"title": ["icontains"]}
    ordering_fields = ordering = ["title"]
    search_fields = ["title"]


class SourceModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SourceModelSerializer
    queryset = NewsSource.objects.all()
    filterset_fields = {"title": ["icontains"]}
    ordering_fields = ordering = ["title"]
    search_fields = ["title"]

    display_config_class = SourceDisplayConfig
    title_config_class = SourceModelTitleConfig


class NewsModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsModelSerializer
    filterset_fields = {"title": ["icontains"], "datetime": ["lte", "gte"], "source": ["exact"], "language": ["exact"]}
    ordering_fields = ["datetime"]
    ordering = ["-datetime"]
    search_fields = ["title", "description"]

    queryset = News.objects.select_related("source")

    button_config_class = NewsButtonConfig
    display_config_class = NewsDisplayConfig
    title_config_class = NewsTitleConfig
    endpoint_config_class = NewsEndpointConfig

    def get_queryset(self):
        qs = super().get_queryset()
        if (content_type_id := self.kwargs.get("content_type")) and (object_id := self.kwargs.get("content_id")):
            content_type = ContentType.objects.get_for_id(content_type_id)
            content_object = content_type.get_object_for_this_type(id=object_id)
            content_types = list(get_ancestors_content_type(content_type))
            # we ensure that for MPTT model, all descendants news are included as well
            if hasattr(content_object, "get_family"):
                conditions = []
                for descendant in content_object.get_family():
                    for ct in content_types:
                        conditions.append(Q(content_type=ct, object_id=descendant.id))
            else:
                conditions = [Q(content_type=ct, object_id=object_id) for ct in content_types]
            relationships = NewsRelationship.objects.filter(reduce(or_, conditions))
            qs = qs.filter(relationships__in=relationships)
        return qs.distinct()


class NewsRelationshipModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsRelationshipModelSerializer
    queryset = News.objects.all()
    display_config_class = NewsRelationshipDisplayConfig
    title_config_class = NewsRelationshipTitleConfig
    ordering = ["-datetime"]

    @cached_property
    def content_type(self) -> ContentType:
        if content_type_id := self.kwargs.get("content_type"):
            return ContentType.objects.get_for_id(content_type_id)

    @cached_property
    def content_object(self):
        if (object_id := self.kwargs.get("content_id")) and self.content_type:
            return self.content_type.get_object_for_this_type(id=object_id)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.content_type and self.content_object:
            content_types = list(get_ancestors_content_type(self.content_type))
            # we ensure that for MPTT model, all descendants news are included as well
            if hasattr(self.content_object, "get_family"):
                conditions = []
                for descendant in self.content_object.get_family():
                    for ct in content_types:
                        conditions.append(Q(content_type=ct, object_id=descendant.id))
            else:
                conditions = [Q(content_type=ct, object_id=self.content_object.id) for ct in content_types]
            relationships = NewsRelationship.objects.filter(reduce(or_, conditions))

            return queryset.filter(id__in=relationships.values("news")).annotate(
                analysis=Subquery(relationships.filter(news=OuterRef("id")).values("analysis")[:1]),
                sentiment=Subquery(relationships.filter(news=OuterRef("id")).values("sentiment")[:1]),
            )
        return News.objects.none()


class NewsSourceModelViewSet(NewsModelViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(source_id=self.kwargs["source_id"])

    display_config_class = NewsSourceDisplayConfig
    title_config_class = NewsSourceModelTitleConfig
    endpoint_config_class = NewsSourceEndpointConfig
