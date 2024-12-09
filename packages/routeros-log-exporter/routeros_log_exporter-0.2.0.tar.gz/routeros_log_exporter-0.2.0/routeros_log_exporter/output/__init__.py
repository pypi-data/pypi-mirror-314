# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Thread
from typing import Any, Dict, Type
from queue import Queue


class Output(Thread):
    registered_outputs: Dict[str, Type["Output"]] = {}

    def __init__(self, queue_size: int = 0):
        super().__init__()
        self._queue: Queue = Queue(maxsize=queue_size)

    def handle_signal(self, signal_number):
        pass

    @property
    def queue(self):
        return self._queue

    def run(self):
        raise NotImplementedError

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "Output":
        raise NotImplementedError

    @classmethod
    def register(cls, name: str, output_cls: Type["Output"]):
        cls.registered_outputs[name] = output_cls
