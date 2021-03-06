import logging
from bs4 import BeautifulSoup as soup
from . import data_types, shared, exceptions

log = logging.getLogger(__name__)

SITE_URL = shared.SITE_URL

# everything related to cleaning up the data from AnidbFetcher
def search_data(raw_data):
    """Clean up raw search content into storage"""
    sauce = soup(raw_data, "html.parser")

    url_title = sauce.title.string
    log.debug(f"Got page title: {url_title}")

    url_link = sauce.find("link", {"property": "og:url"})["href"]
    log.debug(f"Got page url: {url_link}")

    raw_search_tab = sauce.find("div", {"class": "animelist_list"})
    # janky way to check if request has returned empty results
    if not raw_search_tab.tbody:
        log.warning("No valid search data has been found, raising exception")
        raise exceptions.NoSearchResults(url_link)

    raw_search_results = raw_search_tab.tbody.find_all("tr")
    for item in raw_search_results:
        raw_id = item.get("id", None)
        if not raw_id:
            # coz it should be there for every item, I guess
            log.debug("Couldnt find item's id, skippin")
            continue

        if raw_id.startswith("a"):
            item_id = int(raw_id.replace("a", ""))
        else:
            # this isnt the best way to do things, I guess
            item_id = int(raw_id)
        log.debug(f"Got id: {item_id}")

        # I could easily do this with enumerator, but it wouldnt be consistent
        number = int(item.find("td", {"class": "number"}).text)
        log.debug(f"Got item number: {number}")

        raw_image = item.find("td", {"data-label": "Image"})
        if raw_image:
            image = raw_image.source.get("srcset", None)
            log.debug(f"Got cover image link {image}")
        else:
            image = ""
            log.debug("Couldnt find cover image, using placeholder")

        raw_title = item.find("td", {"class": "name main anime"})
        # this will crash if doesnt exist, but it shouldnt happen
        raw_url = raw_title.a["href"]
        anime_url = SITE_URL + raw_url
        log.debug(f"Got anime url: {anime_url}")
        anime_title = raw_title.a.string
        log.debug(f"Got anime title: {anime_title}")

        # not checking for awards right now, coz Im lazy #TODO
        # print(item.find_all("td"))
        # print(item.find_all("td", title=lambda value: value and value.startswith("type")))

        # print(item.find("td", "class"="type"))


