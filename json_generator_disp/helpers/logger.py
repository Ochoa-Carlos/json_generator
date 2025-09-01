import logging


class CustomLogFormatter(logging.Formatter):
    """Set a custom fomart for logs."""
    purple = "\033[38;5;33m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = """|  [%(asctime)s]|  [%(levelname)s]  | [%(module)s].%(funcName)s:%(lineno)d: MSG -> %(message)s"""

    FORMATS = {
        logging.DEBUG: purple + format + reset,
        logging.INFO: purple + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

json_logger = logging.getLogger("json_service")
json_logger.setLevel(logging.DEBUG)

json_handler = logging.StreamHandler()
json_handler.setLevel(logging.DEBUG)

ukituki_formatter = logging.Formatter(
   "\n[%(asctime)s]|  [%(levelname)s]    |  [%(module)s]:%(funcName)s:%(lineno)d: MSG -> %(message)s"
   )

json_handler.setFormatter(CustomLogFormatter())
json_logger.addHandler(json_handler)


def logger() -> logging:
    """Return custom logger."""
    return logging.getLogger("json_service")
