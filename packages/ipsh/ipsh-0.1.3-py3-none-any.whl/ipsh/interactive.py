# -*- coding: utf-8 -*-
"""
shell module
"""

import dataclasses
import logging
import os
import sys

from typing import Callable

from . import const
from . import interpreters

from .buffers import HistoryError, LineBuffer


if sys.platform.startswith("linux") or sys.platform == "darwin":
    from .getch_unix import getch_unix as getch
elif sys.platform in ("win32", "cygwin"):
    from .getch_windows import getch_windows as getch
else:
    raise NotImplementedError(f'Platform "{sys.platform}" not implemented')
#


CTRL_A = chr(1)
CTRL_C = chr(3)
CTRL_D = chr(4)
CTRL_E = chr(5)
CTRL_K = chr(11)
CTRL_R = chr(18)

ESC = chr(0x1B)
OPENING_BRACKET = chr(0x5B)
DIGIT_3 = chr(0x33)

SEQUENCE_INITS = ""

CURSOR_LEFT: tuple[str, ...] = ("\x1b[D",)
CURSOR_RIGHT: tuple[str, ...] = ("\x1b[C",)
CURSOR_UP: tuple[str, ...] = ("\x1b[A",)
CURSOR_DOWN: tuple[str, ...] = ("\x1b[B",)
CURSOR_HOME: tuple[str, ...] = ("\x1b[H",)
CURSOR_END: tuple[str, ...] = ("\x1b[F",)
KBD_DEL: tuple[str, ...] = ("\x1b[3~",)
ALT_DOT: tuple[str, ...] = ("\x1b\x2e",)
ALT_POUND: tuple[str, ...] = ("\x1b\x23",)

if os.name == "nt":
    SEQUENCE_INITS = "\0\xe0"
    CURSOR_UP = ("\0\x48", "\xe0\x48")
    CURSOR_LEFT = ("\0\x4b", "\xe0\x4b")
    CURSOR_RIGHT = ("\0\x4d", "\xe0\x4d")
    CURSOR_DOWN = ("\0\x50", "\xe0\x50")
    CURSOR_HOME = ("\0\x47", "\xe0\x47")
    CURSOR_END = ("\0\x4f", "\xe0\x4f")
    KBD_DEL = ("\0\x53", "\xe0\x53")


def getkey(
    getch_fn: Callable[[], str] | None = None,
    encoding: str | None = None,
    raw: bool = True,
) -> str:
    """Get the sequence for a single keypress,
    adapted from
    <https://gitlab.com/MatteoCampinoti94/PythonRead/-/blob/master
     /readkeys/readkeys.py?ref_type=heads>
    """
    if getch_fn is None:
        # read first character from stdin
        c = getch(nonblock=False, encoding=encoding, raw=raw)
        # keep reading from stdin with nonblock flag until it returns empty
        #  meaning stdin has no more characters stored
        while (ct := getch(nonblock=True, encoding=encoding, raw=raw)) != const.EMPTY:
            c += ct
        #
        if not raw:
            c = c[0:-1]
        #
        return c
    #
    # if an external function is given then assume nonblock flag is not set
    #  keep reading and check for escape sequences
    if (c1 := getch_fn()) != ESC:
        return c1
    #
    if (c2 := getch_fn()) != OPENING_BRACKET:
        return c1 + c2
    #
    if (c3 := getch_fn()) != DIGIT_3:
        return c1 + c2 + c3
    #
    c4 = getch_fn()
    return c1 + c2 + c3 + c4


@dataclasses.dataclass
class Response:
    """Response from a Shell.dispatch method"""

    stop: bool = False
    line_finished: bool = False


class PseudoShell:
    """Interactive pseudo shell"""

    def __init__(
        self,
        prompt: str = "→ ",
        interpreter=interpreters.BaseInterpreter(),
        do_alert: bool = True,
    ) -> None:
        """Initialize"""
        self.prompt = prompt
        self._interpreter = interpreter
        self._do_alert = do_alert

    def acoustic_alert(self):
        """Ring the bell if configured"""
        if self._do_alert:
            sys.stdout.write(const.BEL)
            sys.stdout.flush()
        #

    # pylint: disable=too-many-return-statements,too-many-branches
    def dispatch(self, line_buffer: LineBuffer, key: str) -> Response:
        """Dispatch according to the key"""
        if key in SEQUENCE_INITS:
            key = f"{key}{getkey()}"
        #
        if key in CURSOR_UP:
            try:
                history_line = self._interpreter.history.get_relative(-1)
            except HistoryError:
                self.acoustic_alert()
            else:
                line_buffer.replace(history_line)
            #
            return Response()
        #
        if key in CURSOR_DOWN:
            try:
                history_line = self._interpreter.history.get_relative(1)
            except HistoryError:
                self.acoustic_alert()
            else:
                line_buffer.replace(history_line)
            #
            return Response()
        #
        if key in CURSOR_RIGHT:
            line_buffer.move_right()
            return Response()
        #
        if key in CURSOR_LEFT:
            line_buffer.move_left()
            return Response()
        #
        if key in (const.BS, const.DEL):
            line_buffer.delete_to_left()
            return Response()
        if key == const.TAB:
            try:
                suggestion = self._interpreter.suggest(line_buffer.value)
            except interpreters.NoSuggestionFound:
                self.acoustic_alert()
            else:
                line_buffer.replace(suggestion)
            #
            return Response()
        if key == CTRL_D and not line_buffer:
            print("^D")
            logging.debug("exit")
            return Response(stop=True)
        if key == CTRL_C:
            print("^C")
            logging.debug("Deleted line")
            line_buffer.replace(const.EMPTY)
            return Response()
        if key == const.CR:
            return Response(
                line_finished=True,
            )
        #
        if key.isprintable():
            line_buffer.insert(key)
        #
        return Response()

    def run(self):
        """Read lines, allow editing the buffer.
        Stop when Ctrl-D or a stop word was entered
        """
        logging.info("Exit with CTRL-D or %r", self._interpreter.stopcommand)
        line_buffer = LineBuffer(self.prompt)
        key = getkey()
        while True:
            response = self.dispatch(line_buffer, key)
            if response.stop:
                print()
                break
            #
            if response.line_finished:
                read_line = line_buffer.value
                if read_line.startswith("!"):
                    # replace line buffer with the history entry
                    # having the number following the exclamation mark
                    try:
                        history_pos = int(read_line[1:])
                        line_buffer.replace(self._interpreter.history[history_pos])
                    except (ValueError, HistoryError) as error:
                        print()
                        logging.error(str(error))
                        line_buffer.replace(const.EMPTY)
                    #
                else:
                    print()
                    if read_line:
                        try:
                            self._interpreter.execute(read_line)
                        except interpreters.InterpreterExit:
                            break
                        #
                    #
                    line_buffer.replace(const.EMPTY)
                #
            #
            key = getkey()
        #
