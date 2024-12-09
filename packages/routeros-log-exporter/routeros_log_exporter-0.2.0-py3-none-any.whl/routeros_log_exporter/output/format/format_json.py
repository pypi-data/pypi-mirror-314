# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
This format plugin renders the log message as json string. Every message is one line.

```yaml
outputs:
  log_file:
    type: file
    # Format of the log messages
    format: json
```
"""

import json
from typing import Any, Dict

from . import Format


class JSONFormat(Format):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.one_line = True

    def process(self, data):
        result = json.dumps(data)
        if self.one_line:
            result = result + "\n"
        return result


Format.register("json", JSONFormat)
