"""
getch fuction on Windows, adapted from:

<https://gitlab.com/MatteoCampinoti94/PythonRead
 /-/blob/master/readkeys/getch_windows.py?ref_type=heads>
"""

# pylint: disable=import-error
import msvcrt


def getch_windows(
    nonblock: bool = False, encoding: str | None = None, raw: bool = False
) -> str:
    """Get a character on Windows"""
    del raw
    if nonblock and not msvcrt.kbhit():
        return ""
    #
    if encoding:
        return msvcrt.getch().decode(encoding)
    #
    return msvcrt.getwch()
