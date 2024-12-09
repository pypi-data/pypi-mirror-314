# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later

from librouteros.api import Api
from librouteros.exceptions import TrapError, MultiTrapError
from librouteros.types import (
    ResponseIter
)


class RouterOSApi(Api):
    def readResponse(self) -> ResponseIter:
        """
        Yield each sentence until !done is received.

        :throws TrapError: If one !trap is received.
        :throws MultiTrapError: If > 1 !trap is received.
        """
        traps = []
        reply_word = None
        while reply_word != "!done":
            reply_word, words = self.readSentence()
            if reply_word == "!trap":
                traps.append(TrapError(**words))
            elif reply_word in ("!re", "!done") and words:
                yield words

        if len(traps) > 1:
            raise MultiTrapError(*traps)
        if len(traps) == 1:
            raise traps[0]
