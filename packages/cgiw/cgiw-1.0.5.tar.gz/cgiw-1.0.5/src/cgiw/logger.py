from logging import getLogger, basicConfig
from os import getenv

logger = getLogger()

LOG_FILE_LOCATION = getenv("LOG_FILE_LOCATION", "log")

basicConfig(filename=LOG_FILE_LOCATION)
