# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
The fetcher connects to a RouterOS device and uses the ```/log/print``` command to
collect the log messages from the stream. The messages are not processes by the
fetcher. One should use one or more output plugins to dump the logs.

```yaml
devices:
  - hostname: 192.168.0.1
    username: logger
    password: secure_password
    outputs:
      # The output has to be defined
      - log_file

  - hostname: 1.2.3.4
    username: admin
    password: secure_password
    ssl: yes
    outputs:
      # The output has to be defined
      - log_file
```

# Config

hostname (Default: localhost)
: The hostname or the IP address of the device to connect to

username (Default: admin)
: The username of a user that can access the log stream. We recommend not use the admin
  user and create a dedicated user to fetch the logs. We also recommend to limit the
  access to specified source IPs.

password
: A secure password

port (Default: not set)
: If not set the port is 8728 if ```ssl: false``` and 8729 if ```ssl: true```

ssl (Default: true)
: Use SSL/TLS to connect to the device. It is highly recommended to not disable this feature.

ssl_force_no_certificate (Default: false)
: Use SSL/TLS encryption but without certificate.

ssl_verify (Default: true)
: Verify the provided certificate
: Warning: This will not work if ```ssl_force_no_certificate: true```

ssl_verify_hostname (Default: true)
: Verify the hostname provided.
: Warning: This will not work if ```ssl_force_no_certificate: true```

ssl_cafile (Default: not set use CA from system)
: Set a ca file to use

ssl_capath  (Default: not set use CA from system)
: Set a path to ca files to use

