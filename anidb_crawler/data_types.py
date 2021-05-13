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
