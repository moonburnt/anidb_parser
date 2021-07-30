# For data storages used across this package's modules

from dataclasses import dataclass


class WebpageContent:
    pass


# Ensuring that we wont be able to overwrite data
@dataclass(frozen=True)
class AnidbPage:
    title: str
    url: str
    content: WebpageContent


@dataclass(frozen=True)
class Title:
    title: str
    language: str
    language_short: str = ""
    verified: bool = False


@dataclass(frozen=True)
class Tag:
    name: str
    link: str = ""
    description: str = ""


@dataclass(frozen=True)
class Url:
    name: str
    link: str
    description: str = ""


@dataclass(frozen=True)
class Score:
    name: str
    value: float
    link: str = ""


class Review:
    pass


@dataclass(frozen=True)
class AnimeInfo(WebpageContent):
    main_title: str
    show_type: str
    airing: str
    description: str
    cover_url: str
    titles: dict
    tags: dict
    scores: dict
    resources: dict
    staff: dict


class SearchItem:
    pass


@dataclass(frozen=True)
class AnimeSearchPreview:
    number: int
    title: str
    show_type: str
    episodes_count: int = 0
    rating: float = 0.0
    average: float = 0.0
    reviews: int = 0
    user_counter: int = 0
    aired: str = ""
    ended: str = ""
    image: str = ""
    award: str = ""
