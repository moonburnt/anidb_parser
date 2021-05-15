# For dataclasses and dataclass storages used across this package's modules
# These are used instead of dictionaries to ease throwing incorrect data away
# later with isinstance() check
from dataclasses import dataclass

class Anime:
    pass

# #@dataclass
# class AnimeInfo:
    # pass

class TitleStorage:
    pass

@dataclass
class Title:
    title: str
    language: str
    language_short: str = ""
    verified: bool = False

#@dataclass
class TagStorage:
    pass
    #tags: list[Tag]

@dataclass
class Tag:
    name: str
    link: str = ""
    description: str = ""

class UrlStorage:
    pass

@dataclass
class Url:
    name: str
    link: str
    description: str = ""

class ScoreStorage:
    pass

@dataclass
class Score:
    name: str
    value: float
    link: str = ""

class ReviewStorage:
    pass

class Review:
    pass

class SearchStorage:
    pass

@dataclass
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
