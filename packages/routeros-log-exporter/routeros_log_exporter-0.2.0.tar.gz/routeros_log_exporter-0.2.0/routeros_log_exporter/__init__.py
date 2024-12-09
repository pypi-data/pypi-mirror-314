# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import signal
from threading import Thread
import queue
from typing import Dict, List, Type


import yaml

from .fetcher import LogFetcher
from .helper import load_modules
from .output import Output


logger = logging.getLogger("dispatcher")


class Dispatcher(Thread):
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self._should_terminate = False

    def run(self):
        while not self._should_terminate:
            try:
                message = self.queue.get(timeout=2)
            except queue.Empty:
                continue
            self.queue.task_done()
            message.dispatch()

    def stop(self):
        self._should_terminate = True


class Exporter:
    def __init__(self, config_filename: str):
        self._config_filename = config_filename

        self._fetchers: List[LogFetcher] = []
        self._outputs: Dict[str, Output] = {}
        self._dispatcher = Dispatcher()
        load_modules([".output"])
        load_modules([".output.format"])

    def handle_signal(self, signal_number):
        logger.info(f"Propagating signal {signal_number} ({signal.Signals(signal_number).name})")
        for fetcher in self._fetchers:
            fetcher.handle_signal(signal_number)

        for output in self._outputs.values():
            output.handle_signal(signal_number)

    def start(self):
        with open(self._config_filename) as fp:
            data = yaml.safe_load(fp)
            for name, output_config in data["outputs"].items():
                output_cls: Type[Output] = Output.registered_outputs.get(output_config.get("type"))
                self._outputs[name] = output_cls.from_config(config=output_config)
            for device_config in data["devices"]:
                device_config_merged = dict(data.get("device_defaults", {}).items())
                device_config_merged.update(device_config)
                log_fetcher = LogFetcher.from_config(
                    config=device_config_merged,
                    message_queue=self._dispatcher.queue,
                    available_outputs=self._outputs
                )
                self._fetchers.append(log_fetcher)

        logger.info(f"Starting {len(self._outputs)} output threads ...")
        for output_thread in self._outputs.values():
            output_thread.start()

        logger.info(f"Starting {len(self._fetchers)} fetcher threads ...")
        for fetcher_thread in self._fetchers:
            fetcher_thread.start()

        logger.info("Starting dispatcher thread ...")
        self._dispatcher.start()

    def stop(self):
        logger.info(f"Stopping {len(self._fetchers)} fetcher threads ...")
        for fetcher_thread in self._fetchers:
            fetcher_thread.stop()

        logger.info("Stopping dispatcher thread ...")
        self._dispatcher.stop()

        logger.info(f"Stopping {len(self._outputs)} output threads ...")
        for output_thread in self._outputs.values():
            output_thread.stop()

        logger.info(f"Joining {len(self._fetchers)} fetcher threads ...")
        for fetcher_thread in self._fetchers:
            fetcher_thread.join()

        logger.info("Joining dispatcher thread ...")
        self._dispatcher.join()

        logger.info(f"Joining {len(self._outputs)} output threads ...")
        for output_thread in self._outputs.values():
            output_thread.join()
