import feedparser
import logging
from dateutil import parser

from django.core.management.base import BaseCommand

from apps.feed.models import Article


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--sources', type=str,
            help='List of rss sources, separated by comma'
        )
        parser.add_argument(
            '--log', type=str,
            help='Log to file, optional'
        )

    def handle(self, *args, **options):
        sources = options.get('sources').split(',')
        log_file = options.get('log', None)
        if log_file:
            for handler in logging.root.handlers:
                logging.root.removeHandler(handler)
            logging.basicConfig(
                filename=log_file,
                level=logging.DEBUG,
                format='%(levelname)s %(asctime)s %(module)s: %(message)s'
            )

        for source in sources:
            logger.info('Fetching data from {}'.format(source))
            try:
                feed = feedparser.parse(source)
                for entry in feed.entries:
                    article, created = self.__create_article(entry)
                    if created:
                        logger.info(
                            'Created a new article at {}'.format(article.link)
                        )
                    else:
                        logger.info(
                            'Article at {} exists, skipping now'.format(
                                article.link
                            )
                        )
            except Exception:
                logger.error('Cannot parse feed from {}'.format(source))

    def __create_article(self, entry):
        title = entry.get('title', None)
        description = entry.get('summary', None)
        link = entry.get('link', None)
        try:
            category = entry.get('tags')[0]['term']
        except Exception:
            logger.debug(
                'Cannot parse category for {}, data: {}'.format(
                    link, entry.get('tags')
                )
            )
            category = None
        comments = entry.get('comments', None)
        try:
            pub_date = parser.parse(entry.get('published'))
        except Exception:
            logger.debug(
                'Cannot parse published date for {}, data: {}'.format(  # NOQA
                    link, entry.get('published')
                )
            )
            pub_date = None
        guid = entry.get('id', None)

        return Article.objects.get_or_create(
            title=title, description=description, link=link,
            category=category, comments=comments, guid=guid,
            pub_date=pub_date
        )
