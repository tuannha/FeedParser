import feedparser
import logging
import mock
import os
from dateutil import parser
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from apps.feed.models import Article
from tests.unit.factories import ArticleFactory


class ParsedRssResult(object):
    def __init__(self, entries):
        self.entries = entries


class TestFetchArticle(TestCase):
    def setUp(self):
        super().setUp()

        Article.objects.all().delete()

    @mock.patch.object(logging.Logger, 'info')
    def test_run_command_failed_by_no_sources(self, mock_log_info):
        out = StringIO()
        call_command('fetch_article', stdout=out, sources='')
        self.assertEqual(0, mock_log_info.call_count)

    @mock.patch.object(logging.Logger, 'error')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_failed_by_parse_error(self, mock_parser, mock_error):
        mock_parser.side_effect = Exception('error')
        out = StringIO()
        call_command(
            'fetch_article', stdout=out,
            sources='https://www.feedforall.com/blog-feed.xml'
        )
        self.assertEqual(1, mock_error.call_count)

    @mock.patch.object(logging.Logger, 'info')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_success_one_source(self, mock_parser, mock_log_info):
        entries = [
            {
                'title': 'title1',
                'summary': 'summary1',
                'link': 'link1',
                'tags': [{'term': 'term'}],
                'comments': 'comments',
                'published': '2014-02-05 09:00:00+00:00',
                'id': 'id'
            }
        ]
        mock_parser.return_value = ParsedRssResult(entries=entries)

        out = StringIO()
        call_command(
            'fetch_article', stdout=out,
            sources='https://www.feedforall.com/blog-feed.xml'
        )
        # one info log for fetching, one info log for creating object
        self.assertEqual(2, mock_log_info.call_count)
        self.assertEqual(1, Article.objects.count())

    @mock.patch.object(logging.Logger, 'info')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_success_one_source_log_to_file(
        self, mock_parser, mock_log_info
    ):
        entries = [
            {
                'title': 'title1',
                'summary': 'summary1',
                'link': 'link1',
                'tags': [{'term': 'term'}],
                'comments': 'comments',
                'published': '2014-02-05 09:00:00+00:00',
                'id': 'id'
            }
        ]
        mock_parser.return_value = ParsedRssResult(entries=entries)
        log_file_location = os.path.join(settings.BASE_DIR, 'unit_test.log')
        call_command(
            'fetch_article', log='unit_test.log',
            sources='https://www.feedforall.com/blog-feed.xml'
        )
        # one info log for fetching, one info log for creating object
        self.assertEqual(2, mock_log_info.call_count)
        self.assertEqual(1, Article.objects.count())
        self.assertTrue(os.path.isfile(log_file_location))
        os.remove(log_file_location)

    @mock.patch.object(logging.Logger, 'info')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_success_two_sources(self, mock_parser, mock_log_info):
        entries1 = [
            {
                'title': 'title1',
                'summary': 'summary1',
                'link': 'link1',
                'tags': [{'term': 'term'}],
                'comments': 'comments',
                'published': '2014-02-05 09:00:00+00:00',
                'id': 'id'
            }
        ]
        entries2 = [
            {
                'title': 'title2',
                'summary': 'summary2',
                'link': 'link2',
                'tags': [{'term': 'term'}],
                'comments': 'comments',
                'published': '2014-02-05 09:00:00+00:00',
                'id': 'id'
            }
        ]
        mock_parser.side_effect = [
            ParsedRssResult(entries=entries1),
            ParsedRssResult(entries=entries2)
        ]

        out = StringIO()
        call_command(
            'fetch_article', stdout=out,
            sources='abc,def'
        )
        # one info log for fetching, one info log for creating object
        self.assertEqual(4, mock_log_info.call_count)
        self.assertEqual(2, Article.objects.count())

    @mock.patch.object(logging.Logger, 'info')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_succes_one_source_existed_article(
        self, mock_parser, mock_log_info
    ):
        ArticleFactory.create(
            title='title',
            description='summary',
            link='link',
            category='term',
            comments='comments',
            guid='id',
            pub_date=parser.parse('2014-02-05 09:00:00+00:00')
        )
        entries = [
            {
                'title': 'title',
                'summary': 'summary',
                'link': 'link',
                'tags': [{'term': 'term'}],
                'comments': 'comments',
                'published': '2014-02-05 09:00:00+00:00',
                'id': 'id'
            }
        ]
        mock_parser.return_value = ParsedRssResult(entries=entries)

        out = StringIO()
        call_command(
            'fetch_article', stdout=out,
            sources='https://www.feedforall.com/blog-feed.xml'
        )
        # one info log for fetching, one info log for creating object
        self.assertEqual(2, mock_log_info.call_count)
        self.assertEqual(1, Article.objects.count())

    @mock.patch.object(logging.Logger, 'info')
    @mock.patch.object(logging.Logger, 'debug')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_success_one_source_no_category(
        self, mock_parser, mock_log_debug, mock_log_info
    ):
        entries = [
            {
                'title': 'title1',
                'summary': 'summary1',
                'link': 'link1',
                'tags': [],
                'comments': 'comments',
                'published': '2014-02-05 09:00:00+00:00',
                'id': 'id'
            }
        ]
        mock_parser.return_value = ParsedRssResult(entries=entries)

        out = StringIO()
        call_command(
            'fetch_article', stdout=out,
            sources='https://www.feedforall.com/blog-feed.xml'
        )
        # one info log for fetching, one info log for creating object
        self.assertEqual(2, mock_log_info.call_count)
        self.assertEqual(1, mock_log_debug.call_count)
        self.assertEqual(1, Article.objects.count())

    @mock.patch.object(logging.Logger, 'info')
    @mock.patch.object(logging.Logger, 'debug')
    @mock.patch.object(feedparser, 'parse')
    def test_run_command_success_one_source_no_published(
            self, mock_parser, mock_log_debug, mock_log_info
    ):
        entries = [
            {
                'title': 'title1',
                'summary': 'summary1',
                'link': 'link1',
                'tags': [{'term': 'term'}],
                'comments': 'comments',
                'published': '',
                'id': 'id'
            }
        ]
        mock_parser.return_value = ParsedRssResult(entries=entries)

        out = StringIO()
        call_command(
            'fetch_article', stdout=out,
            sources='https://www.feedforall.com/blog-feed.xml'
        )
        # one info log for fetching, one info log for creating object
        self.assertEqual(2, mock_log_info.call_count)
        self.assertEqual(1, mock_log_debug.call_count)
        self.assertEqual(1, Article.objects.count())
