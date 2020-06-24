from django.urls import path, include
from django.views import generic


app_name = 'feed'
urlpatterns = (
    path(
        '',
        generic.RedirectView.as_view(
            url='/feed/articles/', permanent=False
        ),
        name="index"
     ),

    # articles
    path(
        r'articles/', include('apps.feed.urls.article')
    ),
)
