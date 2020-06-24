from django.conf.urls import url, include


namespace = 'feed'
urlpatterns = (
    # articles
    url(
        r'^articles/', include('apps.feed.urls.article')
    ),
)
