import pytest


@pytest.mark.django_db
class TestSource:
    @pytest.mark.parametrize("news_source__title", ["source1"])
    def test_str(self, news_source):
        assert str(news_source) == f"{news_source.title}"


@pytest.mark.django_db
class TestNews:
    @pytest.mark.parametrize("news__title", ["new1"])
    def test_str(self, news):
        assert str(news) == f"{news.title} ({news.source.title})"
