from django.dispatch import receiver
from django.utils.translation import gettext as _
from rest_framework.reverse import reverse
from wbcore.contrib.icons import WBIcon
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig
from wbcore.signals.instance_buttons import add_extra_button


class NewsButtonConfig(ButtonViewConfig):
    def get_custom_list_instance_buttons(self):
        return {bt.HyperlinkButton(key="open_link", label=_("Open News"), icon=WBIcon.LINK.icon)}

    def get_custom_instance_buttons(self):
        return self.get_custom_list_instance_buttons()


@receiver(add_extra_button)
def add_new_extra_button(sender, instance, request, view, pk=None, **kwargs):
    if instance and pk and view:
        content_type = view.get_content_type()
        endpoint = reverse("wbnews:news_relationship_content_object", args=[content_type.id, pk], request=request)
        return bt.WidgetButton(endpoint=endpoint, label="News", icon=WBIcon.NEWSPAPER.icon)
