import feedparser
import logging
from dateutil import parser

from django.core.management.base import BaseCommand

from apps.feed.models import Article


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--sources", type=str)

    def handle(self, *args, **options):
        sources = options.get('sources').split(',')

        for source in sources:
            feed = feedparser.parse(source)
            for entry in feed.entries:
                title = entry.get('title', None)
                description = entry.get('summary', None)
                link = entry.get('link', None)
                try:
                    category = entry.get('tags')[0]['term']
                except Exception as _:
                    category = None
                comments = entry.get('comments', None)
                try:
                    pub_date = parser.parse(entry.get('published'))
                except Exception as _:
                    pub_date = None
                guid = entry.get('id', None)

                Article.objects.get_or_create(
                    title=title, description=description, link=link,
                    category=category, comments=comments, guid=guid,
                    pub_date=pub_date
                )
