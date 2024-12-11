class YMLException(Exception):
    """
    Basic error for the whole module.
    """

    pass


class ValidationError(YMLException):
    """
    Data validation exception.
    """

    pass


class ParseError(YMLException):
    """
    Base parse exception.
    """

    pass
