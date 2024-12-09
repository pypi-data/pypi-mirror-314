# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from typing import Any, Dict, Type


logger = logging.getLogger("format")


class Format:
    registered_formats: Dict[str, Type["Format"]] = {}

    def __init__(self, config: Dict[str, Any]):
        pass

    def process(self, data):
        raise NotImplementedError

    @classmethod
    def register(cls, name: str, format_cls: Type["Format"]):
        cls.registered_formats[name] = format_cls
