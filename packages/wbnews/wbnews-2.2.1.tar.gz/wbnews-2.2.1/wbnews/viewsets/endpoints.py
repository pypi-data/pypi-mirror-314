from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class NewsEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbnews:news-list", request=self.request)

    def get_instance_endpoint(self, **kwargs):
        return self.get_list_endpoint()


class NewsSourceEndpointConfig(NewsEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse("wbnews:source-news-list", args=[self.view.kwargs["source_id"]], request=self.request)
