import pytest
import anidb_parser
from time import sleep

# @pytest.mark.parametrize("text, category", [('boku no', None),
                                            # ('boku no', 'anime'),
                                            # ('boku no', 'ANIME'),
                                            # ('boku no', 'asda'),
                                            # (4546, '235')])
# def test_search_pass(text, category):
    # #waiting between requests to avoid getting 403
    # sleep(10)
    # fetcher = anidb_parser.AnidbFetcher()
    # result = fetcher.search(text, category)

    # assert isinstance(result, str)

# def test_search_fail(text = 'boku no', category = 14124):
    # fetcher = anidb_parser.AnidbFetcher()

    # with pytest.raises(AttributeError):
        # result = fetcher.search(text, category)

# @pytest.mark.parametrize("item, category", [(123, None),
                                            # ('123', None),
                                            # (123, 'anime'),
                                            # (123, 'ANIME'),
                                            # (123, 'asda')])
# def test_getter(item, category):
    # sleep(10)
    # fetcher = anidb_parser.AnidbFetcher()

    # result = fetcher.get_item(item, category)

    # assert isinstance(result, str)

# #4544 should fail right now due to adult content warning - for now, I have no idea
# #how to handle these. Also last one should fail coz no matching results has been
# #found - I need to somehow handle it too
# @pytest.mark.parametrize("animu", [(99), (10475), (11829),
                                   # ("Samurai Champloo"),
                                   # ("saMuRai CHAMPLOO"),
                                   # ("saMuRai_CHAMPLOO")])
# def test_getting_animu(animu):
    # sleep(5)
    # fetcher = anidb_parser.AnidbFetcher(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
    # client = anidb_parser.AnidbClient(fetcher_instance = fetcher)

    # result = client.get_anime(animu)

    # assert isinstance(result, anidb_parser.Anime)

def test_no_results(animu = "saMuRai_CHAMPLOO 12412"):
    fetcher = anidb_parser.AnidbFetcher(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
    client = anidb_parser.AnidbClient(fetcher_instance = fetcher)

    with pytest.raises(anidb_parser.exceptions.NoSearchResults):
        result = client.get_anime(animu)

def test_adult_warning(animu = 4544):
    fetcher = anidb_parser.AnidbFetcher(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
    client = anidb_parser.AnidbClient(fetcher_instance = fetcher)

    with pytest.raises(anidb_parser.exceptions.AdultContentWarning):
        result = client.get_anime(animu)
