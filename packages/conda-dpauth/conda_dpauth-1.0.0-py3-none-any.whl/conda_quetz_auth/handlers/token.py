"""
Token implementation for the conda auth handler plugin hook
"""
from __future__ import annotations

import os
from collections.abc import Mapping

from conda.models.channel import Channel
from conda.plugins.types import ChannelAuthBase

from ..constants import PLUGIN_NAME


class TokenAuthHandler(ChannelAuthBase):
    """
    Implements token auth that inserts a token as a header for all network request
    in conda for the channel specified on object instantiation.

    We make a special exception for quetz server and set the X-API-Key header as:

        X-API-Key: token <token>

    """

    def __init__(self, channel_name: str):
        self.quetz_host = os.getenv("QUETZ_HOST")
        self.quetz_api_key = os.getenv("QUETZ_API_KEY")

        super().__init__(channel_name)

    def __call__(self, request):
        if self.quetz_host and self.quetz_api_key:
            if request.url.lower().startswith(self.quetz_host.lower()):
                request.headers["X-API-Key"] = self.quetz_api_key

        return request