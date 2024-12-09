import logging
from enum import Enum


class LogLevel(Enum):
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


# Configure logging once at the start of your program
logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s :: api-to-dataframe[%(levelname)s] :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    level=logging.INFO,
)


def log(message: str, level: LogLevel):
    logger = logging.getLogger("api-to-dataframe")
    logger.log(level.value, message)
