from material.frontend.views import ModelViewSet
from apps.feed.models import Article


class ArticleViewSet(ModelViewSet):
    model = Article
