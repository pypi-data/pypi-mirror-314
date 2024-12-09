# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import signal
from typing import Optional

import click

from . import Exporter

g_exporter: Optional[Exporter] = None


def handle_global_signal(signal_number, frame):
    g_exporter.stop()
    raise SystemExit('Exiting')


def handle_signal(signal_number, frame):
    g_exporter.handle_signal(signal_number)


@click.command()
@click.option(
    "config_filename",
    "--config",
    required=True,
    type=click.Path(),
    help="The config filename."
)
@click.option(
    "verbosity",
    "-v",
    count=True,
    help="Specify the verbosity. Use multiple times to increase the log level."
)
def cli(config_filename, verbosity):
    global g_exporter
    log_handler = None
    try:
        from rich.logging import RichHandler
        log_handler = RichHandler()
    except ImportError:
        pass

    logging_levels = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.INFO,
        3: logging.DEBUG
    }
    verbosity = min(verbosity, max(logging_levels.keys()))
    FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    if not log_handler:
        log_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging_levels[verbosity],
        format=FORMAT,
        datefmt="[%X]",
        handlers=[log_handler]
    )

    signal.signal(signal.SIGTERM, handle_global_signal)
    signal.signal(signal.SIGINT, handle_global_signal)

    signal.signal(signal.SIGHUP, handle_signal)

    g_exporter = Exporter(config_filename)
    g_exporter.start()
    signal.pause()
