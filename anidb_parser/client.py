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
            data = self.fetcher.get_item(anime, category = "anime")
        else:
            #this will return not animu's page, but multiple search entries, in
            #case there are multiple matches. I should probably disable redirects
            #in fetcher and then process this manually
            log.error("Sorry, searching for animu isnt implemented yet")
            return
            data = self.fetcher.search(anime, category = "anime")

        clean_data = self.processor.anime_data(data)
        return clean_data
