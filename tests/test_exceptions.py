import pytest
import anidb_parser
from time import sleep

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
)
PAUSE_BETWEEN_REQUESTS = 3


def test_search_fail(text="boku no", category=14124):
    fetcher = anidb_parser.AnidbFetcher(user_agent=USER_AGENT)

    with pytest.raises(AttributeError):
        result = fetcher.search(text, category)


def test_no_results(animu="saMuRai_CHAMPLOO 12412"):
    fetcher = anidb_parser.AnidbFetcher(user_agent=USER_AGENT)
    client = anidb_parser.AnidbClient(fetcher_instance=fetcher)

    with pytest.raises(anidb_parser.exceptions.NoSearchResults):
        result = client.get_anime(animu)


def test_adult_warning(animu=4544):
    fetcher = anidb_parser.AnidbFetcher(user_agent=USER_AGENT)
    client = anidb_parser.AnidbClient(fetcher_instance=fetcher)

    with pytest.raises(anidb_parser.exceptions.AdultContentWarning):
        result = client.get_anime(animu)
