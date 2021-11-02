from typing import Pattern
from .constants import EmojiType
import re

import nextcord


class Position:
    """
    Class for repositioning reaction buttons in a menu.

    Attributes
    ----------
    bucket : int
        The bucket number for the reaction button.
        The default bucket is 1. Bucket 0 comes at the beginning, bucket 2 at the end.
    number : int
        The number of the reaction button in the bucket.
        A lower number means the button will be closer to the beginning
    """

    __slots__ = ("number", "bucket")

    def __init__(self, number: int, *, bucket: int = 1):
        self.bucket = bucket
        self.number = number

    def __lt__(self, other):
        if not isinstance(other, Position) or not isinstance(self, Position):
            return NotImplemented

        return (self.bucket, self.number) < (other.bucket, other.number)

    def __eq__(self, other):
        return (
            isinstance(other, Position)
            and other.bucket == self.bucket
            and other.number == self.number
        )

    def __le__(self, other):
        r = Position.__lt__(other, self)
        if r is NotImplemented:
            return NotImplemented
        return not r

    def __gt__(self, other):
        return Position.__lt__(other, self)

    def __ge__(self, other):
        r = Position.__lt__(self, other)
        if r is NotImplemented:
            return NotImplemented
        return not r

    def __repr__(self):
        return "<{0.__class__.__name__}: {0.number}>".format(self)


class First(Position):
    """
    Class for repositioning reaction buttons at the beginning of a menu.

    This is a shortcut for ``Position(number=number, bucket=0)``.

    Attributes
    ----------
    number : int
        The number of the reaction button within bucket 0.
        A lower number means the button will be closer to the beginning
    """

    __slots__ = ()

    def __init__(self, number=0):
        super().__init__(number, bucket=0)


class Last(Position):
    """
    Class for repositioning reaction buttons at the end of a menu.

    This is a shortcut for ``Position(number=number, bucket=2)``.

    Attributes
    ----------
    number : int
        The number of the reaction button within bucket 2.
        A lower number means the button will be closer to the beginning
    """

    __slots__ = ()

    def __init__(self, number=0):
        super().__init__(number, bucket=2)


_custom_emoji = re.compile(
    r"<?(?P<animated>a)?:?(?P<name>[A-Za-z0-9\_]+):(?P<id>[0-9]{13,20})>?"
)


def _cast_emoji(obj: EmojiType, *, _custom_emoji: Pattern[str] = _custom_emoji):
    if isinstance(obj, nextcord.PartialEmoji):
        return obj

    obj = str(obj)
    match = _custom_emoji.match(obj)
    if match is not None:
        groups = match.groupdict()
        animated = bool(groups["animated"])
        emoji_id = int(groups["id"])
        name = groups["name"]
        return nextcord.PartialEmoji(name=name, animated=animated, id=emoji_id)
    return nextcord.PartialEmoji(name=obj, id=None, animated=False)
