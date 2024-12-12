import factory
from django.conf.global_settings import LANGUAGES
from django.utils import timezone
from faker import Factory
from wbnews.models import News, NewsSource

langs = [n for (n, v) in LANGUAGES]
faker = Factory.create()


class NewsSourceFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"source_{n}")
    identifier = factory.Sequence(lambda n: f"http://myurl_{n}.com")
    image = faker.url()
    description = factory.Faker("sentence", nb_words=32)
    author = faker.name()
    url = factory.Faker("url")

    class Meta:
        model = NewsSource


class NewsFactory(factory.django.DjangoModelFactory):
    datetime = factory.LazyFunction(timezone.now)
    title = factory.Sequence(lambda n: f"news_{n}")
    description = factory.Faker("sentence", nb_words=32)
    summary = factory.Faker("sentence", nb_words=32)
    language = factory.Iterator(langs)
    link = faker.url()
    source = factory.SubFactory(NewsSourceFactory)

    class Meta:
        model = News
