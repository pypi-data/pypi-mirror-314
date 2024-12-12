import math
import re


def format_seconds(secs: int) -> str:
    """Format a duration given in seconds into a human-readable string.

    This function converts a duration in seconds into a formatted string
    representing hours, minutes, and seconds. The format is as follows:
    - "0s" if the duration is zero.
    - "ss" if the duration is less than a minute.
    - "mm:ss" if the duration is less than an hour.
    - "hh:mm:ss" if the duration is an hour or more.

    Args:
        secs: The duration in seconds.

    Returns:
        A string representing the formatted duration.

    """
    val = math.floor(secs)

    seconds = math.floor(val % 60)
    val -= seconds
    val /= 60  # type: ignore

    minutes = math.floor(val % 60)
    val -= minutes
    val /= 60  # type: ignore

    hours = math.floor(val)
    if hours == 0 and minutes == 0 and seconds == 0:
        return "0s"
    elif hours == 0 and minutes == 0:
        return f"{seconds}s".zfill(2)
    elif hours == 0:
        return f"{minutes}m:{seconds}s".zfill(2)
    else:
        return f"{hours}h:{minutes}m:{seconds}s".zfill(2)


def fix_filename(name: str) -> str:
    """Replace invalid characters on Linux/Windows/MacOS with underscores.

    List from https://stackoverflow.com/a/31976060/819417
    Trailing spaces & periods are ignored on Windows.
    >>> fix_filename("  COM1  ")
    '_ COM1 _'
    >>> fix_filename("COM10")
    'COM10'
    >>> fix_filename("COM1,")
    'COM1,'
    >>> fix_filename("COM1.txt")
    '_.txt'
    >>> all('_' == fix_filename(chr(i)) for i in list(range(32)))
    True
    """
    return re.sub(
        r'[/\\:|<>"?*\0-\x1f]|^(AUX|COM[1-9]|CON|LPT[1-9]|NUL|PRN)(?![^.])|^\s|[\s.]$',
        "_",
        str(name),
        flags=re.IGNORECASE,
    )
