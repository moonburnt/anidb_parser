import pytest
import anidb_parser
from time import sleep

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
PAUSE_BETWEEN_REQUESTS = 3

@pytest.mark.parametrize("text, category", [('boku no', None),
                                            ('boku no', 'anime'),
                                            ('boku no', 'ANIME'),
                                            ('boku no', 'asda'),
                                            (4546, '235')])
def test_search(text, category):
    #waiting between requests to avoid getting 403
    sleep(PAUSE_BETWEEN_REQUESTS)
    fetcher = anidb_parser.AnidbFetcher(user_agent = USER_AGENT)
    result = fetcher.search(text, category)

    assert isinstance(result.text, str)

@pytest.mark.parametrize("item, category", [(123, None),
                                            ('123', None),
                                            (123, 'anime'),
                                            (123, 'ANIME'),
                                            (123, 'asda')])
def test_getter(item, category):
    sleep(PAUSE_BETWEEN_REQUESTS)
    fetcher = anidb_parser.AnidbFetcher(user_agent = USER_AGENT)

    result = fetcher.get_item(item, category)

    assert isinstance(result.text, str)

@pytest.mark.parametrize("animu", [(99), (10475), (11829),
                                   ("Samurai Champloo"),
                                   ("saMuRai CHAMPLOO"),
                                   ("saMuRai_CHAMPLOO")])
def test_getting_animu(animu):
    sleep(PAUSE_BETWEEN_REQUESTS)
    fetcher = anidb_parser.AnidbFetcher(user_agent = USER_AGENT)
    client = anidb_parser.AnidbClient(fetcher_instance = fetcher)

    result = client.get_anime(animu)

    assert isinstance(result, anidb_parser.Anime)

