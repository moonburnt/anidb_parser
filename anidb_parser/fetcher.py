import logging
from requests import Session
from . import shared

log = logging.getLogger(__name__)

SITE_URL = shared.SITE_URL
TIMEOUT = 30

class AnidbFetcher:
    '''Class dedicated to obtaining various raw data from anidb'''
    def __init__(self, timeout:int = 0, user_agent:str = None):
        #Using the recommended way to fetch data
        self.session = Session()

        #ensuring that timeout wont be negative value
        self.timeout = max(timeout, 0) or TIMEOUT

        if user_agent:
            self.session.headers.update({'user-agent': user_agent})

        #dict with valid item categories. Name of dict is the same as search
        #category would appear on site, and value is what appears in search url
        self.item_categories = {'anime': 'anime',
                                'character': 'character',
                                'club': 'club',
                                'collections': 'collection',
                                'creator': 'creator',
                                'episodes': 'episode',
                                'group': 'group',
                                #'mylist' isnt there, coz it requires auth
                                'songs': 'song',
                                'tags': 'tag'}
                                #same for user
                                #'user': 'user'}

        #expanding item categories to include items that only exist for search
        #purposes and never actually used anywhere else
        search_exclusive_categories = {'all': 'search/anime'}
        self.search_categories = self.item_categories | search_exclusive_categories

    def fetch_url(self, url:str):
        '''Fetches url, checks response code and returns response content.
        Only meant for internal usage'''
        log.debug(f"Fetching {url}")
        answer = self.session.get(url, timeout = self.timeout)
        answer.raise_for_status()

        #returning raw answer object, because due to redirects we may need to
        #double check answer.url to proceed
        return answer

    #there is also "advanced search", but I wont bother with it for now
    def search(self, text:str, category:str = None):
        '''Search for specified info in provided category'''
        if category:
            #ensuring that it will be in lowercase
            category = category.lower()

        if not category or not category in self.search_categories:
            category = "all"

        search_url = f"{SITE_URL}/{self.search_categories[category]}/?adb.search={text}"

        #return answer.text
        return self.fetch_url(search_url)

    def get_item(self, item_id:int, category:str = None):
        '''Get info of provided item in provided category'''
        if category:
            #ensuring that it will be in lowercase
            category = category.lower()

        if not category or not category in self.item_categories:
            #Assuming that if category isnt set, we are searching for anime
            category = "anime"

        search_url = f"{SITE_URL}/{self.item_categories[category]}/{item_id}"

        return self.fetch_url(search_url)

