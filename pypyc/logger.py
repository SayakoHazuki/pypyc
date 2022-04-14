import logging

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"
format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

FORMATS = {
    logging.DEBUG: grey + format + reset,
    logging.INFO: grey + format + reset,
    logging.WARNING: yellow + format + reset,
    logging.ERROR: red + format + reset,
    logging.CRITICAL: bold_red + format + reset
}


class Formatter(logging.Formatter):

    def format(self, record):
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def logger() -> logging.Logger:
    logger = logging.getLogger('Pypyc')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(Formatter())

    logger.addHandler(ch)
    return logger
