"""
Module contains `logger` object to interact with bot logs
"""

from logging import FileHandler, StreamHandler, getLogger, basicConfig

from .configuration import LOGGING_FILENAME

basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        StreamHandler(),
        FileHandler(
            filename=LOGGING_FILENAME,
            mode="w",
            encoding="utf-8",
        ),
    ],
)
logger = getLogger(__file__)

__all__ = ("logger",)
