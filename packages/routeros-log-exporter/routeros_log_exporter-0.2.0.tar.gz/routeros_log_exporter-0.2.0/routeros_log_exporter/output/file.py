# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
This plugin can writes the log messages to a file.

```yaml
outputs:
  log_file:
    type: file
    # Format of the log messages
    format: json
    # The config of this output plugin
    file_config:
      # The logging directory
      dir: "./logs"
      # The logging filename
      filename: "{{hostname}}-{{timestamp:%Y-%m-%d}}.json"
```

## Filename patterns

hostname

: The hostname value from the config file

timestamp

: The timestamp when the log message has been received.
  It has an additional parameter to specify the format.
  It uses the strftime syntax.

## Signals

SIGHUP

: This plugin handles the SIGHUP signal. If the signal is received it closes all file
  handles and reopens them if needed. This is useful if you want to use it with a
  tool like logrotate.
"""


from datetime import datetime
import logging
import os.path
from pprint import pformat
import queue
import re
import signal
from typing import Any, Dict, List, TextIO


from . import Output
from .format import Format
from ..exception import ConfigError
from ..fetcher import LogMessage

logger = logging.getLogger("output.file")


class FileOutput(Output):
    name = "file"

    def __init__(self, filename_template: str, output_format: Format):
        super().__init__()

        self._filename_template: str = filename_template
        self._filename_patterns: Dict[str, Dict[str, Any]] = {}
        for m in re.finditer(r"{{(?P<type>[^}:]+)(:(?P<params>[^}]+))?}}", self._filename_template):
            pattern_type = m.group("type")
            pattern = m.group(0)
            pattern_config = {
                "type": pattern_type,
            }
            if pattern_type == "timestamp":
                pattern_config["format"] = m.group("params")
            elif pattern_type in ("hostname",):
                # Patterns without params
                pass
            else:
                logger.warning(
                    f"Unknown pattern '{pattern_type}' "
                    f"found in filename template: {self._filename_template}"
                )
                continue

            self._filename_patterns[pattern] = pattern_config
            logger.debug(
                f"Found pattern '{pattern}' in filename template '{filename_template}'"
                f" with config {pformat(pattern_config)}"
            )

        self._fp_cache: Dict[str, List] = {}
        self._clean_fp_lastrun = datetime.now()
        self._force_clean_fp = False

        self.output_format = output_format

        self._should_terminate = False

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> Output:
        file_config = config.get("file_config")
        if not isinstance(file_config, dict):
            raise ConfigError("file_config not a dict")

        raw_filename = file_config.get("filename")
        if not isinstance(raw_filename, str):
            raise ConfigError("Filename not set or not a string")
        filename = raw_filename

        raw_log_dir = file_config.get("dir", "")
        if not isinstance(raw_log_dir, str):
            raise ConfigError("log_dir not set or not a string")
        log_dir = raw_log_dir
        filename_template = os.path.join(log_dir, filename)

        format_name = config.get("format")
        if not isinstance(format_name, str):
            raise ConfigError("format must be set and a string")

        format_cls = Format.registered_formats.get(format_name)
        if format_cls is None:
            raise ConfigError(f"Unable to find format with name '{format_name}'")

        return cls(
            filename_template=filename_template,
            output_format=format_cls(config=config.get("format_config", {}))
        )

    def _get_fp(self, filename) -> TextIO:
        cached_fp = self._fp_cache.get(filename)
        if cached_fp is None:
            logger.info(f"Open file {filename} ...")
            cached_fp = [open(filename, "a"), datetime.now()]
        else:
            cached_fp[1] = datetime.now()
        self._fp_cache[filename] = cached_fp
        return cached_fp[0]

    def _clean_fp(self):
        if self._force_clean_fp:
            self._force_clean_fp = False
            logger.info("File cache forced cleaning started")
            for filename in list(self._fp_cache.keys()):
                cached_fp = self._fp_cache[filename]
                logger.info(f"Closing file {filename} ...")
                cached_fp[0].close()
                del self._fp_cache[filename]
            logger.info("File cache forced cleaning finished")
            return

        now = datetime.now()
        lastrun_ago = now - self._clean_fp_lastrun
        if lastrun_ago.total_seconds() < 600:
            return
        logger.info("File cache cleaning started")
        for filename in list(self._fp_cache.keys()):
            cached_fp = self._fp_cache[filename]
            idle_time = now - cached_fp[1]
            if idle_time.total_seconds() > 600:
                logger.info(f"Closing unused file {filename} ...")
                cached_fp[0].close()
                del self._fp_cache[filename]
        self._clean_fp_lastrun = now
        logger.info("File cache cleaning finished")

    def handle_signal(self, signal_number):
        logger.info(f"Handling signal {signal_number} ({signal.Signals(signal_number).name})")
        if signal_number == signal.SIGHUP:
            self._force_clean_fp = True

    def write(self, message: LogMessage):
        filename = self._filename_template
        for pattern, pattern_config in self._filename_patterns.items():
            if pattern_config["type"] == "hostname":
                data = message.fetcher.hostname
            elif pattern_config["type"] == "timestamp":
                data = message.timestamp.strftime(pattern_config["format"])
            else:
                continue

            filename = filename.replace(pattern, data)

        fp = self._get_fp(filename)
        fp.write(self.output_format.process(message.as_dict))

    def run(self):
        while not self._should_terminate:
            try:
                message = self._queue.get(timeout=2)
            except queue.Empty:
                continue
            self._queue.task_done()
            self.write(message)
            self._clean_fp()

    def stop(self):
        self._should_terminate = True


Output.register("file", FileOutput)
