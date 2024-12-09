# SPDX-FileCopyrightText: PhiBo DinoTools (2021)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from routeros_log_exporter.output.format.format_json import JSONFormat


class TestBase:
    def test_json_format(self):
        f = JSONFormat(config={})

        data = {"test_key": "test_value"}
        assert f.process(data) == json.dumps(data) + "\n"