"""

import logging
from datetime import datetime, timezone
from threading import Thread
import ssl
from typing import Any, Dict, List, Optional, Set
from queue import Queue

from librouteros import connect

from .exception import ConfigError
from .output import Output
from .routeros import RouterOSApi

logger = logging.getLogger("fetcher")


class LogFetcher(Thread):
    DEFAULT_CONFIG: Dict[str, Any] = {
        "hostname": "localhost",
        "username": "admin",
        "password": "",
    }

    def __init__(
            self,
            hostname: str,
            username: str,
            password: str,
            message_queue: Queue,
            outputs: Set[Output],
            port: Optional[int] = None,
            use_ssl: bool = True,
            ssl_cafile: Optional[str] = None,
            ssl_capath: Optional[str] = None,
            ssl_force_no_certificate: bool = False,
            ssl_verify: bool = True,
            ssl_verify_hostname: bool = True
    ):
        super().__init__()
        self._api: Optional[RouterOSApi] = None
        self._message_queue = message_queue

        self.hostname = hostname
        self.username = username
        self.password = password

        self.port: int = 8728
        if port is None:
            if use_ssl:
                self.port = 8729
        else:
            self.port = port

        self.outputs = outputs

        self.ssl_cafile = ssl_cafile
        self.ssl_capath = ssl_capath
        self.ssl_force_no_certificate = ssl_force_no_certificate
        self.ssl_verify = ssl_verify
        self.ssl_verify_hostname = ssl_verify_hostname

        self._should_terminate = False

    @classmethod
    def from_config(
        cls, config: Dict[str, Any], message_queue: Queue, available_outputs: Dict[str, Output]
    ) -> "LogFetcher":
        _config = dict(cls.DEFAULT_CONFIG.items())
        _config.update(config)

        raw_hostname = config.get("hostname")
        if not isinstance(raw_hostname, str):
            raise ConfigError("Hostname not set or not a string")
        hostname: str = raw_hostname

        raw_port = config.get("port")
        if raw_port is not None and not isinstance(raw_port, int):
            raise ConfigError("Port must be None or type int")
        port = raw_port

        raw_username = config.get("username")
        if not isinstance(raw_username, str):
            raise ConfigError("Username not set or not a string")
        username: str = raw_username

        raw_password = config.get("password")
        if not isinstance(raw_password, str):
            raise ConfigError("Password not set or not a string")
        password: str = raw_password

        outputs: Set[Output] = set()
        raw_outputs = config.get("outputs")
        if not isinstance(raw_outputs, (list, tuple)):
            raise ConfigError("No outputs specified")

        for output_name in raw_outputs:
            output = available_outputs.get(output_name)
            if output is None:
                raise ConfigError(f"Unable to found output with name '{output_name}'")
            outputs.add(output)

        use_ssl = bool(config.get("ssl"))
        ssl_cafile: Optional[str] = config.get("ssl_cafile")
        ssl_capath: Optional[str] = config.get("ssl_capath")
        ssl_force_no_certificate = bool(config.get("ssl_force_no_certificate"))
        ssl_verify = bool(config.get("ssl_verify"))
        ssl_verify_hostname = bool(config.get("ssl_verify_hostname"))

        return cls(
            hostname=hostname,
            username=username,
            password=password,
            message_queue=message_queue,
            outputs=outputs,
            port=port,
            use_ssl=use_ssl,
            ssl_cafile=ssl_cafile,
            ssl_capath=ssl_capath,
            ssl_force_no_certificate=ssl_force_no_certificate,
            ssl_verify=ssl_verify,
            ssl_verify_hostname=ssl_verify_hostname,
        )

    def _process_messages(self):
        log_stream = self.api(
            "/log/print",
            **{
                "follow-only": "",
            }
        )
        for message in log_stream:
            if self._should_terminate:
                return
            if message.get(".dead") is True:
                continue
            self._message_queue.put(LogMessage(fetcher=self, message=message))

    @property
    def api(self) -> RouterOSApi:
        if self._api is not None:
            return self._api

        ssl_ctx = ssl.create_default_context(
            cafile=self.ssl_cafile,
            capath=self.ssl_capath
        )
        if self.ssl_force_no_certificate:
            ssl_ctx.check_hostname = False
            ssl_ctx.set_ciphers('ADH:@SECLEVEL=0')
        elif not self.ssl_verify:
            # We have to disable hostname check if we disable certificate verification
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
        elif not self.ssl_verify_hostname:
            ssl_ctx.check_hostname = False

        logger.info(f"Connection to {self.hostname}:{self.port}")
        self._api = connect(
            host=self.hostname,
            username=self.username,
            password=self.password,
            ssl_wrapper=ssl_ctx.wrap_socket,
            port=self.port,
            subclass=RouterOSApi,
        )
        logger.info("Connected")
        return self._api

    def handle_signal(self, signal_number):
        pass

    def run(self):
        while not self._should_terminate:
            try:
                self._process_messages()
            except OSError:
                continue

    def join(self, timeout=None):
        logger.info("Termination fetcher")
        logger.info(f"Closing connection to {self.hostname}:{self.port}")
        self.api.close()

    def stop(self):
        self._should_terminate = True


class LogMessage:
    def __init__(self, fetcher: LogFetcher, message: Dict[str, Any]):
        self._fetcher: LogFetcher = fetcher
        self._timestamp = datetime.now(timezone.utc)
        self._raw_message = message

        self.timestamp = datetime.now(timezone.utc)
        self.id = None
        self.time = None
        self.topics: List[str] = []
        self.message = message

        self.processed = False

    @property
    def fetcher(self):
        return self._fetcher

    def process(self):
        if self.processed:
            return
        message_id = self._raw_message[".id"]
        str_topics = self._raw_message.get("topics", "")
        self.id = message_id.strip("*")
        self.time = self._raw_message.get("time")
        self.topics = [t.strip() for t in str_topics.split(",")]
        self.message = self._raw_message.get("message")
        self.processed = True

    def dispatch(self):
        self.process()
        for log_output in self._fetcher.outputs:
            log_output.queue.put(self)

    @property
    def as_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.id,
            "message_time": self.time,
            "message_topics": self.topics,
            "message": self.message,
        }
