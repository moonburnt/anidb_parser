# custom exceptions used by this library


class AnidbExeption(Exception):
    """Parent exception class for all custom exceptions"""

    pass


class ParserException(AnidbExeption):
    """Undefined exception thrown by parser"""

    pass


class PageDoesntExist(AnidbExeption):
    """Exception thrown if web page queued to process doesnt exist"""

    pass


class PageUnavailable(ParserException):
    """Exception thrown if web page queued to process exists, but isnt available
    to parse at the moment (for unknown reasons)"""

    pass


class NoSearchResults(ParserException):
    """Exception thrown if search request has returned no results"""

    def __init__(self, url):
        message = f"{url} has returned no results"
        super().__init__(message)


class AdultContentWarning(ParserException):
    """Exception thrown by anime pages that cant be processed due to Adult Content
    Warning pop-up that naturally require user to log in"""

    def __init__(self, url):
        message = f"{url} has returned Adult Content Warning"
        super().__init__(message)
