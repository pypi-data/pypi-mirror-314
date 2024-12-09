# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
This format plugin renders the plan log message as string. Every message is one line.

```yaml
outputs:
  log_file:
    type: file
    # Format of the log messages
    format: text
```
"""

from . import Format


class TextFormat(Format):
    def process(self, data):
        return f"{data.get('message_time')} {','.join(data.get('message_topics', []))} {data.get('message')}\n"


Format.register("text", TextFormat)
