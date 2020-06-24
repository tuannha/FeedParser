from libs.views import BaseModelListView

from apps.feed.models import Article


class ArticleListView(BaseModelListView):
    model = Article
    ajax_searchable = True
    ajax_search_fields = ['category']
