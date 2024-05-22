from platform import system
from .exceptions import RequiredFieldError, general_logger

LOGGER_PATH = "_funcs"


def is_win() -> bool:
    """Cheks if os is windows

    :return: True if OS is Windows else False
    :rtype: bool"""
    return system() == "Windows"


def univoque(text: str) -> str:
    """Text passed is returned as univoque string

    :param text: The text to modify
    :type text: str

    :return: The modified text
    :rtype: str
    """
    return text.replace(" ", "").lower()


def check_string(text: str, required: bool = False) -> str:
    """Checks if the string is different from ""

    :param text: The string to check
    :type text: str
    :param required: Wether the string is required or not, defaults to False
    :type required: bool, optional

    :return: The text passed if the field is valid or // if the text is not requried and == ""
    :rtype str

    :raises:
        * RequiredFieldError if the text is required and == ""
    """

    FUNC_PATH = "check_string"

    general_logger.info(f"Checking string: {text}", f"{LOGGER_PATH}.{FUNC_PATH}")

    if text.replace(" ", "") == "":
        if required:
            raise RequiredFieldError(
                "The field is required", f"{LOGGER_PATH}.{FUNC_PATH}"
            )
        else:
            general_logger.success("Check string => //", f"{LOGGER_PATH}.{FUNC_PATH}")
            return "//"

    general_logger.success("String is valid", f"{LOGGER_PATH}.{FUNC_PATH}")
    return text


def generate_file(text: str, filename: str) -> None:
    """Generates the given file with custom text

    :param text: The text to insert in the file
    :type text: str
    :param filename: The file name
    :type filename: str
    """

    with open(filename, mode="w") as new_file:
        new_file.write(text)
