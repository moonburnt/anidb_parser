import logging
from bs4 import BeautifulSoup as soup
from . import data_types, shared

log = logging.getLogger(__name__)

SITE_URL = shared.SITE_URL

class AnidbProcessor:
    '''Class dedicated to cleaning up the data from AnidbFetcher'''
    def __init__(self):
        pass

    def search_data(self, raw_data:str):
        '''Clean up raw search response into dictionary with only useful stuff'''
        sauce = soup(raw_data, 'html.parser')

        data = data_types.SearchStorage()

        raw_search_tab = sauce.find("div", {"class": "animelist_list"})
        raw_search_results = raw_search_tab.tbody.find_all("tr")
        for item in raw_search_results:
            raw_id = item.get('id', None)
            if not raw_id:
                #coz it should be there for every item, I guess
                continue
            if raw_id.startswith('a'):
                item_id = int(raw_id.replace('a', ''))
            else:
                #this isnt the best way to do things, I guess
                item_id = int(raw_id)

            number = int(item.find("td", {"class": "number"}).text)

            raw_image = item.find("td", {"data-label": "Image"})
            if raw_image:
                image = raw_image.source.get('srcset', None)
            else:
                image = ""

    def anime_data(self, raw_data:str):
        '''Cleans up raw anime page text into dict with only useful stuff'''

        sauce = soup(raw_data, 'html.parser')

        data = data_types.Anime()

        data.url_title = sauce.title.string
        log.debug(f"Got page title: {data.url_title}")

        raw_info_tab = sauce.find("div", {"class": "tabbed_pane"})
        #we are doing like that here and below, coz items may have unconfirmed
        #(g_odd {itemname}) and confirmed ({itemname}) properties. Sometimes both
        raw_main_title = (raw_info_tab.find("tr", {"class": "g_odd romaji"}) or
                          raw_info_tab.find("tr", {"class": "romaji"}))

        #since raw title info should only contain one tag of each type, it should
        #be possible to pass things like that
        data.main_title = raw_main_title.td.span.string
        log.debug(f"Got main title: {data.main_title}")

        def get_titles(raw_data, official = False):
            titles = []
            label = raw_data.td.label.string
            for lang in item.td.span.find_all("span", recursive = False):
                #dirty workaround to avoid getting verification icons there
                if 'i_state_verified' in lang.get('class'):
                    continue

                l = lang.get("title", None)
                if not l:
                    continue

                lngs = l.split(": ")
                if len(lngs) != 2:
                    continue

                language = lngs[1]
                language_short = lang.string

                item_data = data_types.Title(title = label,
                                             language = language,
                                             language_short = language_short,
                                             verified = official)
                log.debug(f"Got label: {item_data}")
                titles.append(item_data)

            return titles

        raw_official_verified_titles = raw_info_tab.find_all("tr",
                                        {"class": "official verified yes"})

        raw_official_verified_titles += raw_info_tab.find_all("tr",
                                        {"class": "g_odd official verified yes"})

        data.official_titles = data_types.TitleStorage()
        data.official_titles.verified = data_types.TitleStorage()
        for item in raw_official_verified_titles:
            titles = get_titles(item, official = True)

            for item in titles:
                setattr(data.official_titles.verified, item.language, item)

        log.debug("Got following verified titles: "
                 f"{list(vars(data.official_titles.verified).items())}")

        raw_official_unverified_titles = raw_info_tab.find_all("tr",
                                        {"class": "official verified no"})

        raw_official_unverified_titles += raw_info_tab.find_all("tr",
                                        {"class": "g_odd official verified no"})


        data.official_titles.unverified = data_types.TitleStorage()
        for item in raw_official_unverified_titles:
            titles = get_titles(item, official = False)

            for item in titles:
                setattr(data.official_titles.unverified, item.language, item)

        log.debug("Got following unverified titles: "
                 f"{list(vars(data.official_titles.unverified).items())}")

        raw_show_type = (raw_info_tab.find("tr", {"class": "g_odd type"}) or
                         raw_info_tab.find("tr", {"class": "type"}))
        #this will return both type and length
        data.show_type = raw_show_type.td.text
        log.debug(f"Got show type: {data.show_type}")

        raw_airing = raw_info_tab.find("tr", {"class": "year"})
        data.airing = raw_airing.td.text
        log.debug(f"Got airing dates: {data.airing}")

        raw_tags_info = (raw_info_tab.find("tr", {"class": "g_odd tags"}) or
                         raw_info_tab.find("tr", {"class": "tags"}))
        raw_tags_list = raw_tags_info.find_all("a", {"class": "tooltip"})

        data.tags = data_types.TagStorage()
        for item in raw_tags_list:
            url = item.get('href', None)
            if url:
                url = SITE_URL+url
            description = item.find("span", {"class": "wrapper"}).span.text
            name = item.find("span", {"class": "tagname"}).text

            item_data = data_types.Tag(name = name,
                                       description = description,
                                       link = url)
            log.debug(f"Got tag: {item_data}")
            setattr(data.tags, name, item_data)
        log.debug(f"Got tags:{list(vars(data.tags).items())}")

        raw_resources = raw_info_tab.find("tr", {"class": "resources"})

        data.resources = data_types.UrlStorage()
        for item in raw_resources.td.find_all("div"):
            url = item.a.get('href', None)
            if url:
                url = SITE_URL+url
            title = item.a.get('title', None)
            #I could also parse link's group, but not doing it rn
            item_data = data_types.Url(name = title,
                                       link = url)
            log.debug(f"Got url: {item_data}")
            setattr(data.resources, title, item_data)
        log.debug(f"Got resources:{list(vars(data.tags).items())}")

        data.scores = data_types.ScoreStorage()

        def get_score(raw_data):
            #coz its the same structure for all of these below, except for top tr
            name = raw_data.th.text
            url = raw_data.td.a.get('href', None)
            if url:
                url = SITE_URL+url
            value = raw_data.td.a.span.text
            #avoiding the issue with accident string-to-float conversion
            if value == "N/A":
                value = 0

            item_data = data_types.Score(name = name,
                                         link = url,
                                         value = float(value))
            log.debug(f"Got rating: {item_data}")
            return item_data

        raw_rating = (raw_info_tab.find("tr", {"class": "g_odd rating"}) or
                      raw_info_tab.find("tr", {"class": "rating"}))
        rating_data = get_score(raw_rating)
        setattr(data.scores, rating_data.name, rating_data)

        raw_average = (raw_info_tab.find("tr", {"class": "g_odd tmprating"}) or
                       raw_info_tab.find("tr", {"class": "tmprating"}))
        average_data = get_score(raw_average)
        setattr(data.scores, average_data.name, average_data)

        raw_review_rating = (raw_info_tab.find("tr", {"class": "g_odd reviews"}) or
                             raw_info_tab.find("tr", {"class": "reviews"}))
        review_rating_data = get_score(raw_review_rating)
        setattr(data.scores, review_rating_data.name, review_rating_data)

        log.debug(f"Got scores:{list(vars(data.scores).items())}")

        #that sums up the data we can possibly get from infobox, with the
        #exclusion of added_by and edited_by, coz Im bored #TODO

        #I will also add description and link to cover image there, coz it would
        #make sense. Then call it a day
        raw_description = sauce.find("div",
                                    {"class": "g_bubble g_section desc resized"})
        data.description = raw_description.text
        log.debug(f"Got description: {data.description}")

        raw_cover = sauce.find("meta", {"property": "og:image"})
        data.cover_image = raw_cover.get('content', None)

        log.debug(f"Got cover image link: {data.cover_image}")

        log.debug(f"Collected following data total:{list(vars(data).items())}")

        return data
