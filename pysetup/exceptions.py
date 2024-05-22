class RequiredFieldError(Exception):
    '''Raised when an input is == ""'''

    def __init__(self, data: str):
        """Raised when an input is == ""
        :param data: Additional error data, tipically ``format_exc()``
        :type data: str
        :param func: The function that raised this error
        :type func: str"""

        message = f"RequiredFieldError: {data}"
        super().__init__(message)
