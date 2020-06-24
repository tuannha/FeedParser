from django.conf.urls import url, include

from apps.feed.views import ArticleViewSet

urlpatterns = [
    url('', include(ArticleViewSet().urls)),
]
