import factory

from django.utils import timezone

from apps.feed.models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        strategy = factory.CREATE_STRATEGY

    title = factory.Faker('first_name')
    description = factory.Faker('first_name')
    link = factory.Faker('first_name')
    category = factory.Faker('first_name')
    comments = factory.Faker('first_name')
    guid = factory.Faker('first_name')
    pub_date = timezone.now()
