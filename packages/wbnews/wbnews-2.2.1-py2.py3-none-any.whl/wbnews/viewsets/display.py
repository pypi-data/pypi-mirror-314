from typing import Optional

from django.utils.translation import gettext as _
from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
    create_simple_section,
)
from wbcore.metadata.configs.display.instance_display.utils import repeat_field
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class SourceDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="title", label=_("Title")),
                dp.Field(key="identifier", label=_("RSS feed")),
                dp.Field(key="author", label=_("Author")),
                dp.Field(key="description", label=_("Description")),
                dp.Field(key="updated", label=_("Last Update")),
            ]
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["title", "identifier"],
                ["author", "updated"],
                [repeat_field(2, "description")],
                [repeat_field(2, "news_section")],
            ],
            [create_simple_section("news_section", "News", [["news"]], "news", collapsed=False)],
        )


class NewsDisplayConfig(DisplayViewConfig):
    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["datetime", "source"],
                ["language", "link"],
                [repeat_field(2, "summary")],
                [repeat_field(2, "description")],
            ]
        )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="datetime", label=_("Datetime")),
                dp.Field(key="title", label=_("Title")),
                dp.Field(key="summary", label=_("Summary")),
                dp.Field(key="description", label=_("Description")),
                # dp.Field(key="tags", label=_("Edited")),
                dp.Field(key="source", label=_("Source")),
                dp.Field(key="language", label=_("Language")),
                dp.Field(key="image_url", label=_("Image")),
            ]
        )


class NewsRelationshipDisplayConfig(DisplayViewConfig):
    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["datetime", "source"],
                ["language", "link"],
                [repeat_field(2, "summary")],
                [repeat_field(2, "description")],
            ]
        )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        POSITIVE = "#96DD99"
        SLIGHTLY_POSITIVE = "#FFEE8C"
        SLIGHTLY_NEGATIVE = "#FF964F"
        NEGATIVE = "#FF6961"

        return dp.ListDisplay(
            fields=[
                dp.Field(key="datetime", label=_("Datetime")),
                dp.Field(key="analysis", label=_("Analysis")),
                dp.Field(key="title", label=_("Title")),
                dp.Field(key="summary", label=_("Summary")),
                dp.Field(key="description", label=_("Description")),
            ],
            formatting=[
                dp.Formatting(
                    column="sentiment",
                    formatting_rules=[
                        dp.FormattingRule(condition=("==", 4), style={"backgroundColor": POSITIVE}),
                        dp.FormattingRule(condition=("==", 3), style={"backgroundColor": SLIGHTLY_POSITIVE}),
                        dp.FormattingRule(condition=("==", 2), style={"backgroundColor": SLIGHTLY_NEGATIVE}),
                        dp.FormattingRule(condition=("==", 1), style={"backgroundColor": NEGATIVE}),
                    ],
                )
            ],
            legends=[
                dp.Legend(
                    items=[
                        dp.LegendItem(icon=POSITIVE, label=_("Positive")),
                        dp.LegendItem(icon=SLIGHTLY_POSITIVE, label=_("Slightly Positive")),
                        dp.LegendItem(icon=SLIGHTLY_NEGATIVE, label=_("Slightly Negative")),
                        dp.LegendItem(icon=NEGATIVE, label=_("Negative")),
                    ]
                )
            ],
        )


class NewsSourceDisplayConfig(DisplayViewConfig):
    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                [repeat_field(2, "title")],
                ["datetime", "language", "link"],
                [repeat_field(2, "description")],
            ]
        )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="datetime", label=_("Datetime")),
                dp.Field(key="title", label=_("Title")),
                dp.Field(key="description", label=_("Description")),
                dp.Field(key="language", label=_("Language")),
                # dp.Field(key="tags", label="_(Edited")),
                # dp.Field(key="link", label="_(Link"))
            ]
        )
