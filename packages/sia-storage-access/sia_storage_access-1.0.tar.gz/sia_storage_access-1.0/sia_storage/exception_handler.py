import logging


class SiaAzureException(Exception):
    """
    Customized Exception class which accepts exception original error message
    along with user defined custom error message. It overrides the __str__
    to print custom error message along with complete stack trace.
    """

    def __init__(self, real_error_message, custom_error_message):
        super().__init__(real_error_message)
        self.custom_error_message = custom_error_message
        self.real_error_message = real_error_message
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        self.logger.info(self.__traceback__)
        return f"{self.real_error_message} (Custom Error Message: {self.custom_error_message})"
