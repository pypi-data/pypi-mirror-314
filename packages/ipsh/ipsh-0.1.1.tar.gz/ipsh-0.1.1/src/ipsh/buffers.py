# -*- coding: utf-8 -*-

"""
buffers module, providing both History and LineBuffer classes
"""

from typing import Iterator

from . import const


class HistoryError(Exception):
    """Error from a history instance"""

    def __init__(self, message: str = "unspecified") -> None:
        """Store the message"""
        self.message = message

    def __str__(self) -> str:
        """String value (the message)"""
        return self.message


def echo(*data: str):
    """Print data to the screen without adding a line feed"""
    print(const.EMPTY.join(data), end=const.EMPTY, flush=True)


class History:
    """History class"""

    def __init__(self) -> None:
        """Initialize the internal buffer and current position"""
        self.__entries: list[str] = ["(empty)"]
        self.__position = len(self)

    def __len__(self):
        """Number of entries"""
        return len(self.__entries)

    def __getitem__(self, pos: int):
        """Return entry at pos"""
        if pos < 1:
            raise HistoryError("Not available")
        #
        if pos == len(self):
            return const.EMPTY
        #
        try:
            found_entry = self.__entries[pos]
        except IndexError as error:
            raise HistoryError("Not available") from error
        #
        return found_entry

    @property
    def position(self) -> int:
        """Return the current position"""
        return self.__position

    def add(self, line: str):
        """add line to buffer"""
        self.__entries.append(line)
        self.__position = len(self)

    def get_last(self):
        """get last line from buffer"""
        return self[-1]

    def get_relative(self, delta: int):
        """Get line from relative buffer index.
        Might raise a HistoryError indirectly
        """
        new_position = self.position + delta
        found_entry = self[new_position]  # raises the HistoryError if appropriate
        # If everything went fine and an entry was found,
        # adjust the position and return the found entry
        self.__position = new_position
        return found_entry

    def iter_range(self, start=1, end=-1) -> Iterator[tuple[int, str]]:
        """Return an iterator over (index, entry) tuples
        in the specified range
        """
        if end < 0:
            end = len(self) + end
        #
        if start < 0:
            start = len(self) + start
        #
        for idx in range(start, end + 1):
            try:
                yield idx, self[idx]
            except HistoryError:
                ...
            #
        #


class LineBuffer:
    """Line buffer with prompt and relative cursor position"""

    def __init__(
        self, prompt: str, initial_value: str = const.EMPTY, alert: bool = True
    ):
        """Initialize the buffer"""
        self._prompt = prompt
        self._alert = alert
        self._old_buf_len = 0
        self._buffer: list[str] = list(initial_value)
        self._pos = len(self)
        self.redraw()

    @property
    def value(self) -> str:
        """Return the string value"""
        return const.EMPTY.join(self._buffer)

    def __len__(self) -> int:
        """Return the length of the buffer"""
        return len(self._buffer)

    def replace(self, new_value: str):
        """replace the buffer contents"""
        self._buffer.clear()
        self._buffer.extend(new_value)
        self._pos = len(self)
        self.redraw()

    def redraw(self):
        """Redraw the line"""
        if self._old_buf_len > len(self):
            echo(const.CR, self._prompt, const.BLANK * self._old_buf_len)
        #
        echo(const.CR, self._prompt, const.EMPTY.join(self._buffer))
        rpos = len(self._buffer) - self._pos
        if rpos:
            echo(const.BS * rpos)
        #
        self._old_buf_len = len(self)

    def insert(self, character: str) -> None:
        """Insert _character at the cursor position"""
        if len(character) > 1:
            raise ValueError("Can only insert single characters")
        #
        if self._pos == len(self):
            self._pos += 1
            self._buffer.append(character)
            self._old_buf_len += 1
            echo(character)
            return
        #
        self._buffer.insert(self._pos, character)
        self._pos += 1
        self.redraw()

    def move_left(self):
        """Move cursor left without changing the buffer,
        ring the bell on the left edge
        """
        if self._pos > 0:
            self._pos -= 1
            echo(const.BS)
        elif self._alert:
            echo(const.BEL)
        #

    def move_right(self):
        """Move cursor right without changing the buffer,
        ring the bell on the right edge
        """
        if self._pos < len(self):
            echo(self._buffer[self._pos])
            self._pos += 1
        elif self._alert:
            echo(const.BEL)
        #

    def delete_to_left(self):
        """Delete the character left to the cursor,
        also moving the cursor left,
        ring the bell on the left edge
        """
        if self._pos > 0:
            self._pos -= 1
            del self._buffer[self._pos]
            self.redraw()
        elif self._alert:
            echo(const.BEL)
        #