def anime_data(raw_data: str):
    """Cleans up raw anime page content into storage"""
    sauce = soup(raw_data, "html.parser")

    url_title = sauce.title.string
    log.debug(f"Got page title: {url_title}")

    # this is not the most efficient thing since we should already know url
    # from response of requests. Also it may break. But for now it will do
    url_link = sauce.find("link", {"property": "og:url"})["href"]
    log.debug(f"Got page url: {url_link}")

    # checking page's title to find if it returned adult content warning
    # Idk if it may break at some point or not
    if url_title.count("Adult Content Warning"):
        log.warning("Got adult content warning, raising exception")
        raise exceptions.AdultContentWarning(url_link)

    raw_info_tab = sauce.find("div", {"class": "tabbed_pane"})
    # we are doing like that here and below, coz items may have unconfirmed
    # (g_odd {itemname}) and confirmed ({itemname}) properties. Sometimes both
    raw_main_title = raw_info_tab.find(
        "tr", {"class": "g_odd romaji"}
    ) or raw_info_tab.find("tr", {"class": "romaji"})

    # since raw title info should only contain one tag of each type, it should
    # be possible to pass things like that
    main_title = raw_main_title.td.span.string
    log.debug(f"Got main title: {main_title}")

    def get_titles(raw_data, official=False):
        titles = []
        label = raw_data.td.label.string
        for lang in item.td.span.find_all("span", recursive=False):
            # dirty workaround to avoid getting verification icons there
            if "i_state_verified" in lang.get("class"):
                continue

            l = lang.get("title", None)
            if not l:
                continue

            lngs = l.split(": ")
            if len(lngs) != 2:
                continue

            language = lngs[1]
            language_short = lang.string

            item_data = data_types.Title(
                title=label,
                language=language,
                language_short=language_short,
                verified=official,
            )
            log.debug(f"Got label: {item_data}")
            titles.append(item_data)

        return titles

    verified_titles = raw_info_tab.find_all(
        "tr", {"class": "official verified yes"}
    ) + raw_info_tab.find_all("tr", {"class": "g_odd official verified yes"})

    official_titles = {}
    official_titles["verified"] = {}
    official_titles["unverified"] = {}
    for item in verified_titles:
        titles = get_titles(item, official=True)

        for item in titles:
            official_titles["verified"][item.language] = item

    unverified_titles = raw_info_tab.find_all(
        "tr", {"class": "official verified no"}
    ) + raw_info_tab.find_all("tr", {"class": "g_odd official verified no"})

    for item in unverified_titles:
        titles = get_titles(item, official=False)

        for item in titles:
            official_titles["unverified"][item.language] = item

    log.debug(f"Got following titles: {official_titles}")

    raw_show_type = raw_info_tab.find(
        "tr", {"class": "g_odd type"}
    ) or raw_info_tab.find("tr", {"class": "type"})
    # this will return both type and length
    show_type = raw_show_type.td.text
    log.debug(f"Got show type: {show_type}")

    raw_airing = raw_info_tab.find("tr", {"class": "year"})
    airing = raw_airing.td.text
    log.debug(f"Got airing dates: {airing}")

    raw_tags_info = raw_info_tab.find(
        "tr", {"class": "g_odd tags"}
    ) or raw_info_tab.find("tr", {"class": "tags"})
    raw_tags_list = raw_tags_info.find_all("a", {"class": "tooltip"})
    tags = {}
    for item in raw_tags_list:
        url = item.get("href", None)
        if url:
            url = SITE_URL + url
        description = item.find("span", {"class": "wrapper"}).span.text
        name = item.find("span", {"class": "tagname"}).text

        item_data = data_types.Tag(name=name, description=description, link=url)
        log.debug(f"Got tag: {item_data}")
        tags[name] = item_data
    log.debug(f"Got tags:{tags}")

    raw_resources = raw_info_tab.find("tr", {"class": "resources"})
    resources = {}
    for item in raw_resources.td.find_all("div"):
        url = item.a.get("href", None)
        title = item.a.get("title", None)
        # I could also parse link's group, but not doing it rn
        item_data = data_types.Url(name=title, link=url)
        log.debug(f"Got url: {item_data}")
        resources[title] = item_data
    log.debug(f"Got resources:{resources}")

    scores = {}

    def get_score(raw_data):
        # coz its the same structure for all of these below, except for top tr
        name = raw_data.th.text
        url = raw_data.td.a.get("href", None)
        if url:
            url = SITE_URL + url
        value = raw_data.td.a.span.text
        # avoiding the issue with accident string-to-float conversion
        if value == "N/A":
            value = 0

        item_data = data_types.Score(name=name, link=url, value=float(value))
        log.debug(f"Got rating: {item_data}")
        return item_data

    raw_rating = raw_info_tab.find(
        "tr", {"class": "g_odd rating"}
    ) or raw_info_tab.find("tr", {"class": "rating"})
    rating_data = get_score(raw_rating)
    scores[rating_data.name] = rating_data

    raw_average = raw_info_tab.find(
        "tr", {"class": "g_odd tmprating"}
    ) or raw_info_tab.find("tr", {"class": "tmprating"})
    average_data = get_score(raw_average)
    scores[average_data.name] = average_data

    raw_review_rating = raw_info_tab.find(
        "tr", {"class": "g_odd reviews"}
    ) or raw_info_tab.find("tr", {"class": "reviews"})
    review_rating_data = get_score(raw_review_rating)
    scores[review_rating_data.name] = review_rating_data

    log.debug(f"Got scores:{scores}")

    # we dont include added_by and edited_by, coz author is hidden from anon
    # this may be useful in future to track page's changes, tho #TODO

    # I will also add description and link to cover image there, coz it would
    # make sense. Then call it a day
    raw_description = sauce.find("div", {"class": "g_bubble g_section desc resized"})
    description = raw_description.text
    # removing newline at the end of some descriptions
    # if description.endswith("\n\t"):
    # description = description[:-4]
    log.debug(f"Got description: {description}")

    raw_cover = sauce.find("meta", {"property": "og:image"})
    cover_image = raw_cover.get("content", None)
    log.debug(f"Got cover image link: {cover_image}")

    raw_staff = sauce.find("div", {"class": "g_section g_bubble staff"})
    staff = {}
    for category in raw_staff.find_all("tr", {"class": "g_odd"}):
        item = category.find_all("td")
        name = item[0].text
        # workaround for newlines at the end of name
        name = name.replace("\n", "")

        authors = []
        for i in item[1]:
            # workaround for random string errors, I didnt manage to debug #TODO
            try:
                author = data_types.Url(name=i.text, link=SITE_URL + i["href"])
            except:
                pass
            else:
                authors.append(author)

        staff[name] = authors
    log.debug(f"Got staff data: {staff}")

    anime_info = data_types.AnimeInfo(
        main_title=main_title,
        titles=official_titles,
        show_type=show_type,
        airing=airing,
        tags=tags,
        resources=resources,
        scores=scores,
        description=description,
        cover_url=cover_image,
        staff=staff,
    )

    data = data_types.AnidbPage(title=url_title, url=url_link, content=anime_info)

    log.debug(f"Collected following data total:{data}")

    return data
