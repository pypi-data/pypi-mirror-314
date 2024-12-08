"""
**Tense Versioning** \n
\\@since 0.3.27a2 \\
© 2024-Present Aveyzan // License: MIT
```
module tense._versioning
```
TensePy versioning components. Under testing
"""
# scroll down to version variables
from ._primal_types import Optional, Union, TypeIs, TypeVar, Literal

version_type = ("alpha", "beta", "candidate", "final")
"\\@since 0.3.27a2"

_version_type = Literal["alpha", "beta", "candidate", "final"]
"\\@since 0.3.27a2"

_version_check_type = Union[
    tuple[int],
    tuple[int, int],
    tuple[int, int, int],
    tuple[int, int, int, str],
    tuple[int, int, int, str, int]
]
"\\@since 0.3.27a2"

_T = TypeVar("_T")

# all of these declarations are under testing, since code
# does not become unreachable
class _version(tuple[int, int, int, _version_type, int]):
    "\\@since 0.3.27a2"
    __major = 0
    __minor = 0
    __micro = 0
    __level = "final"
    __serial = 0
    @property
    def major(self):
        return self.__major
    @property
    def minor(self):
        return self.__minor
    @property
    def micro(self):
        return self.__micro
    @property
    def level(self):
        return self.__level
    @property
    def serial(self):
        return self.__serial
    @property
    def full(self):
        return (self.__major, self.__minor, self.__micro, self.__level, self.__serial)
    def __local_level_checker(self, other: Optional[str] = None):
        if isinstance(other, str):
            if other == version_type[0]:
                return 0
            elif other == version_type[1]:
                return 1
            elif other == version_type[2]:
                return 2
            else:
                return 3
        else:
            if self.__level == version_type[0]:
                return 0
            elif self.__level == version_type[1]:
                return 1
            elif self.__level == version_type[2]:
                return 2
            else:
                return 3
    def __init__(self, _1: int, _2: Optional[int] = None, _3: Optional[int] = None, _4: Optional[_version_type] = None, _5: Optional[int] = None):
        # _1 = major
        # _2 = minor
        # _3 = micro
        # _4 = level
        # _5 = serial
        self.__major = _1
        self.__minor = _2 if _2 is not None else 0
        self.__micro = _3 if _3 is not None else 0
        self.__level = _4 if _4 is not None else ""
        self.__serial = _5 if _5 is not None else 0
    def __gt__(self, other: _version_check_type):
        def _checker(v, t: _T) -> TypeIs[_T]: ...
        if _checker(other, tuple[int]):
            return self.full[0] > other[0]
        elif _checker(other, tuple[int, int]):
            return self.full[0] > other[0] or self.full[1] > other[1]
        elif _checker(other, tuple[int, int, int]):
            return self.full[0] > other[0] or self.full[1] > other[1] or self.full[2] > other[2]
        elif _checker(other, tuple[int, int, int, str]):
            return self.full[0] > other[0] or self.full[1] > other[1] or self.full[2] > other[2] or self.__local_level_checker() > self.__local_level_checker(other[3])
        elif _checker(other, tuple[int, int, int, str, int]):
            return self.full[0] > other[0] or self.full[1] > other[1] or self.full[2] > other[2] or self.__local_level_checker() > self.__local_level_checker(other[3]) or self.full[4] > other[4]
        else:
            err, s = (TypeError, "Expected a tuple with 1-5 items")
            raise err(s)
    def __lt__(self, other: _version_check_type):
        def _checker(v, t: _T) -> TypeIs[_T]: ...
        if _checker(other, tuple[int]):
            return self.full[0] < other[0]
        elif _checker(other, tuple[int, int]):
            return self.full[0] < other[0] or self.full[1] < other[1]
        elif _checker(other, tuple[int, int, int]):
            return self.full[0] < other[0] or self.full[1] < other[1] or self.full[2] < other[2]
        elif _checker(other, tuple[int, int, int, str]):
            return self.full[0] < other[0] or self.full[1] < other[1] or self.full[2] < other[2] or self.__local_level_checker() < self.__local_level_checker(other[3])
        elif _checker(other, tuple[int, int, int, str, int]):
            return self.full[0] < other[0] or self.full[1] < other[1] or self.full[2] < other[2] or self.__local_level_checker() < self.__local_level_checker(other[3]) or self.full[4] < other[4]
        else:
            err, s = (TypeError, "Expected a tuple with 1-5 items")
            raise err(s)
    def __ge__(self, other: _version_check_type):
        return not self.__lt__(other)
    def __le__(self, other: _version_check_type):
        return not self.__gt__(other)
    def __eq__(self, other: _version_check_type):
        def _checker(v, t: _T) -> TypeIs[_T]: ...
        if _checker(other, tuple[int]):
            return self.full[0] == other[0]
        elif _checker(other, tuple[int, int]):
            return self.full[0] == other[0] and self.full[1] == other[1]
        elif _checker(other, tuple[int, int, int]):
            return self.full[0] == other[0] and self.full[1] == other[1] and self.full[2] == other[2]
        elif _checker(other, tuple[int, int, int, str]):
            return self.full[0] == other[0] and self.full[1] == other[1] and self.full[2] == other[2] and self.__local_level_checker() == self.__local_level_checker(other[3])
        elif _checker(other, tuple[int, int, int, str, int]):
            return self.full[0] == other[0] and self.full[1] == other[1] and self.full[2] == other[2] and self.__local_level_checker() == self.__local_level_checker(other[3]) and self.full[4] == other[4]
        else:
            err, s = (TypeError, "Expected a tuple with 1-5 items")
            raise err(s)
    def __ne__(self, other: _version_check_type):
        return not self.__eq__(other)

version_current = (0, 3, 31, version_type[3], )
"\\@since 0.3.27a2"

version = ("0.3.31", _version(version_current))
"\\@since 0.3.27a2"

