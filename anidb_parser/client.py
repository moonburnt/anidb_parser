import logging
from . import fetcher, processor

log = logging.getLogger(__name__)

class AnidbClient:
    '''Default way to make fetcher and processor communicate.
    Its strongly recommended to pass custom fetcher_insance, initialized with real
    browser's user_agent, because by default anidb bans all automated requests'''
    def __init__(self, fetcher_instance = None, processor_instance = None):
        #if not passed manually - these are instanced with no args, for now
        if not fetcher_instance or not isinstance(fetcher_instance, fetcher.AnidbFetcher):
            self.fetcher = fetcher.AnidbFetcher()
        else:
            self.fetcher = fetcher_instance

        if not processor_instance or not isinstance(processor_instance, processor.AnidbProcessor):
            self.processor = processor.AnidbProcessor()
        else:
            self.processor = processor_instance

        #self.fetcher = fetcher_instance or fetcher.AnidbFetcher()
        #self.processor = processor_instance or fetcher.AnidbProcessor()

    def get_anime(self, anime):
        '''Get provided anime. Receives either id or name to search it'''
        if isinstance(anime, int):
            log.debug(f"Attempting to fetch anime with id {anime}")
            data = self.fetcher.get_item(anime, category = "anime")
        else:
            log.debug(f"Attempting to find anime matching search {anime}")
            #this will return not animu's page, but multiple search entries, in
            #case there are multiple matches
            data = self.fetcher.search(anime, category = "anime")
            #checking if request has still returned search page or redirected us
            #to anime's own page (happens if only one match to request has found)
            #It may be now the most optimal way to return two different answer's
            #contents, but since they have different classes, we can later filter
            #results out with isinstance() and proceed accordingly
            if data.url.count("search"):
                log.debug("Received search results, processing accordingly")
                clean_data = self.processor.search_data(data.text)
                return clean_data

        log.debug("Received anime data, processing accordingly")
        clean_data = self.processor.anime_data(data.text)

        return clean_data
