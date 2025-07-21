"""
The module provides some base embeds classes, ErrorEmbed, SuccessEmbed, WarningEmbed, InfoEmbed.
"""

from disnake import Embed, Color
from datetime import datetime


class ErrorEmbed(Embed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
        timestamp=datetime.now(),
        colour=...,
    ):
        super().__init__(
            title=":red_circle: Information",
            type=type,
            description=description,
            url=url,
            timestamp=timestamp,
            colour=colour,
            color=Color.red(),
        )


class SuccessEmbed(Embed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
        timestamp=datetime.now(),
        colour=...,
    ):
        super().__init__(
            title=":green_circle: Success",
            type=type,
            description=description,
            url=url,
            timestamp=timestamp,
            colour=colour,
            color=Color.green(),
        )


class WarningEmbed(Embed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
        timestamp=datetime.now(),
        colour=...,
    ):
        super().__init__(
            title=":yellow_circle: Warning",
            type=type,
            description=description,
            url=url,
            timestamp=timestamp,
            colour=colour,
            color=Color.yellow,
        )


class InfoEmbed(Embed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
        timestamp=datetime.now(),
        colour=...,
    ):
        super().__init__(
            title=":blue_circle: Information",
            type=type,
            description=description,
            url=url,
            timestamp=timestamp,
            colour=colour,
            color=Color.blue(),
        )


__all__ = (
    "ErrorEmbed",
    "SuccessEmbed",
    "WarningEmbed",
    "InfoEmbed",
)
