from material.frontend.views import ModelViewSet
from apps.feed.models import Article

from .list import ArticleListView


class ArticleViewSet(ModelViewSet):
    model = Article
    list_display = ['title', 'link', 'pub_date']

    list_view_class = ArticleListView
