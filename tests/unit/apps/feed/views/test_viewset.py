from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.feed.models import Article
from tests.unit.factories import ArticleFactory


class TestArticleViewset(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='foo', password='bar')
        cls.user.is_superuser = True
        cls.user.is_staff = True
        cls.user.save()

    def setUp(self):
        super().setUp()

        ArticleFactory.create_batch(10)
        self.article = ArticleFactory.create()

        self.list_url = reverse('feed:article_list')
        self.add_url = reverse('feed:article_add')
        self.detail_url = reverse(
            'feed:article_detail', kwargs={'pk': self.article.id}
        )
        self.delete_url = reverse(
            'feed:article_delete', kwargs={'pk': self.article.id}
        )
        self.change_url = reverse(
            'feed:article_change', kwargs={'pk': self.article.id}
        )
        self.post_data = {
            'title': 'title',
            'description': 'description',
            'link': 'link',
            'category': 'category',
            'comments': 'comments',
            'guid': 'guid',
            'pub_date': '2020-06-25 22:00:56'
        }

    def tearDown(self):
        Article.objects.all().delete()

    def test_get_list_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(11, len(response.context['object_list']))
        self.assertEqual(self.article, response.context['object_list'][0])

    def test_get_list_failed_by_unauthorized_user(self):
        response = self.client.get(self.list_url)
        self.assertEqual(302, response.status_code)

    def test_get_add_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.add_url)

        self.assertEqual(200, response.status_code)

    def test_get_add_failed_by_unauthorized_user(self):
        response = self.client.get(self.add_url)
        self.assertEqual(403, response.status_code)

    def test_post_add_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_url, data=self.post_data
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(12, Article.objects.count())
        self.assertTrue(
            Article.objects.filter(
                title='title',
                description='description',
                link='link',
                category='category',
                comments='comments',
                guid='guid',
                pub_date=timezone.datetime(2020, 6, 25, 22, 00, 56)
            ).exists()
        )

    def test_post_add_failed_by_unauthorized(self):
        response = self.client.post(
            self.add_url, data=self.post_data
        )
        self.assertEqual(403, response.status_code)

    def test_get_detail_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.article, response.context['object'])

    def test_get_detail_failed_by_unauthorized_user(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(403, response.status_code)

    def test_get_detailed_failed_by_unknown_id(self):
        url = reverse(
            'feed:article_detail', kwargs={'pk': uuid4()}
        )
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_get_delete_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.delete_url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.article, response.context['object'])

    def test_get_delete_failed_by_unauthorized(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(403, response.status_code)

    def test_get_delete_failed_by_unknown_id(self):
        url = reverse(
            'feed:article_delete', kwargs={'pk': uuid4()}
        )
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_post_delete_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.delete_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(10, Article.objects.count())

    def test_post_delete_failed_by_unauthorized(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(403, response.status_code)

    def test_post_delete_failed_by_unknown_id(self):
        url = reverse(
            'feed:article_delete', kwargs={'pk': uuid4()}
        )
        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(404, response.status_code)

    def test_get_change_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.change_url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.article, response.context['object'])

    def test_get_change_failed_by_unauthorized(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(403, response.status_code)

    def test_get_change_failed_by_unknown_id(self):
        url = reverse(
            'feed:article_change', kwargs={'pk': uuid4()}
        )
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_post_change_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.change_url, data=self.post_data
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(11, Article.objects.count())
        self.assertTrue(
            Article.objects.filter(
                title='title',
                description='description',
                link='link',
                category='category',
                comments='comments',
                guid='guid',
                pub_date=timezone.datetime(2020, 6, 25, 22, 00, 56)
            ).exists()
        )

    def test_post_change_failed_by_unauthorized(self):
        response = self.client.post(self.change_url, data=self.post_data)
        self.assertEqual(403, response.status_code)

    def test_post_change_failed_by_unknown_id(self):
        url = reverse(
            'feed:article_change', kwargs={'pk': uuid4()}
        )
        self.client.force_login(self.user)
        response = self.client.post(url, data=self.post_data)
        self.assertEqual(404, response.status_code)
