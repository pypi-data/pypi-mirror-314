"""Errors used by the NaluConfigs package.

"""

class NaluConfigsException(Exception):
    """Base class for NaluConfigs exceptions, for tracability.
    """


class InvalidBoardModelError(NaluConfigsException):
    """Raised when the board model doesn't exist in the list of models.
    """


class PostProcessingError(NaluConfigsException):
    """Raised when post-processing configuration runs into a problem.
    """

class RangeParsingError(PostProcessingError):
    """Raised when post-processing configuration runs into a problem while
    parsing.
    """

class ConfigurationFileParsingError(NaluConfigsException):
    """Something wrong during the processing of a configuration file."""