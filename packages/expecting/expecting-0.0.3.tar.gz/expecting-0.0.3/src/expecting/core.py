from abc import ABC
from typing import Any


class Expecting(ABC):

    def __eq__(self, other: Any) -> bool:
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


__all__ = [
    'Expecting',
]
