from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class DependantArticleEndpointViewConfig(EndpointViewConfig):
    def _get_instance_endpoint(self, **kwargs):
        return "{{dependant_article_url}}" if "article_id" in self.view.kwargs else "{{article_url}}"


class ReviewerArticleModelEndpointConfig(EndpointViewConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse("wbwriter:review-article-list", args=[], request=self.request)
