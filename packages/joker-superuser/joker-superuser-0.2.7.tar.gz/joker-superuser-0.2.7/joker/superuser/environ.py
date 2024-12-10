#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import joker.meta


class JokerInterface(joker.meta.JokerInterface):
    package_name = "joker.superuser"

    default_config = {
        "urls": {
            "youtube.com/watch": ["v"],
            "youtube.com/playlist": ["list"],
        }
    }
