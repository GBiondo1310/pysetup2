from pylogger import general_logger


class RequiredFieldError(Exception):
    '''Raised when an input is == ""'''

    def __init__(self, data: str, function: str):
        """Raised when an input is == ""
        :param data: Additional error data, tipically ``format_exc()``
        :type data: str
        :param func: The function that raised this error
        :type func: str"""

        message = f"RequiredFieldError: {data}"
        general_logger.error(message, function)
        super().__init__(message)
