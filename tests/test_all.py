import pytest
import anidb_parser as anidb_crawler

@pytest.mark.parametrize("text, category", [('boku no', None),
                                            ('boku no', 'anime'),
                                            ('boku no', 'ANIME'),
                                            ('boku no', 'asda'),
                                            (4546, '235')])
def test_search_pass(text, category):
    fetcher = anidb_crawler.AnidbFetcher()
    result = fetcher.search(text, category)

    assert isinstance(result, str)

def test_search_fail(text = 'boku no', category = 14124):
    fetcher = anidb_crawler.AnidbFetcher()

    with pytest.raises(AttributeError):
        result = fetcher.search(text, category)

@pytest.mark.parametrize("item, category", [(123, None),
                                            ('123', None),
                                            (123, 'anime'),
                                            (123, 'ANIME'),
                                            (123, 'asda')])
def test_getter(item, category):
    fetcher = anidb_crawler.AnidbFetcher()

    result = fetcher.get_item(item, category)

    assert isinstance(result, str)

@pytest.mark.parametrize("animu", [(99), (10475)])
def test_getting_animu(animu):
    fetcher = anidb_crawler.AnidbFetcher(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
    client = anidb_crawler.AnidbClient(fetcher_instance = fetcher)

    result = client.get_anime(animu)

    assert isinstance(result, anidb_crawler.Anime)
