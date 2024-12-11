class AnuraException(Exception):
    """
    Raised when an error is returned from the Anura Direct API.
    """
    pass

class AnuraServerException(AnuraException):
    """
    Raised when a 5XX response is returned from the Anura Direct API.
    """
    pass

class AnuraClientException(AnuraException):
    """
    Raised when a 4XX response is returned from the Anura Direct API.
    """
    pass