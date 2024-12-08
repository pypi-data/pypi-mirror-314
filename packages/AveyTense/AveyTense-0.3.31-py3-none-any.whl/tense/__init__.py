"""
# Tense (`AveyTense` on PyPi)

\\@since 0.3.24 \\
© 2023-Present Aveyzan // License: MIT
```ts
module tense
```
Multipurpose library with several extensions, including for built-ins.

Documentation: https://aveyzan.glitch.me/tense/py.html

Submodules:
- `tense.types_collection` - types collection
- `tense.constants` - constants collection
- `tense.fencord` - connection with discord
- `tense.operators` (since 0.3.27a3) - extension of `operator` library
- `tense.databases` (since 0.3.27a4) - connection with SQL. *Experimental*
"""

import sys

if sys.version_info < (3, 9):
    error = (RuntimeError, "To use TensePy library, consider having Python 3.9 or newer")
    raise error

import time, warnings, types as ty, typing as tp
from collections import deque
from ._primal import *
from ._nennai_types import *
# from tkinter import BooleanVar, IntVar, StringVar # intentions to remove this import before version 0.3.36

__module__ = "tense"

# between @since and @author there is unnecessarily long line spacing
# hence this warning is being thrown; it is being disabled.
warnings.filterwarnings("ignore")

_var = tc.TypeVar
_par = tc.ParamSpec
_uni = tc.Union
_lit = tc.Literal
_opt = tc.Optional
_cal = tc.Callable
_cm = classmethod
_sm = staticmethod
_p = property

_T = _var("_T")
_T1 = _var("_T1")
_T2 = _var("_T2")
_T_ls = _var("_T_ls", bound = _uni[
    str,
    tc.MutableSequence[tc.Any]
])
"""Note: alias `ls` - list/string"""
_T_richComparable = _var("_T_richComparable", bound = tc.RichComparable)

_P = _par("_P")


_Bits = _lit[3, 4, 8, 24]
_ProbabilityType = tc.ProbabilityType[_T] # expected int
_ProbabilitySeqNoDict = _uni[list, deque, set, frozenset, tuple]
_SizeableItemGetter = tc.TypeOrFinalVarType[tc.PickSequence[_T]]
_FileType = tc.FileType
_FileMode = tc.FileMode
_FileOpener = tc.FileOpener
_EnchantedBookQuantity = tc.EnchantedBookQuantity
_TicTacToeBoard = tc.TicTacToeBoard
_HaveCodeType = _uni[
    # satisfy dis.dis() first argument requirement
    str, bytes, bytearray, ty.MethodType, ty.FunctionType, tc.CodeType, type, tc.AnyCallable, None
]
_Ellipsis = tc.Ellipsis
_Statement = tc.Union[tc.Callable[[], object], str]
_Timer = tc.Callable[[], float]

def _local_architecture(executable = sys.executable, bits = "", linkage = ""):
    "\\@since 0.3.26rc2"
    
    from platform import architecture
    return architecture(executable, bits, linkage)[0]

class _ProbabilityLength(tc.Enum):
    "\\@since 0.3.26rc2. Internal class for class `tense.Tense`, for probability methods"
    PROBABILITY_COMPUTE = -1
    PROBABILITY_DEFAULT = 10000
    if _local_architecture() == "64bit":
        PROBABILITY_MAX = 2 ** 63 - 1 # 9223372036854775807
    else:
        PROBABILITY_MAX = 2 ** 31 - 1 # 2147483647
    # utopic probability max 'length' parameter value, basing on:
    if False: # 2d lists
        if _local_architecture() == "64bit":
            PROBABILITY_MAX = 2 ** 127 - 1
        else:
            PROBABILITY_MAX = 2 ** 63 - 1
    if False: # 3d lists
        if _local_architecture() == "64bit":
            PROBABILITY_MAX = 2 ** 191 - 1
        else:
            PROBABILITY_MAX = 2 ** 127 - 1
    if False: # 4d lists
        if _local_architecture() == "64bit":
            PROBABILITY_MAX = 2 ** 255 - 1
        else:
            PROBABILITY_MAX = 2 ** 191 - 1
    if False: # 5d lists
        if _local_architecture() == "64bit":
            PROBABILITY_MAX = 2 ** 319 - 1
        else:
            PROBABILITY_MAX = 2 ** 255 - 1
    if False: # 6d lists
        if _local_architecture() == "64bit":
            PROBABILITY_MAX = 2 ** 383 - 1
        else:
            PROBABILITY_MAX = 2 ** 319 - 1
    PROBABILITY_MIN = 1

class _BisectMode(tc.Enum):
    "\\@since 0.3.26rc2. Internal class for method `Tense.bisect()`"
    BISECT_LEFT = 0
    BISECT_RIGHT = 1

class _InsortMode(tc.Enum):
    "\\@since 0.3.26rc2. Internal class for method `Tense.insort()`"
    INSORT_LEFT = 0
    INSORT_RIGHT = 1
    
_ProbabilityLengthType = _uni[int, _lit[_ProbabilityLength.PROBABILITY_COMPUTE]]

class TenseOptions(tc.AbstractFinal):
    """
    \\@since 0.3.27a5
    ```ts
    in module tense
    ```
    Several settings holder class. Cannot be initialized nor subclassed.
    """
    initializationMessage = False
    """
    \\@since 0.3.27a5
    
    Toggle on/off initialization message in the terminal
    """
    
    insertionMessage = False
    """
    \\@since 0.3.27b1
    
    Toggle on/off insertion messages (these displayed by `Tense.print()`). \\
    If this option was `False`, invoked is mere `print()` method. This option \\
    has also influence on `Fencord` solutions.
    """
    if False: # to be toggled on on version 0.3.27 or later
        probabilityExtendedLength = False
        """
        \\@since 0.3.27rc1. Toggle on/off extended length via 2d list technique. Once it is toggled off, \\
        error will be thrown if going above `sys.maxsize`, `(sys.maxsize + 1) ** 2 - 1` otherwise.
        """
    
    disableProbability2LengthLimit = False
    """
    \\@since 0.3.31
    
    Switch on/off length limit, which bases on `sys.maxsize`. If that option was enabled, length passed \\
    to `Tense.probability2()` class method will no longer throw an error whether length is greater than \\
    `sys.maxsize`. This also prevents creating a temporary list to generate the result via this method. It will \\
    not work on extended variation of this method, `Tense.probability()`, unless there were exactly 2 \\
    integer values passed. Its default value is `False`
    """


class FencordOptions(tc.AbstractFinal):
    """
    \\@since 0.3.27b1
    ```ts
    in module tense
    ```
    Several settings holder class. Cannot be initialized nor subclassed.
    """
    
    initializationMessage = False
    "\\@since 0.3.27b1. Toggle on/off initialization message in the terminal"


class Tense(
    NennaiAbroads,
    # NennaiStringz, ### no inherit since 0.3.27
    NennaiRandomize,
    Time,
    Math,
    tc.Positive[str],
    tc.Negative[str],
    tc.Invertible[str],
    tc.BitwiseLeftOperable,
    tc.BitwiseRightOperable
    ):
    """
    \\@since 0.3.24 (standard since 0.3.24)
    ```ts
    in module tense
    ```
    Root of TensePy. Subclassing since 0.3.26b3
    """
    from . import types_collection as __tc
    from .constants import VERSION as version, VERSION_ID as versionId, VERSION_TUPLE as versionTuple # last 2 = since 0.3.27a2
    import uuid as __uu, re as __re, time as __ti, tkinter as __tk, inspect as __ins, bisect as __bi, ast as __ast # math as __ma
    import dis as __dis, socket as __so
    PROBABILITY_COMPUTE = _ProbabilityLength.PROBABILITY_COMPUTE
    "\\@since 0.3.26rc2"
    BISECT_LEFT = _BisectMode.BISECT_LEFT
    "\\@since 0.3.26rc2"
    BISECT_RIGHT = _BisectMode.BISECT_RIGHT
    "\\@since 0.3.26rc2"
    INSORT_LEFT = _InsortMode.INSORT_LEFT
    "\\@since 0.3.26rc2"
    INSORT_RIGHT = _InsortMode.INSORT_RIGHT
    "\\@since 0.3.26rc2"
    TIMEIT_TIMER_DEFAULT = __ti.perf_counter
    "\\@since 0.3.26rc3"
    TIMEIT_NUMBER_DEFAULT = 1000000
    "\\@since 0.3.26rc3"
    streamLikeC = False
    "\\@since 0.3.27a5. If set to `True`, output becomes `<<` and input - `>>`, vice versa otherwise"
    streamInputPrompt = ""
    "\\@since 0.3.27a5. Prompt for `input()` via `>>` and `<<` operators, depending on value of setting `streamLikeC`"
    streamInputResult = ""
    "\\@since 0.3.27b1. Result from `>>` or `<<`, depending on which one of them is for input"
    @_cm
    def __isConditionCallback(self, v: object) -> __tc.TypeIs[_cal[[__tc.Any], bool]]:
        "\\@since 0.3.26rc2"
        return self.__ins.isfunction(v)
    
    __formername__ = "Tense08"
    
    def __init__(self):
        e = super().fencordFormat()
        if TenseOptions.initializationMessage is True:
            print(f"\33[1;90m{e}\33[1;36m INITIALIZATION\33[0m Class '{__class__.__name__}' was successfully initalized. Line {self.__ins.currentframe().f_back.f_lineno}")
            
    def __str__(self):
        e = super().fencordFormat()
        if self.__formername__ != "Tense08":
            error = ValueError(f"When invoking string constructor of '{__class__.__name__}', do not rename variable '__formername__'")
            raise error
        try:
            subcl = f"'{__class__.__subclasses__()[0]}', "
            for i in abroad(1, __class__.__subclasses__()):
                subcl += f"'{__class__.__subclasses__()[i]}', "
            subcl = re.sub(r", $", "", subcl)
        except IndexError(AttributeError):
            subcl = f"'{NennaiAbroads.__name__}', '{NennaiRandomize.__name__}', '{Math.__name__}', '{Time.__name__}'"
        return f"""
            \33[1;90m{e}\33[1;38;5;51m INFORMATION\33[0m Basic '{__class__.__name__}' class information (in module 'tense')

            Created by Aveyzan for version 0.3.24 as a deputy of cancelled class '{__class__.__formername__}'. The '{__class__.__name__}' class is a subclass of various classes located inside other
            TensePy files: {subcl}. Class itself cannot be subclassed. Generally speaking, the '{__class__.__name__}' class
            is a collection of many various methods inherited from all of these classes, but also has some defined within its body itself, like methods: probability(),
            random(), pick() etc.
        """
    
    def __pos__(self):
        "Return information about this class. Since 0.3.26rc1"
        return self.__str__()
    
    def __neg__(self):
        "Return information about this class. Since 0.3.26rc1"
        return self.__str__()
    
    def __invert__(self):
        "Return information about this class. Since 0.3.26rc1"
        return self.__str__()
    
    def __lshift__(self, other: object):
        "\\@since 0.3.27a5. A C-like I/O printing"
        if self.streamLikeC is True:
            self.print(other)
        else:
            if self.isString(other):
                self.streamInputResult = input(self.streamInputPrompt)
            else:
                error = TypeError("Expected a string as a right operand")
                raise error
        return self
    
    def __rshift__(self, other: object):
        "\\@since 0.3.27a5. A C-like I/O printing"
        if self.streamLikeC is False:
            self.print(other)
        else:
            if self.isString(other):
                self.streamInputResult = input(self.streamInputPrompt)
            else:
                error = TypeError("Expected a string as a right operand")
                raise error
        return self
    
    @_cm
    def toList(self, v: __tc.Union[__tc.Iterable[_T], __tc.ListConvertible[_T], __tc.TupleConvertible[_T]], /):
        """
        \\@since 0.3.26rc3
        ```ts
        "class method" in class Tense
        ```
        Converts a value to a `list` built-in.
        """
        if isinstance(v, self.__tc.ListConvertible):
            return v.__tlist__()
        
        elif isinstance(v, self.__tc.TupleConvertible):
            return list(v.__ttuple__())
        
        elif isinstance(v, self.__tc.Iterable):
            return list(v)
        
        else:
            error = TypeError("Expected an iterable object or instance of 'ListConvertible'")
            raise error
    
    @_cm
    def toString(self, v: __tc.Object = ..., /):
        """
        \\@since 0.3.26rc3
        ```ts
        "class method" in class Tense
        ```
        Alias to `Tense.toStr()`, `str()`

        Converts a value to a `str` built-in.
        """
        return str(v)
    
    @_cm
    def toStr(self, v: __tc.Object = ..., /):
        """
        \\@since 0.3.26rc3
        ```ts
        "class method" in class Tense
        ```
        Converts a value to a `str` built-in.
        """
        return str(v)
    
    @_cm
    def isNone(self, v, /) -> __tc.TypeIs[None]:
        """
        \\@since 0.3.26b3
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is `None`
        """
        return v is None
    
    @_cm
    def isEllipsis(self, v, /) -> __tc.TypeIs[__tc.Ellipsis]:
        """
        \\@since 0.3.26
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is `...`
        """
        return v is ...
    
    @_cm
    def isBool(self, v: object, /) -> __tc.TypeIs[bool]:
        """
        \\@since 0.3.26b3
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `bool`
        """
        return v is True or v is False
    
    @_cm
    def isBoolean(self, v: object, /) -> __tc.TypeIs[bool]:
        """
        \\@since 0.3.26rc1
        ```ts
        "class method" in class Tense
        ```
        Alias to `Tense.isBool()`

        Determine whether a value is of type `bool`
        """
        return v is True or v is False
    
    @_cm
    def isInt(self, v: object, /) -> __tc.TypeIs[int]:
        """
        \\@since 0.3.26b3
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `int`
        """
        return isinstance(v, int)
    
    @_cm
    def isInteger(self, v: object, /) -> __tc.TypeIs[int]:
        """
        \\@since 0.3.26rc1
        ```ts
        "class method" in class Tense
        ```
        Alias to `Tense.isInt()`

        Determine whether a value is of type `int`
        """
        return isinstance(v, int)
    
    @_cm
    def isFloat(self, v: object, /) -> __tc.TypeIs[float]:
        """
        \\@since 0.3.26b3
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `float`
        """
        return isinstance(v, float)
    
    @_cm
    def isComplex(self, v: object, /) -> __tc.TypeIs[complex]:
        """
        \\@since 0.3.26b3
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `complex`
        """
        return isinstance(v, complex)
    
    @_cm
    def isStr(self, v: object, /) -> __tc.TypeIs[str]:
        """
        \\@since 0.3.26b3
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `str`
        """
        return isinstance(v, str)
    
    @_cm
    def isString(self, v: object, /) -> __tc.TypeIs[str]:
        """
        \\@since 0.3.26rc1
        ```ts
        "class method" in class Tense
        ```
        Alias to `Tense.isStr()`

        Determine whether a value is of type `str`
        """
        return isinstance(v, str)
    
    @_cm
    def isTuple(self, v: object, /) -> __tc.TypeIs[tuple[__tc.Any, ...]]:
        """
        \\@since 0.3.26rc1
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `tuple`
        """
        return isinstance(v, tuple)
    
    @_cm
    def isList(self, v: object, /) -> __tc.TypeIs[list[__tc.Any]]:
        """
        \\@since 0.3.26rc1
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `list`
        """
        return isinstance(v, list)
    
    @_cm
    def isDict(self, v: object, /) -> __tc.TypeIs[dict[__tc.Any, __tc.Any]]:
        """
        \\@since 0.3.31
        ```ts
        "class method" in class Tense
        ```
        Determine whether a value is of type `dict`
        """
        return isinstance(v, dict)
    
    @_cm
    def architecture(self, executable = sys.executable, bits = "", linkage = ""):
        """
        \\@since 0.3.26rc2 (0.3.27a5: added optional parameters)
        ```
        "class method" in class Tense
        ```
        Returns system's architecture
        """
        return _local_architecture(executable, bits, linkage)
    
    @_cm
    def disassemble(
        self,
        x: _HaveCodeType = None,
        /,
        file: __tc.Optional[__tc.IO[str]] = None,
        depth: __tc.Optional[int] = None,
        showCaches = False,
        adaptive = False,
        showOffsets = False
        ):
        """
        \\@since 0.3.26rc3
        ```
        "class method" in class Tense
        ```
        Detach code of a class, type, function, methods and other compiled objects. \\
        If argument `x` is `None` (by default is `None`), disassembled is last traceback. \\
        See [`dis.dis()`](https://docs.python.org/3/library/dis.html#dis.dis) \\
        Modified 0.3.31: added missing parameter `showOffsets`
        """
        self.__dis.dis(x, file = file, depth = depth, show_caches = showCaches, adaptive = adaptive, show_offsets = showOffsets)
        return self
    
    @_cm
    def timeit(
        self,
        statement: __tc.Optional[_Statement] = None,
        /,
        setup: __tc.Optional[_Statement] = None,
        timer: _Timer = TIMEIT_TIMER_DEFAULT,
        number = TIMEIT_NUMBER_DEFAULT,
        globals: __tc.Optional[dict[str, __tc.Any]] = None
        ):
        """
        \\@since 0.3.26rc3
        ```
        "class method" in class Tense
        ```
        See [`timeit.timeit()`](https://docs.python.org/3/library/timeit.html#timeit.timeit) \\
        Return time execution for specific code scrap (`statement`). Basic use::

            Tense.timeit(lambda: pow(3, 2)) # 0.06483080000180053
            Tense.timeit(lambda: math.pow(3, 2)) # 0.1697132999979658
            Tense.timeit(lambda: Tense.pow(3, 2)) # 0.26907890000074985
        """
        from timeit import timeit as _timeit
        return _timeit(
            stmt = "pass" if self.isNone(statement) else statement,
            setup = "pass" if self.isNone(setup) else setup,
            timer = timer,
            number = number,
            globals = globals
        )
    @_cm
    def socket(self, family: _uni[int, __so.AddressFamily] = -1, type: _uni[int, __so.SocketKind] = -1, proto = -1, fileno: _opt[int] = None):
        """
        \\@since 0.3.27a2
        ```
        "class method" in class Tense
        ```
        See [`socket.socket`](https://docs.python.org/3/library/socket.html#socket.socket)
        """
        from socket import socket as _socket
        return _socket(family, type, proto, fileno)
    @_cm
    def shuffle(self, v: _T_ls) -> _T_ls:
        """
        \\@since 0.3.26rc1
        ```
        "class method" in class Tense
        ```
        Shuffle a string or a list. Comparing to `random.shuffle()` in case of lists, \\
        shuffled list is returned and the one passed to the parameter isn't modified.

        String isn't modified as well, returned is shuffled one
        """
        from random import shuffle
        if isinstance(v, self.__tc.MutableSequence):
            _v = v
            shuffle(_v)
        elif self.isString(v):
            _v = [c for c in v]
            shuffle(_v)
            _v = "".join(_v)
        # elif isinstance(v, Sequence):
        #     _v = list(v)
        #     shuffle(_v)
        #     _v = tuple(_v)
        # elif isinstance(v, MutableSet):
        #     _v = list(v)
        #     shuffle(_v)
        #     _v = set(_v)
        # elif isinstance(v, Set):
        #     _v = list(v)
        #     shuffle(_v)
        #     _v = frozenset(_v)
        # elif isinstance(v, MutableMapping):
        #    _l = list(v.values())
        #    _r = 0 # random integer
        #    _f = {} # final dict
        #    _b = list(0) # blacklist
        #    while _v:
        #        _r = self.random(0, reckon(_v) - 1)
        #        for k in v:
        #            if v[k] == _l[_r]:
        #                _f[k] = _l[_r]
        #                del _l[_r]
        #                break
        else:
            if not self.isString(v):
                error = TypeError("Expected a list or a string")
                raise error
            
        return _v
    @_cm
    def reverse(self, v: _T_ls) -> _T_ls:
        """
        \\@since 0.3.26rc2
        ```
        "class method" in class Tense
        ```
        Reverse a string or a list. Comparing to `list.reverse()` in case of lists, \\
        reversed list is returned and the one passed to the parameter isn't modified.

        String isn't modified as well, returned is reversed one
        """
        if isinstance(v, self.__tc.MutableSequence):
            _v = v
            _v.reverse()
        # elif isinstance(v, Sequence):
        #     _v = list(v)
        #     _v.reverse()
        #     _v = tuple(_v)
        # elif isinstance(v, MutableSet):
        #     _v = list(v)
        #     _v.reverse()
        #     _v = set(_v)
        # elif isinstance(v, Set):
        #     _v = list(v)
        #     _v.reverse()
        #     _v = frozenset(_v)
        else:
            if not self.isString(v):
                error = TypeError("Expected a list or a string")
                raise error
            _v = [c for c in v]
            _v.reverse()
            _v = "".join(_v)
        return _v
    @_cm
    def append(self, seq: __tc.MutableSequence[_T], *items: _T):
        """
        \\@since 0.3.27a4
        ```
        "class method" in class Tense
        ```
        Same as `list.append()`, just variable amount of items can be passed. \\
        Input list remains non-modified, and returned is its modified copy.
        """
        return [e1 for e1 in seq] + [e2 for e2 in items]
    
    @_cm
    def extend(self, seq: __tc.MutableSequence[_T], *iterables: __tc.Iterable[_T]):
        """
        \\@since 0.3.27a4
        ```
        "class method" in class Tense
        ```
        Same as `list.extend()`, just variable amount of iterables can be passed. \\
        Input list remains non-modified, and returned is its modified copy.
        """
        _seq = [e for e in seq]
        for e1 in iterables:
            
            for e2 in e1:
                _seq += [e2]
                
        return _seq

    @_cm
    def clear(self, *seqs: __tc.Union[__tc.MutableSequence[_T], str]):
        """
        \\@since 0.3.27a4
        ```
        "class method" in class Tense
        ```
        Same as `list.clear()`, just variable amount of lists can be passed. \\
        Since 0.3.27b1 strings are also passable.
        """
        for seq in seqs:
            
            if self.isString(seq):
                seq = ""
                
            else:
                seq.clear()

    @_cm
    def eval(self, source: __tc.Union[str, __tc.Buffer, __ast.Module, __ast.Expression, __ast.Interactive], ast = False):
        "\\@since 0.3.26rc2."
        from ast import literal_eval
        if not ast:
            return eval(compile(source))
        else:
            if not self.isString(source) and not isinstance(source, self.__tc.Buffer):
                error = TypeError("For ast.literal_eval expected a string or buffer")
                raise error
            else:
                return literal_eval(str(source) if not self.isString(source) else source)
    @_cm
    def bisect(self, seq: __tc.SizeableItemGetter[_T], item: _T_richComparable, low: int = 0, high: _opt[int] = None, mode: _BisectMode = BISECT_RIGHT, key: _opt[_cal[[_T], _T_richComparable]] = None):
        "\\@since 0.3.26rc2. A blend of functions inside `bisect` module: `bisect_left()` and `bisect_right()`."
        if mode == self.BISECT_LEFT:
            return int(self.__bi.bisect_left(seq, item, low, high, key = key))
        
        elif mode == self.BISECT_RIGHT:
            return int(self.__bi.bisect_right(seq, item, low, high, key = key))
        
        else:
            error = TypeError("Incompatible value for 'mode' parameter. Expected one of constants: 'BISECT_LEFT' or 'BISECT_RIGHT'")
            raise error
    @_cm
    def insort(self, seq: __tc.MutableSequence[_T], item: _T, low: int = 0, high: _opt[int] = None, mode: _InsortMode = INSORT_RIGHT, key: _opt[_cal[[_T], _T_richComparable]] = None):
        "\\@since 0.3.26rc2. A blend of functions inside `bisect` module: `insort_left()` and `insort_right()`."
        _seq = seq
        if mode == self.INSORT_LEFT:
            self.__bi.insort_left(_seq, item, low, high, key = key)
            
        elif mode == self.INSORT_RIGHT:
            self.__bi.insort_right(_seq, item, low, high, key = key)
            
        else:
            error = TypeError("Incompatible value for 'mode' parameter. Expected one of constants: 'INSORT_LEFT' or 'INSORT_RIGHT'")
            raise error
        return _seq
    
    @_cm
    def print(self, *values: object, separator: _opt[str] = " ", ending: _opt[str] = "\n", file: _uni[tc.Writable[str], tc.Flushable, None] = None, flush: bool = False, invokeAs = "INSERTION"):
        """
        \\@since 0.3.25
        ```
        "class method" in class Tense
        ```
        Same as `print()`, just with `INSERTION` beginning. It can be \\
        changed with `invokeAs` parameter. Since 0.3.26a1 this method \\
        returns reference to this class. Since 0.3.27b1, if setting \\
        `TenseOptions.insertionMessage` was `False`, `invokeAs` \\
        parameter will lose its meaning.
        """
        if TenseOptions.insertionMessage is True:
            e = super().fencordFormat()
            print(f"\33[1;90m{e}\33[1;38;5;45m {invokeAs}\33[0m", *values, sep = separator, end = ending, file = file, flush = flush)
        else:
            print(*values, sep = separator, end = ending, file = file, flush = flush)
            
        return self
    
    @_cm
    def random(self, x: int, y: int, /):
        """
        \\@since 0.3.24 (standard since 0.3.25) \\
        \\@lifetime ≥ 0.3.24 \\
        \\@modified 0.3.25, 0.3.26rc2 (support for `tkinter.IntVar`), 0.3.31 (cancelled support for `tkinter.IntVar`)
        ```
        "class method" in class Tense
        ```
        Return a pseudo-random integer from range [x, y], including both points. If `x` is \\
        greater than `y`, returned is random integer from range [y, x]. If `x` and `y` are equal, \\
        returned is `x`. This interesting move perhaps doesn't return a random number, both \\
        points may not together generate floating-point numbers, since this method returns \\
        integer!
        """
        _x = x
        _y = y
        return super().randomizeInt(_x, _y)
    
    @_cm
    def uuidPrimary(self, node: _uni[int, None] = None, clockSeq: _uni[int, None] = None):
        """
        \\@since 0.3.26a1 \\
        \\@modified 0.3.31 (cancelled support for `tkinter.IntVar`)
        ```
        // created 20.07.2024
        "class method" in class Tense
        ```
        Return an UUID from host ID, sequence number and the current time.
        """
        _n = node
        _c = clockSeq
        return self.__uu.uuid1(node = _n, clock_seq = _c)
    
    @_cm
    def uuidMd5(self, namespace: __tc.UUID, name: _uni[str, bytes]):
        """
        \\@since 0.3.26a1 \\
        \\@modified 0.3.31 (cancelled support for `tkinter.StringVar`)
        ```
        // created 20.07.2024
        "class method" in class Tense
        ```
        Return an UUID from the MD5 (Message Digest) hash of a namespace UUID and a name
        """
        return self.__uu.uuid3(namespace = namespace, name = name)
    
    @_cm
    def uuidRandom(self):
        """
        \\@since 0.3.26a1
        ```
        // created 20.07.2024
        "class method" in class Tense
        ```
        Return a random UUID
        """
        return self.__uu.uuid4()
    
    @_cm
    def uuidSha1(self, namespace: __tc.UUID, name: _uni[str, bytes]):
        """
        \\@since 0.3.26a1 \\
        \\@modified 0.3.31 (cancelled support for `tkinter.StringVar`)
        ```
        "class method" in class Tense
        ```
        Return an UUID from the SHA-1 (Secure Hash Algorithm) hash of a namespace UUID and a name
        """
        return self.__uu.uuid5(namespace = namespace, name = name)
    
    @_cm
    def pick(self, seq: __tc.SequencePickType[_T], /):
        """
        \\@since 0.3.8 (standard since 0.3.24) \\
        \\@lifetime ≥ 0.3.8 \\
        \\@modified 0.3.25, 0.3.26rc2, 0.3.26rc3
        ```
        "class method" in class Tense
        ```
        Returns random item from a sequence
        """
        if not isinstance(seq, self.__tc.SequencePickNGT):
            error = TypeError("expected any iterable (except dictionaries) with integer indexes, like list or tuple")
            raise error
        if isinstance(seq, self.__tc.ListConvertible):
            _seq = tuple(seq.__tlist__())
        else:
            _seq = tuple(seq) if not self.isTuple(seq) else seq
        from random import choice
        return choice(_seq)
    
    if False: # deprecated since 0.3.25, removed 0.3.31
        def error(self, handler: type[Exception], message: _uni[str, None] = None):
            """
            \\@since 0.3.24 \\
            \\@deprecated 0.3.25
            ```
            "class method" in class Tense
            ```
            """
            _user_defined_error = handler
            _user_defined_reason = message
            if _user_defined_reason is None:
                raise _user_defined_error()
            else:
                raise _user_defined_error(_user_defined_reason)
    @_cm
    def first(self, seq: _SizeableItemGetter[_T], condition: _opt[_cal[[_T], bool]] = None):
        """
        \\@since 0.3.26rc2
        ```
        "class method" in class Tense
        ```
        Return first element in a `seq` (sequence) which satisfies `condition`. If none found, returned \\
        is default value defined via parameter `default`, which by default has value `None`. On 0.3.27a4 \\
        removed this parameter.

        Comparing to `first.first()` function, this method is implemeted and has no overloads. 
        """
        if not self.__isConditionCallback(condition) and not self.isNone(condition):
            error = TypeError("Expected 'condition' parameter as a callable or 'None'")
            raise error
        
        _seq = +seq if isinstance(seq, self.__tc.FinalVar) else seq
        _seq = list(_seq) if isinstance(_seq, (set, frozenset)) else _seq
        
        for i in abroad(_seq):
            if self.__isConditionCallback(condition) and condition(_seq[i]): return _seq[i]
            else:
                if _seq[i]: return _seq[i]
        return
    
    @_cm
    def last(self, seq: _SizeableItemGetter[_T], condition: _opt[_cal[[_T], bool]] = None, /):
        """
        \\@since 0.3.26rc2
        ```
        "class method" in class Tense
        ```
        Return last element in a `seq` (sequence) which satisfies `condition`. If none found, returned is default \\
        value defined via parameter `default`, which by default has value `None`. On 0.3.27a4 removed this parameter.
        """
        if not self.__isConditionCallback(condition) and not self.isNone(condition):
            error = TypeError("Expected 'condition' parameter as a callable or 'None'")
            raise error
        _seq = +seq if isinstance(seq, self.__tc.FinalVar) else seq
        _seq = list(_seq) if isinstance(_seq, (set, frozenset)) else _seq
        for i in self.abroadNegative(1, _seq):
            if self.__isConditionCallback(condition) and condition(_seq[i]): return _seq[i]
            else:
                if _seq[i]: return _seq[i]
        return
    
    @_cm
    def any(self, seq: _SizeableItemGetter[_T], condition: _opt[_cal[[_T], bool]] = None, /):
        """
        \\@since 0.3.26rc2
        ```
        "class method" in class Tense
        ```
        Equivalent to `any()` in-built function, but this method returns list of items, which satisfied `condition`, \\
        which has default value `None`. If none found, returned is empty list.

        Do it as `reckon(self.any(seq, condition)) > 0`
        """
        if not self.__isConditionCallback(condition) and not self.isNone(condition):
            error = TypeError("Expected 'condition' parameter as a callable or 'None'")
            raise error
        _seq = +seq if isinstance(seq, self.__tc.FinalVar) else seq
        _seq = list(_seq) if isinstance(_seq, (set, frozenset)) else _seq
        a: list[_T] = []
        for e in _seq:
            if self.__isConditionCallback(condition) and condition(e): a.append(e)
            else:
                if e: a.append(e)
        return a
    
    @_cm
    def all(self, seq: _SizeableItemGetter[_T], condition: _opt[_cal[[_T], bool]] = None, /):
        """
        \\@since 0.3.26rc2
        ```
        "class method" in class Tense
        ```
        Equivalent to `all()` in-built function, but this method returns shallow copy of sequence (as a list) with \\
        same items as in primal sequence,  if all satisfied `condition` (has default value `None`). If one of items \\
        didn't, returned is default value defined via parameter `default`, which by default has value `None`. 

        Change 0.3.27a4: removed parameter `default`.
        """
        if not self.__isConditionCallback(condition) and not self.isNone(condition):
            error = TypeError("Expected 'condition' parameter as a callable or 'None'")
            raise error
        _seq = +seq if isinstance(seq, self.__tc.FinalVar) else seq
        _seq = list(_seq) if isinstance(_seq, (set, frozenset)) else _seq
        a: list[_T] = []
        for e in _seq:
            if self.__isConditionCallback(condition) and not condition(e): return a
            else:
                if not e: return a
        a.extend(n for n in _seq)
        return a
    
    @_cm
    def probability2(self, x: _T = 1, y: _T = 0, frequency: int = 1, length: _ProbabilityLengthType = int(1e+4)):
        """
        \\@since 0.3.8 (standard since 0.3.9) \\
        \\@lifetime ≥ 0.3.8; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.26a3, 0.3.26rc1, 0.3.31 \\
        https://aveyzan.glitch.me/tense/py/method.probability.html#2
        ```
        "class method" in class Tense
        ``` \n
        ``` \n
        # syntax since 0.3.25
        def probability2(x = 1, y = 0, frequency = 1, length = 10000): ...
        # syntax for 0.3.19 - 0.3.23; on 0.3.19 renamed from probability()
        def probability2(rareValue = 1, usualValue = 0, frequency = 1, length = 10000): ...
        # syntax before 0.3.19
        def probability(value = 1, frequency = 1, length = 10000): ...
        ```
        Randomize a value using probability `frequency/length` applied on parameter `x`. \\
        Probability for parameter `y` will be equal `(length - frequency)/length`. \\
        Default values:
        - for `x`: 1
        - for `y`: 0
        - for `frequency`: 1
        - for `length`: 10000 (since 0.3.26a3 `length` can also have value `-1`)

        To be more explanatory, `x` has `1/10000` chance to be returned by default (in percents: 0.01%), \\
        meanwhile the rest chance goes to `y` (`9999/10000`, 99.99%), hence `y` will be returned more \\
        frequently than `x`. Exceptions:
        - for `frequency` equal 0 or `x` equal `y`, returned is `y`
        - for `frequency` greater than (or since 0.3.25 equal) `length` returned is `x`
        """
        
        
        
        # due to swap from IntegerEnum to Enum in _ProbabilityLength class's subclass
        # it had to be replaced
        _length = 10000 if length in (-1, self.PROBABILITY_COMPUTE) else length
        _frequency = frequency
            
        if not self.isInteger(_frequency):
            error = TypeError("expected parameter 'frequency' to be of type 'int'")
            raise error
        
        # types must match, otherwise you can meet an union-typed result, which is not useful during
        # type inspection, since you need to append appropriate 'if' statement!
        if type(x).__qualname__ != type(y).__qualname__:
            error = TypeError(f"types of parameters 'x' and 'y' do not match. Received types: for 'x' -> '{type(y).__name__}', for 'y' -> '{type(x).__name__}'")
            raise error
        
        elif _frequency < 0:
            error = ValueError("parameter 'frequency' may not have a negative integer value")
            raise error
        
        if not self.isInteger(length) and length != self.PROBABILITY_COMPUTE:
            error = TypeError("expected parameter 'length' to be of type 'int' or 'self.PROBABILITY_COMPUTE'")
            raise error
        
        elif _length == 0:
            error = ZeroDivisionError("parameter 'length' may not be equal zero, as it leads to math error")
            raise error
        
        elif _length > sys.maxsize and not TenseOptions.disableProbability2LengthLimit:
            error = ValueError(f"parameter 'length' has too high value, expected value below or equal {sys.maxsize}")
            raise error
        
        elif _length < -1:
            error = ValueError("parameter 'length' may not have a negative integer value")
            raise error
        
        tmp1, tmp2 = (x, y)
        
        # these statements are according to probability math definition
        # once 'x' and 'y' are the same, there is no reason to activate loop at all
        if tmp1 == tmp2 or _frequency == 0:
            return tmp2
        
        if _frequency >= _length:
            return tmp1
        
        if TenseOptions.disableProbability2LengthLimit:
            r = self.random(1, _length)
            return tmp1 if r >= 1 and r <= _frequency else tmp2
            
        else:
            # type of list will be deduced anyway, so there annotation may be skipped
            # 0.3.31: shortened code, reduced due to usage of list comprehension
            a = [tmp2 for _ in abroad(_length - _frequency)] + [tmp1 for _ in abroad(_length - _frequency, _length)]
            return self.pick(a)
    
    @_cm
    def probability(self, *vf: _ProbabilityType[int], length: _ProbabilityLengthType = PROBABILITY_COMPUTE):
        """
        \\@since 0.3.8 (standard since 0.3.9) \\
        \\@lifetime ≥ 0.3.8 \\
        \\@modified 0.3.19, 0.3.24, 0.3.25, 0.3.26a3, 0.3.26b3, 0.3.26rc1, 0.3.26rc2, 0.3.31 \\
        https://aveyzan.glitch.me/tense/py/method.probability.html
        ```
        "class method" in class Tense
        ``` \n
        ``` \n
        # since 0.3.25
        def probability(*vf: int | list[int] | tuple[int, int | None] | dict[int, int | None] | deque[int], length: int = PROBABILITY_COMPUTE): ...

        # for 0.3.24
        def probability(*valuesAndFrequencies: int | list[int] | tuple[int] | dict[int, int | None], length: int = PROBABILITY_ALL): ...

        # during 0.3.19 - 0.3.23; on 0.3.19 renamed
        def probability(*valuesAndFrequencies: int | list[int] | tuple[int], length: int = -1): ...

        # during 0.3.8 - 0.3.18
        def complexity(values: list[_T] | tuple[_T], frequencies: int | list[int] | tuple[int], length: int = 10000): ...
        ```
        Extended version of `Tense.probability2()` method. Instead of only 2 values user can put more than 2. \\
        Nevertheless, comparing to the same method, it accepts integers only.

        *Parameters*:

        - `vf` - this parameter waits at least for 3 values (before 0.3.26a3), for 2 values you need to use `Tense.probability2()` method \\
        instead, because inner code catches unexpected exception `ZeroDivisionError`. For version 0.3.25 this parameter accepts: 
        - integers
        - integer lists of size 1-2
        - integer tuples of size 1-2
        - integer deques of size 1-2
        - integer key-integer/`None`/`...` value dicts
        - integer sets and frozensets of size 1-2 both

        - `length` (Optional) - integer which has to be a denominator in probability fraction. Defaults to `-1`, what means this \\
        number is determined by `vf` passed values (simple integer is plus 1, dicts - plus value or 1 if it is `None` or ellipsis, \\
        sequence - 2nd item; if `None`, then plus 1). Since 0.3.26b3 put another restriction: length must be least than or equal \\
        `sys.maxsize`, which can be either equal 2\\*\\*31 - 1 (2,147,483,647) or 2\\*\\*63 - 1 (9,223,372,036,854,775,807)
        """
        # explanation:
        # a1 is final list, which will be used to return the integer
        # a2 is temporary list, which will store all single integers, without provided "frequency" value (item 2)
        a1, a2 = [[0] for _ in abroad(2)]
        a1.clear()
        a2.clear()

        # c1 sums all instances of single numbers, and with provided "frequency" - plus it
        # c2 is substraction of length and c1
        # c3 has same purpose as c1, but counts only items without "frequency" (second) item
        # c4 is last variable, which is used as last from all of these - counts the modulo of c2 and c3 (but last one minus 1 as well)
        # c5 gets value from rearmost iteration 
        c1, c2, c3, c4, c5 = [0 for _ in abroad(5)]
        
        if not self.isInteger(length) and length != self.PROBABILITY_COMPUTE:
            error = TypeError("expected integer or constant 'PROBABILITY_COMPUTE'")
            raise error
        
        _length = -1 if length == self.PROBABILITY_COMPUTE else length
        
        if _length < -1:
            error = ValueError("expected integer value from -1 or above in 'length' parameter")
            raise error
        
        elif _length == 0:
            error = ZeroDivisionError("expected integer value from -1 or above in 'length' parameter, but not equal zero")
            raise error
        
        elif _length > sys.maxsize:
            # since 0.3.26b3; cannot be greater than sys.maxsize
            error = ValueError(f"parameter 'length' has too high value, expected value below or equal {sys.maxsize}")
            raise error
        
        # START 0.3.26a3
        if reckon(vf) == 2:
            e1, e2 = (vf[0], vf[1])
            
            if self.isInteger(e1) and self.isInteger(e2):
                return self.probability2(e1, e2, length = 2)
            
            elif self.isInteger(e1) and isinstance(e2, (_ProbabilitySeqNoDict, dict)):
                
                if isinstance(e2, _ProbabilitySeqNoDict):
                    
                    if reckon(e2) == 1:
                        tmp = e2[0]
                        
                        if not self.isInteger(tmp):
                            error = TypeError("first item in an iterable is not an integer")
                            raise error
                        
                        return self.probability2(e1, tmp, length = 2)
                    
                    # those are, respectively, "value" and "frequency"
                    elif reckon(e2) == 2:
                        tmp1, tmp2 = (e2[0], e2[1])
                        
                        if not self.isInteger(tmp1):
                            error = TypeError("first item in an iterable is not an integer")
                            raise error
                        
                        if not (self.isInteger(tmp2) or self.isEllipsis(tmp2) or self.isNone(tmp2)):
                            error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                            raise error
                        
                        if Tense.isNone(tmp2) or Tense.isEllipsis(tmp2):
                            return self.probability2(e1, tmp1, length = _length)
                        
                        elif tmp2 < 1: # probability fraction cannot be negative
                            error = ValueError(f"second item in an iterable is negative or equal zero")
                            raise error
                        
                        return self.probability2(e1, tmp1, frequency = tmp2, length = _length)
                    
                    else:
                        error = IndexError(f"length of an iterable may have length 1-2 only")
                        raise error
                    
                elif isinstance(e2, dict):
                    
                    if reckon(e2) != 1:
                        error = ValueError(f"expected only one pair in a dictonary, received {reckon(e2)}")
                        raise error
                    
                    tmp1, tmp2 = (0, 0)
                    for f in e2:
                        if f in e2:
                            tmp1, tmp2 = (f, e2[f])
                            break
                    
                    if Tense.isNone(tmp2) or Tense.isEllipsis(tmp2):
                        return self.probability2(e1, tmp1, length = _length)
                    
                    elif tmp2 < 1: # probability fraction cannot be negative
                        error = ValueError(f"value in a dictionary is negative or equal zero")
                        raise error
                        
                    return self.probability2(e1, tmp1, frequency = tmp2, length = _length)
                
            elif self.isInteger(e2) and isinstance(e1, (_ProbabilitySeqNoDict, dict)):
                
                if isinstance(e1, _ProbabilitySeqNoDict):
                    
                    if reckon(e1) == 1:
                        tmp = e1[0]
                        
                        if not self.isInteger(tmp):
                            error = TypeError("first item in an iterable is not an integer")
                            raise error
                        
                        return self.probability2(tmp, e2, length = 2)
                    
                    # those are, respectively, "value" and "frequency"
                    elif reckon(e1) == 2:
                        tmp1, tmp2 = (e1[0], e1[1])
                        
                        if not isinstance(tmp1, int):
                            error = TypeError("first item in an iterable is not an integer")
                            raise error
                        
                        if not (self.isInteger(tmp2) or self.isEllipsis(tmp2) or self.isNone(tmp2)):
                            error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                            raise error
                        
                        if Tense.isNone(tmp2) or Tense.isEllipsis(tmp2):
                            return self.probability2(tmp1, e2, length = _length)
                        
                        elif tmp2 < 1: # probability fraction cannot be negative
                            error = ValueError(f"second item in an iterable is negative or equal zero")
                            raise error
                        
                        return self.probability2(tmp1, e2, frequency = _length - tmp2, length = _length)
                    
                    else:
                        error = IndexError(f"length of an iterable may have length 1-2 only")
                        raise error
                
                elif isinstance(e1, dict):
                    
                    if reckon(e1) != 1:
                        error = ValueError(f"expected only one pair in a dictonary, received {reckon(e1)}")
                        raise error
                    
                    tmp1, tmp2 = (0, 0)
                    for f in e1:
                        if f in e1:
                            tmp1, tmp2 = (f, e2[f])
                            break
                    
                    if Tense.isNone(tmp2) or Tense.isEllipsis(tmp2):
                        return self.probability2(e2, tmp1, length = _length)
                    
                    elif tmp2 < 1: # probability fraction cannot be negative
                        error = ValueError(f"value in a dictionary is negative or equal zero")
                        raise error
                        
                    return self.probability2(e2, tmp1, frequency = tmp2, length = _length)
                
            elif isinstance(e1, (_ProbabilitySeqNoDict, dict)) and isinstance(e2, (_ProbabilitySeqNoDict, dict)):
                
                if isinstance(e1, _ProbabilitySeqNoDict):
                    
                    if isinstance(e2, _ProbabilitySeqNoDict):
                        
                        if reckon(e1) == 1:
                            
                            if reckon(e2) == 1:
                                tmp1, tmp2 = (e1[0], e2[0])
                                
                                if not isinstance(tmp1, int) or not isinstance(tmp2, int):
                                    error = TypeError("first item in an iterable is not an integer")
                                    raise error
                                
                                return self.probability2(tmp1, tmp2, length = _length)
                            
                            elif reckon(e2) == 2:
                                tmp1, tmp2_1, tmp2_2 = (e1[0], e2[0], e2[1])
                                
                                if not isinstance(tmp1, int) or not isinstance(tmp2_1, int):
                                    error = TypeError("first item in an iterable is not an integer")
                                    raise error
                                
                                if not self.isEllipsis(tmp2_2) and not self.isInteger(tmp2_2) and tmp2_2 is not None:
                                    error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                    return self.probability2(tmp1, tmp2_1, length = _length)
                                
                                return self.probability2(tmp1, tmp2_1, frequency = tmp2_2, length = _length)
                            
                            else:
                                error = IndexError(f"Length of list/tuple/set/frozenset/deque may have length 1-2 only")
                                raise error
                            
                        elif reckon(e1) == 2:
                            
                            if reckon(e2) == 1:
                                tmp1_1, tmp1_2, tmp2 = (e1[0], e1[1], e2[0])
                                
                                if not isinstance(tmp1_1, int) or not isinstance(tmp2, int):
                                    error = TypeError("first item in an iterable is not an integer")
                                    raise error
                                
                                if not self.isEllipsis(tmp1_2) and not self.isInteger(tmp1_2) and self.isNone(tmp1_2):
                                    error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if tmp1_2 is None or self.isEllipsis(tmp1_2):
                                    return self.probability2(tmp1_1, tmp2, length = _length)
                                
                                return self.probability2(tmp1_1, tmp2, frequency = _length - tmp1_2, length = _length)
                            
                            elif reckon(e2) == 2:
                                tmp1_1, tmp1_2, tmp2_1, tmp2_2 = (e1[0], e1[1], e2[0], e2[1])
                                
                                if not isinstance(tmp1_1, int) or not isinstance(tmp2_1, int):
                                    error = TypeError("first item in an iterable is not an integer")
                                    raise error
                                
                                if (
                                    not self.isEllipsis(tmp1_2) and not self.isInteger(tmp1_2) and self.isNone(tmp1_2)) or (
                                    not self.isEllipsis(tmp2_2) and not self.isInteger(tmp2_2) and self.isNone(tmp2_2)
                                ):
                                    error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if tmp1_2 is None or isinstance(tmp1_2, _Ellipsis):
                                    
                                    if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                        return self.probability2(tmp1_1, tmp2_1, length = _length)
                                    
                                    else:
                                        return self.probability2(tmp1_1, tmp2_1, frequency = _length - tmp2_2, length = _length)
                                    
                                else:
                                    
                                    if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                        return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length)
                                    
                                    else:
                                        return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length if _length > tmp1_2 + tmp2_2 else tmp1_2 + tmp2_2)
                                    
                            else:
                                error = IndexError(f"Length of list/tuple/set/frozenset/deque may have length 1-2 only")
                                raise error
                            
                        else:
                            error = IndexError(f"Length of list/tuple/set/frozenset/deque may have length 1-2 only")
                            raise error
                        
                    elif isinstance(e2, dict):
                        
                        if reckon(e2) != 1:
                            error = ValueError(f"Expected only one pair in dictonary, received {reckon(e2)}")
                            raise error
                        
                        if reckon(e1) == 1:
                            tmp1, tmp2_1, tmp2_2 = (e1[0], 0, 0)
                            
                            for v in e2:
                                
                                if not isinstance(v, int):
                                    error = KeyError(f"Key in dictionary is not an integer")
                                    raise error
                                
                                if not isinstance(e2[v], int) and not self.isEllipsis(e2[v]) and e2[v] is not None:
                                    error = ValueError(f"Value in dictionary is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if e2[v] < 1:
                                    error = ValueError(f"Value in dictionary is negative integer or equal zero")
                                    raise error
                                
                                tmp2_1, tmp2_2 = (v, e2[v])
                                break
                            
                            if not isinstance(tmp1, int):
                                error = TypeError(f"First item in an iterable is not an integer")
                                raise error
                            
                            if not isinstance(tmp2_2, (int, _Ellipsis)) and tmp2_2 is not None:
                                error = TypeError("Second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                raise error
                            
                            if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                return self.probability2(tmp1, tmp2_1, length = _length)
                            
                            return self.probability2(tmp1, tmp2_1, frequency = tmp2_2, length = _length)
                        
                        elif reckon(e1) == 2:
                            tmp1_1, tmp1_2, tmp2_1, tmp2_2 = (e1[0], e1[1], 0, 0)
                            
                            for v in e2:
                                
                                if not isinstance(v, int):
                                    error = KeyError(f"Key in dictionary is not an integer")
                                    raise error
                                
                                if not isinstance(e2[v], int) and not self.isEllipsis(e2[v]) and e2[v] is not None:
                                    error = ValueError(f"Value in dictionary is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if e2[v] < 1:
                                    error = ValueError(f"Value in dictionary is negative integer or equal zero")
                                    raise error
                                
                                tmp2_1, tmp2_2 = (v, e2[v])
                                break
                            
                            if not isinstance(tmp1_1, int) or not isinstance(tmp2_1, int):
                                error = TypeError("first item in an iterable is not an integer")
                                raise error
                            
                            if (not self.isEllipsis(tmp1_2) and not self.isInteger(tmp1_2) and self.isNone(tmp1_2)) or (not isinstance(tmp2_2, (int, _Ellipsis)) and tmp2_2 is not None):
                                error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                raise error
                            
                            if tmp1_2 is None or isinstance(tmp1_2, _Ellipsis):
                                
                                if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                    return self.probability2(tmp1_1, tmp2_1, length = _length)
                                
                                else:
                                    return self.probability2(tmp1_1, tmp2_1, frequency = _length - tmp2_2, length = _length)
                                
                            else:
                                
                                if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                    return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length)
                                
                                else:
                                    return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length if _length > tmp1_2 + tmp2_2 else tmp1_2 + tmp2_2)
                                
                        else:
                            error = IndexError(f"Length of list/tuple/set/frozenset/deque may have length 1-2 only")
                            raise error
                        
                    else:
                        error = TypeError(f"Inappropriate type found. Allowed types: 'int', 'dict', 'set', 'frozenset', 'tuple', 'list', 'deque'")
                        raise error
                    
                elif isinstance(e1, dict):
                    
                    if isinstance(e2, _ProbabilitySeqNoDict):
                        
                        if reckon(e1) != 1:
                            error = ValueError(f"Expected only one pair in dictonary, received {reckon(e1)}")
                            raise error
                        
                        if reckon(e2) == 1:
                            tmp1_1, tmp1_2, tmp2 = (0, 0, e2[0])
                            
                            for v in e1:
                                if not isinstance(v, int):
                                    error = KeyError(f"Key in dictionary is not an integer")
                                    raise error
                                
                                if not isinstance(e1[v], int) and not self.isEllipsis(e1[v]) and e1[v] is not None:
                                    error = ValueError(f"Value in dictionary is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if e1[v] < 1:
                                    error = ValueError(f"Value in dictionary is negative integer or equal zero")
                                    raise error
                                
                                tmp1_1, tmp1_2 = (v, e1[v])
                                break
                            
                            if not isinstance(tmp1_1, int) or not isinstance(tmp2, int):
                                error = TypeError("first item in an iterable is not an integer")
                                raise error
                            
                            if not self.isEllipsis(tmp1_2) and not self.isInteger(tmp1_2) and self.isNone(tmp1_2):
                                error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                raise error
                            
                            if tmp1_2 is None or isinstance(tmp1_2, _Ellipsis):
                                return self.probability2(tmp1_1, tmp2, length = _length)
                            
                            return self.probability2(tmp1_1, tmp2, frequency = _length - tmp1_2, length = _length)
                        
                        elif reckon(e2) == 2:
                            tmp1_1, tmp1_2, tmp2_1, tmp2_2 = (0, 0, e2[0], e2[1])
                            
                            for v in e1:
                                
                                if not isinstance(v, int):
                                    error = KeyError(f"Key in dictionary is not an integer")
                                    raise error
                                
                                if not isinstance(e1[v], int) and not self.isEllipsis(e1[v]) and e1[v] is not None:
                                    error = ValueError(f"Value in dictionary is neither an integer, 'None', nor an ellipsis")
                                    raise error
                                
                                if e1[v] < 1:
                                    error = ValueError(f"Value in dictionary is negative integer or equal zero")
                                    raise error
                                
                                tmp1_1, tmp1_2 = (v, e1[v])
                                break
                            
                            if not isinstance(tmp1_1, int) or not isinstance(tmp2_1, int):
                                error = TypeError("first item in an iterable is not an integer")
                                raise error
                            
                            if (not self.isEllipsis(tmp1_2) and not self.isInteger(tmp1_2) and self.isNone(tmp1_2)) or (not isinstance(tmp2_2, (int, _Ellipsis)) and tmp2_2 is not None):
                                error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                                raise error
                            
                            if tmp1_2 is None or isinstance(tmp1_2, _Ellipsis):
                                
                                if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                    return self.probability2(tmp1_1, tmp2_1, length = _length)
                                
                                else:
                                    return self.probability2(tmp1_1, tmp2_1, frequency = _length - tmp2_2, length = _length)
                            else:
                                
                                if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                    return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length)
                                
                                else:
                                    return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length if _length > tmp1_2 + tmp2_2 else tmp1_2 + tmp2_2)
                        else:
                            error = IndexError(f"Length of list/tuple/set/frozenset/deque may have length 1-2 only")
                            raise error
                        
                    elif isinstance(e2, dict):
                        
                        if reckon(e2) != 1:
                            error = ValueError(f"Expected only one pair in dictonary, received {reckon(e2)}")
                            raise error
                        
                        tmp1_1, tmp1_2, tmp2_1, tmp2_2 = (0, 0, 0, 0)
                        
                        for v in e1:
                            
                            if not isinstance(v, int):
                                error = KeyError(f"key in dictionary is not an integer")
                                raise error
                            
                            if not isinstance(e1[v], int) and not self.isEllipsis(e1[v]) and e1[v] is not None:
                                error = ValueError(f"value in dictionary is neither an integer, 'None', nor an ellipsis")
                                raise error
                            
                            if e1[v] < 1:
                                error = ValueError(f"value in dictionary is negative integer or equal zero")
                                raise error
                            
                            tmp1_1, tmp1_2 = (v, e1[v])
                            break
                        
                        for v in e2:
                            
                            if not isinstance(v, int):
                                error = KeyError(f"key in dictionary is not an integer")
                                raise error
                            
                            if not isinstance(e2[v], (int, _Ellipsis)) and e2[v] is not None:
                                error = ValueError(f"value in dictionary is neither an integer, 'None', nor an ellipsis")
                                raise error
                            
                            if e2[v] < 1:
                                error = ValueError(f"value in dictionary is negative integer or equal zero")
                                raise error
                            
                            tmp2_1, tmp2_2 = (v, e2[v])
                            break
                        
                        if not isinstance(tmp1_1, int) or not isinstance(tmp2_1, int):
                            error = TypeError("first item in an iterable is not an integer")
                            raise error
                        
                        if (not self.isEllipsis(tmp1_2) and not self.isInteger(tmp1_2) and self.isNone(tmp1_2)) or (not isinstance(tmp2_2, (int, _Ellipsis)) and tmp2_2 is not None):
                            error = TypeError("second item in an iterable is neither an integer, 'None', nor an ellipsis")
                            raise error
                        
                        if tmp1_2 is None or isinstance(tmp1_2, _Ellipsis):
                            
                            if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                return self.probability2(tmp1_1, tmp2_1, length = _length)
                            
                            else:
                                return self.probability2(tmp1_1, tmp2_1, frequency = _length - tmp2_2, length = _length)
                            
                        else:
                            
                            if tmp2_2 is None or self.isEllipsis(tmp2_2):
                                return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length)
                            
                            else:
                                return self.probability2(tmp1_1, tmp2_1, frequency = tmp1_2, length = _length if _length > tmp1_2 + tmp2_2 else tmp1_2 + tmp2_2)
                            
                    else:
                        error = TypeError(f"inappropriate type found. Allowed types: 'int', 'dict', 'set', 'frozenset', 'tuple', 'list', 'deque'")
                        raise error
                    
                else:
                    error = TypeError(f"inappropriate type found. Allowed types: 'int', 'dict', 'set', 'frozenset', 'tuple', 'list', 'deque'")
                    raise error
                
            else:
                error = TypeError(f"inappropriate type found. Allowed types: 'int', 'dict', 'set', 'frozenset', 'tuple', 'list', 'deque'")
                raise error
        # END 0.3.26a3
        
        elif reckon(vf) < 2:
            # lack of integers
            error = self.__tc.MissingValueError(f"expected at least 2 items in 'vf' parameter, received {reckon(vf)}")
            raise error
        
        # reading all items provided
        for e in vf:
            
            # value is an integer (that means it cannot have "frequency"),
            # which is "value" parameter equivalent
            if isinstance(e, int):
                a1.append(e)
                a2.append(e)
                c1 += 1
                c3 += 1
                
            elif isinstance(e, _ProbabilitySeqNoDict):
                # we have only one item, and that item is "value"
                # 0.3.25 (additional statement for tuple and overall)
                if reckon(e) == 1:
                    
                    if not isinstance(e[0], int):
                        error = TypeError(f"First item in a list/tuple/set/frozenset/deque is not an integer. Ensure every first item of lists/tuples/sets/frozensets/deques is an integer. Error thrown by item: '{e[0]}'")
                        raise error
                    
                    a1.append(e[0])
                    a2.append(e[0])
                    c1 += 1
                    c3 += 1
                    
                # those are, respectively, "value" and "frequency"
                elif reckon(e) == 2:
                    
                    if not isinstance(e[0], int):
                        error = TypeError(f"First item in a list/tuple/set/frozenset/deque is not an integer. Ensure every first item of lists/tuples/sets/frozensets/deques is an integer. Error thrown by item: '{e[0]}'")
                        raise error
                    
                    if not isinstance(e[1], (int, _Ellipsis)) and e[1] is not None:
                        error = TypeError("Second item in a list/tuple/set/frozenset/deque is neither an integer, 'None', nor an ellipsis. Ensure every second item of lists/tuples/sets/frozensets/deques " + \
                        f"satisfies this requirement. Error thrown by item: '{e[1]}'")
                        raise error
                    
                    if e[1] is None or isinstance(e[1], _Ellipsis):
                        a1.append(e[0])
                        a2.append(e[0])
                        c1 += 1
                        c3 += 1
                    
                    elif e[1] < 1: # probability fraction cannot be negative
                        error = ValueError(f"Second item in a list/tuple/set/frozenset/deque is negative or equal zero. Ensure every second item of lists/tuples/sets/frozensets/deques are positive. Error thrown by item: '{e[1]}'")
                        raise error
                    
                    for _ in abroad(e[1]): a1.append(e[0])
                    c1 += int(e[1])
                    
                # if thought that the length is third item, that is wrong presupposition
                else:
                    error = IndexError(f"Length of lists/tuples/sets/frozensets/deques may have length 1-2 only, one of them has length 0 or greater than 2. Error thrown by item: '{e}'")
                    raise error
                
            # 0.3.24 (dict support)
            elif isinstance(e, dict):
                
                if reckon(e) == 0:
                   error = ValueError(f"Expected at least one pair in every dictonary, received {reckon(e)}")
                   raise error
               
                for f in e:
                    
                    if not isinstance(f, int):
                        error = KeyError(f"One of keys in dictionaries is not an integer. Ensure every key is of type 'int'. Error thrown by item: '{f}'")
                        raise error
                    
                    if not isinstance(e[f], (int, _Ellipsis)) and e[f] is not None:
                        error = ValueError(f"One of values in dictionaries is neither an integer, 'None', nor an ellipsis. Ensure every values satisfies this requirement. Error thrown by item: '{f}'")
                        raise error
                    
                    if e[f] < 1:
                        error = ValueError(f"One of values in dictionaries is negative integer or equal zero. Ensure every value is positive integer. Error thrown by item: '{e[f]}'")
                        raise error
                    
                    elif e[f] is None or isinstance(e[f], _Ellipsis):
                        a1.append(f)
                        a2.append(f)
                        c1 += 1
                        c3 += 1
                        
                    else:
                        for _ in abroad(e[f]): a1.append(f)
                        c1 += 1
                        
            # incorrect type defined
            else:
                error = TypeError(f"one of values has inappropriate type. Ensure every value are of types: 'int', 'dict', 'set', 'frozenset', 'tuple', 'list', 'deque'. Error thrown by item: '{e}', of type '{type(e).__name__}'")
                raise error
            
        # length minus times when single integers are provided is needed
        # to continue extended probability
        if _length == self.PROBABILITY_COMPUTE: c2 = c1
        else: c2 = _length - c1
        
        # hint: if not that minus one, last item will be also included
        # and we want the modulo just for the last item
        if c3 > 1: c3 -= 1
        
        # that instruction shouldn't be complicated
        # also, it is impossible to get into here, since
        # most values do not have "frequency" (aka 2nd item)
        if c2 != c1 and c2 > _length:
            tmp = [0]
            tmp.clear()
            for i in abroad(_length): tmp.append(a1[i])
            a1 = tmp
            
        # look in here: used is abroad() method, but before the valid
        # loop, all items of temporary variable will become positive
        elif c2 == c1 or (c2 != c1 and c2 < _length):
            
            for i in abroad(c2):
                
                # there we are looking for the highest number, which will
                # be divisible by number of integers passed to "vf" parameter
                if i % c3 == 0:
                    c5 = i
                    break
            # this loop is nested as we use to repeat all items from a2 list
            for i in abroad(a2):
                for _ in abroad(c5 / c3):
                    a1.append(a2[i])
                    
            # modulo will be used merely there
            c4 = c2 % c3
            
            # that one will be always done (more likely)
            # only indicated whether result in more than zero
            if c4 > 0:
                for _ in abroad(c4): a1.append(a2[reckon(a2) - 1])

        # code with following 'if False' below: as a general warning, you would use Tense.architecture()
        # to find your system's architecture, because it determines about value of sys.maxsize, which is
        # max size for all sequences not entirely sure, if creating 2d sequences to increase 'length'
        # parameter value is a good idea. scrap code below is projected
        if False:
            a3 = [[0]]
            a3.clear()
            _2d_i = 0
            while _2d_i < sys.maxsize:
                for _ in abroad(sys.maxsize):
                    a3[_2d_i].append(self.pick(a1))
                _2d_i += 1
            return self.pick(self.pick(a3))
        
        return self.pick(a1) # this will be returned
    
    @_cm
    def until(self, desiredString: _SizeableItemGetter[str], /, message: _opt[str] = None, caseInsensitive: bool = True):
        """
        \\@since 0.3.25
        ```
        "class method" in class Tense
        ```
        Console method, which will repeat the program until user won't \\
        write correct string. Case is insensitive, may be configured via \\
        optional parameter `caseInsensitive`, which by default has \\
        value `True`. Returned is reference to this class.
        """
        s = ""
        c = False
        _d = +desiredString if isinstance(desiredString, self.__tc.FinalVar) else desiredString
        _d = list(_d) if isinstance(_d, (set, frozenset)) else _d
        while c:
            s = input(message if message is not None and message != "" else "")
            c = s.lower() != _d.lower() if self.isString(_d) else s.lower() not in (_s.lower() for _s in _d)
            if not caseInsensitive: c = s != _d if self.isString(_d) else s not in _d
        return self
    
    @_cm
    def sleep(self, seconds: float, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class Tense
        ```
        Define an execution delay, which can be a floating-point number \\
        with 2 fractional digits. Returned is reference to this class.
        """
        from time import sleep as _sleep
        _sleep(seconds)
        return self
    
    @_cm
    def repeat(self, value: _T, times: _opt[int] = None, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class Tense
        ```
        Returns list with `value` repeated `times` times. \\
        `times` has default value `2`. Equals `itertools.repeat()`. \\
        Since 0.3.31 it *factually* equals `itertools.repeat()`.
        """
        from itertools import repeat as _repeat
        return _repeat(value, times) if not self.isNone(times) else _repeat(value)
    
    @_cm
    def __local_owoify_template(self, string: str, /) -> str:
        "\\@since 0.3.26b1"
        s: str = string
        s = self.__re.sub(r"\s{2}", " UrU ", s, flags = re.M)
        s = self.__re.sub(r"XD", "UrU", s, flags = re.M | re.I)
        s = self.__re.sub(r":D", "UrU", s, flags = re.M)
        s = self.__re.sub(r"lenny face", "OwO", s, flags = re.M | re.I)
        s = self.__re.sub(r":O", "OwO", s, flags = re.M | re.I)
        s = self.__re.sub(r":\)", ":3", s, flags = re.M)
        s = self.__re.sub(r"\?", " uwu?", s, flags = re.M) # ? is a metachar
        s = self.__re.sub(r"!", " owo!", s, flags = re.M)
        s = self.__re.sub(r"; ", "~ ", s, flags = re.M)
        s = self.__re.sub(r", ", "~ ", s, flags = re.M)
        s = self.__re.sub(r"you are", "chu is", s, flags = re.M)
        s = self.__re.sub(r"You are", "chu is".capitalize(), s, flags = re.M)
        s = self.__re.sub(r"You Are", "chu is".title(), s, flags = re.M)
        s = self.__re.sub(r"YOU ARE", "chu is".upper(), s, flags = re.M)
        s = self.__re.sub(r"wat's this", "OwO what's this", s, flags = re.M)
        s = self.__re.sub(r"Wat's [Tt]his", "OwO What's this", s, flags = re.M)
        s = self.__re.sub(r"WAT'S THIS", "OwO what's this".upper(), s, flags = re.M)
        s = self.__re.sub(r"old person", "greymuzzle", s, flags = re.M)
        s = self.__re.sub(r"Old [Pp]erson", "greymuzzle".capitalize(), s, flags = re.M)
        s = self.__re.sub(r"OLD PERSON", "greymuzzle".upper(), s, flags = re.M)
        s = self.__re.sub(r"forgive me father, I have sinned", "sowwy daddy~ I have been naughty", s, flags = re.M)
        s = self.__re.sub(r"Forgive me father, I have sinned", "sowwy daddy~ I have been naughty".capitalize(), s, flags = re.M)
        s = self.__re.sub(r"FORGIVE ME FATHER, I HAVE SINNED", "sowwy daddy~ I have been naughty".upper(), s, flags = re.M)
        s = self.__re.sub(r"your ", "ur ", s, flags = re.M)
        s = self.__re.sub(r"Your ", "Ur ", s, flags = re.M)
        s = self.__re.sub(r"YOUR ", "UR ", s, flags = re.M)
        s = self.__re.sub(r" your", " ur", s, flags = re.M)
        s = self.__re.sub(r" Your", " Ur", s, flags = re.M)
        s = self.__re.sub(r" YOUR", " UR", s, flags = re.M)
        s = self.__re.sub(r"(^your)| your", "ur", s, flags = re.M)
        s = self.__re.sub(r"(^Your)| Your", "Ur", s, flags = re.M)
        s = self.__re.sub(r"(^YOUR)| YOUR", "UR", s, flags = re.M)
        s = self.__re.sub(r"you", "chu", s, flags = re.M)
        s = self.__re.sub(r"You", "Chu", s, flags = re.M)
        s = self.__re.sub(r"YOU", "CHU", s, flags = re.M)
        s = self.__re.sub(r"with ", "wif ", s, flags = re.M)
        s = self.__re.sub(r"With ", "Wif ", s, flags = re.M)
        s = self.__re.sub(r"wITH ", "wIF ", s, flags = re.M)
        s = self.__re.sub(r"what", "wat", s, flags = re.M)
        s = self.__re.sub(r"What", "Wat", s, flags = re.M)
        s = self.__re.sub(r"WHAT", "WAT", s, flags = re.M)
        s = self.__re.sub(r"toe", "toe bean", s, flags = re.M)
        s = self.__re.sub(r"Toe", "Toe Bean", s, flags = re.M)
        s = self.__re.sub(r"TOE", "TOE BEAN", s, flags = re.M)
        s = self.__re.sub(r"this", "dis", s, flags = re.M)
        s = self.__re.sub(r"This", "Dis", s, flags = re.M)
        s = self.__re.sub(r"THIS", "DIS", s, flags = re.M)
        s = self.__re.sub(r"(?!hell\w+)hell", "hecc", s, flags = re.M)
        s = self.__re.sub(r"(?!Hell\w+)Hell", "Hecc", s, flags = re.M)
        s = self.__re.sub(r"(?!HELL\w+)HELL", "HECC", s, flags = re.M)
        s = self.__re.sub(r"the ", "teh ", s, flags = re.M)
        s = self.__re.sub(r"^the$", "teh", s, flags = re.M)
        s = self.__re.sub(r"The ", "Teh ", s, flags = re.M)
        s = self.__re.sub(r"^The$", "Teh", s, flags = re.M)
        s = self.__re.sub(r"THE ", "TEH ", s, flags = re.M)
        s = self.__re.sub(r"^THE$", "TEH", s, flags = re.M)
        s = self.__re.sub(r"tare", "tail", s, flags = re.M)
        s = self.__re.sub(r"Tare", "Tail", s, flags = re.M)
        s = self.__re.sub(r"TARE", "TAIL", s, flags = re.M)
        s = self.__re.sub(r"straight", "gay", s, flags = re.M)
        s = self.__re.sub(r"Straight", "Gay", s, flags = re.M)
        s = self.__re.sub(r"STRAIGHT", "GAY", s, flags = re.M)
        s = self.__re.sub(r"source", "sauce", s, flags = re.M)
        s = self.__re.sub(r"Source", "Sauce", s, flags = re.M)
        s = self.__re.sub(r"SOURCE", "SAUCE", s, flags = re.M)
        s = self.__re.sub(r"(?!slut\w+)slut", "fox", s, flags = re.M)
        s = self.__re.sub(r"(?!Slut\w+)Slut", "Fox", s, flags = re.M)
        s = self.__re.sub(r"(?!SLUT\w+)SLUT", "FOX", s, flags = re.M)
        s = self.__re.sub(r"shout", "awoo", s, flags = re.M)
        s = self.__re.sub(r"Shout", "Awoo", s, flags = re.M)
        s = self.__re.sub(r"SHOUT", "AWOO", s, flags = re.M)
        s = self.__re.sub(r"roar", "rawr", s, flags = re.M)
        s = self.__re.sub(r"Roar", "Rawr", s, flags = re.M)
        s = self.__re.sub(r"ROAR", "RAWR", s, flags = re.M)
        s = self.__re.sub(r"pawlice department", "paw patrol", s, flags = re.M)
        s = self.__re.sub(r"Paw[Ll]ice [Dd]epartment", "Paw Patrol", s, flags = re.M)
        s = self.__re.sub(r"PAWLICE DEPARTMENT", "PAW PATROL", s, flags = re.M)
        s = self.__re.sub(r"police", "pawlice", s, flags = re.M)
        s = self.__re.sub(r"Police", "Pawlice", s, flags = re.M)
        s = self.__re.sub(r"POLICE", "PAWLICE", s, flags = re.M)
        s = self.__re.sub(r"pervert", "furvert", s, flags = re.M)
        s = self.__re.sub(r"Pervert", "Furvert", s, flags = re.M)
        s = self.__re.sub(r"PERVERT", "FURVERT", s, flags = re.M)
        s = self.__re.sub(r"persona", "fursona", s, flags = re.M)
        s = self.__re.sub(r"Persona", "Fursona", s, flags = re.M)
        s = self.__re.sub(r"PERSONA", "FURSONA", s, flags = re.M)
        s = self.__re.sub(r"perfect", "purrfect", s, flags = re.M)
        s = self.__re.sub(r"Perfect", "Purrfect", s, flags = re.M)
        s = self.__re.sub(r"PERFECT", "PURRFECT", s, flags = re.M)
        s = self.__re.sub(r"(?!not\w+)not", "nawt", s, flags = re.M)
        s = self.__re.sub(r"(?!Not\w+)Not", "Nawt", s, flags = re.M)
        s = self.__re.sub(r"(?!NOT\w+)NOT", "NAWT", s, flags = re.M)
        s = self.__re.sub(r"naughty", "nawt", s, flags = re.M)
        s = self.__re.sub(r"Naughty", "Nawt", s, flags = re.M)
        s = self.__re.sub(r"NAUGHTY", "NAWT", s, flags = re.M)
        s = self.__re.sub(r"name", "nyame", s, flags = re.M)
        s = self.__re.sub(r"Name", "Nyame", s, flags = re.M)
        s = self.__re.sub(r"NAME", "NYAME", s, flags = re.M)
        s = self.__re.sub(r"mouth", "maw", s, flags = re.M)
        s = self.__re.sub(r"Mouth", "Maw", s, flags = re.M)
        s = self.__re.sub(r"MOUTH", "MAW", s, flags = re.M)
        s = self.__re.sub(r"love", "luv", s, flags = re.M)
        s = self.__re.sub(r"Love", "Luv", s, flags = re.M)
        s = self.__re.sub(r"LOVE", "LUV", s, flags = re.M)
        s = self.__re.sub(r"lol", "waw", s, flags = re.M)
        s = self.__re.sub(r"Lol", "Waw", s, flags = re.M)
        s = self.__re.sub(r"LOL", "WAW", s, flags = re.M)
        s = self.__re.sub(r"lmao", "hehe~", s, flags = re.M)
        s = self.__re.sub(r"Lmao", "Hehe~", s, flags = re.M)
        s = self.__re.sub(r"LMAO", "HEHE~", s, flags = re.M)
        s = self.__re.sub(r"kiss", "lick", s, flags = re.M)
        s = self.__re.sub(r"Kiss", "Lick", s, flags = re.M)
        s = self.__re.sub(r"KISS", "LICK", s, flags = re.M)
        s = self.__re.sub(r"lmao", "hehe~", s, flags = re.M)
        s = self.__re.sub(r"Lmao", "Hehe~", s, flags = re.M)
        s = self.__re.sub(r"LMAO", "HEHE~", s, flags = re.M)
        s = self.__re.sub(r"hyena", "yeen", s, flags = re.M)
        s = self.__re.sub(r"Hyena", "Yeen", s, flags = re.M)
        s = self.__re.sub(r"HYENA", "YEEN", s, flags = re.M)
        s = self.__re.sub(r"^hi$", "hai", s, flags = re.M)
        s = self.__re.sub(r" hi ", " hai~ ", s, flags = re.M)
        s = self.__re.sub(r"hi(,| )", "hai~ ", s, flags = re.M)
        s = self.__re.sub(r"hi!", "hai!", s, flags = re.M)
        s = self.__re.sub(r"hi\?", "hai?", s, flags = re.M)
        s = self.__re.sub(r"^Hi$", "Hai", s, flags = re.M)
        s = self.__re.sub(r" Hi ", " Hai~ ", s, flags = re.M)
        s = self.__re.sub(r"Hi(,| )", "Hai~ ", s, flags = re.M)
        s = self.__re.sub(r"Hi!", "Hai!", s, flags = re.M)
        s = self.__re.sub(r"Hi\?", "Hai?", s, flags = re.M)
        s = self.__re.sub(r"^HI$", "HAI", s, flags = re.M)
        s = self.__re.sub(r" HI ", " HAI~ ", s, flags = re.M)
        s = self.__re.sub(r"HI(,| )", "HAI~ ", s, flags = re.M)
        s = self.__re.sub(r"HI!", "HAI!", s, flags = re.M)
        s = self.__re.sub(r"HI\?", "HAI?", s, flags = re.M)
        s = self.__re.sub(r"(?!handy)hand", "paw", s, flags = re.M)
        s = self.__re.sub(r"(?!Handy)Hand", "Paw", s, flags = re.M)
        s = self.__re.sub(r"(?!HANDY)HAND", "PAW", s, flags = re.M)
        s = self.__re.sub(r"handy", "pawi", s, flags = re.M)
        s = self.__re.sub(r"Handy", "Pawi", s, flags = re.M)
        s = self.__re.sub(r"HANDY", "PAWI", s, flags = re.M)
        s = self.__re.sub(r"for", "fur", s, flags = re.M)
        s = self.__re.sub(r"For", "Fur", s, flags = re.M)
        s = self.__re.sub(r"FOR", "FUR", s, flags = re.M)
        s = self.__re.sub(r"foot", "footpaw", s, flags = re.M)
        s = self.__re.sub(r"Foot", "Footpaw", s, flags = re.M)
        s = self.__re.sub(r"FOOT", "FOOTPAW", s, flags = re.M)
        s = self.__re.sub(r"father", "daddy", s, flags = re.M)
        s = self.__re.sub(r"Father", "Daddy", s, flags = re.M)
        s = self.__re.sub(r"FATHER", "DADDY", s, flags = re.M)
        s = self.__re.sub(r"fuck", "fluff", s, flags = re.M)
        s = self.__re.sub(r"Fuck", "Fluff", s, flags = re.M)
        s = self.__re.sub(r"FUCK", "FLUFF", s, flags = re.M)
        s = self.__re.sub(r"dragon", "derg", s, flags = re.M)
        s = self.__re.sub(r"Dragon", "Derg", s, flags = re.M)
        s = self.__re.sub(r"DRAGON", "DERG", s, flags = re.M)
        s = self.__re.sub(r"(?!doggy)dog", "good boi", s, flags = re.M)
        s = self.__re.sub(r"(?!Doggy)Dog", "Good boi", s, flags = re.M)
        s = self.__re.sub(r"(?!DOGGY)DOG", "GOOD BOI", s, flags = re.M)
        s = self.__re.sub(r"disease", "pathOwOgen", s, flags = re.M)
        s = self.__re.sub(r"Disease", "PathOwOgen", s, flags = re.M)
        s = self.__re.sub(r"DISEASE", "PATHOWOGEN", s, flags = re.M)
        s = self.__re.sub(r"cyborg|robot|computer", "protogen", s, flags = re.M)
        s = self.__re.sub(r"Cyborg|Robot|Computer", "Protogen", s, flags = re.M)
        s = self.__re.sub(r"CYBORG|ROBOT|COMPUTER", "PROTOGEN", s, flags = re.M)
        s = self.__re.sub(r"(?!children)child", "cub", s, flags = re.M)
        s = self.__re.sub(r"(?!Children)Child", "Cub", s, flags = re.M)
        s = self.__re.sub(r"(?!CHILDREN)CHILD", "CUB", s, flags = re.M)
        s = self.__re.sub(r"(?!cheese[ds])cheese", "sergal", s, flags = re.M)
        s = self.__re.sub(r"(?!Cheese[ds])Cheese", "Sergal", s, flags = re.M)
        s = self.__re.sub(r"(?!CHEESE[DS])CHEESE", "SERGAL", s, flags = re.M)
        s = self.__re.sub(r"celebrity", "popufur", s, flags = re.M)
        s = self.__re.sub(r"Celebrity", "Popufur", s, flags = re.M)
        s = self.__re.sub(r"CELEBRITY", "POPUFUR", s, flags = re.M)
        s = self.__re.sub(r"bye", "bai", s, flags = re.M)
        s = self.__re.sub(r"Bye", "Bai", s, flags = re.M)
        s = self.__re.sub(r"BYE", "BAI", s, flags = re.M)
        s = self.__re.sub(r"butthole", "tailhole", s, flags = re.M)
        s = self.__re.sub(r"Butthole", "Tailhole", s, flags = re.M)
        s = self.__re.sub(r"BUTTHOLE", "TAILHOLE", s, flags = re.M)
        s = self.__re.sub(r"bulge", "bulgy-wulgy", s, flags = re.M)
        s = self.__re.sub(r"Bulge", "Bulgy-wulgy", s, flags = re.M)
        s = self.__re.sub(r"BULGE", "BULGY-WULGY", s, flags = re.M)
        s = self.__re.sub(r"bite", "nom", s, flags = re.M)
        s = self.__re.sub(r"Bite", "Nom", s, flags = re.M)
        s = self.__re.sub(r"BITE", "NOM", s, flags = re.M)
        s = self.__re.sub(r"awful", "pawful", s, flags = re.M)
        s = self.__re.sub(r"Awful", "Pawful", s, flags = re.M)
        s = self.__re.sub(r"AWFUL", "PAWFUL", s, flags = re.M)
        s = self.__re.sub(r"awesome", "pawsome", s, flags = re.M)
        s = self.__re.sub(r"Awesome", "Pawsome", s, flags = re.M)
        s = self.__re.sub(r"AWESOME", "PAWSOME", s, flags = re.M)
        s = self.__re.sub(r"(?!ahh(h)+)ahh", "murr", s, flags = re.M)
        s = self.__re.sub(r"(?!Ahh[Hh]+)Ahh", "Murr", s, flags = re.M)
        s = self.__re.sub(r"(?!AHH(H)+)AHH", "MURR", s, flags = re.M)
        s = self.__re.sub(r"(?![Gg]reymuzzle|[Tt]ail(hole)?|[Pp]aw [Pp]atrol|[Pp]awlice|luv|lick|[Ff]luff|[Ss]ergal|[Pp]awful)l", "w", s, flags = re.M)
        s = self.__re.sub(r"(?!GREYMUZZLE|TAIL(HOLE)?|PAW PATROL|PAWLICE|L(uv|UV)|L(ick|ICK)|FLUFF|SERGAL|PAWFUL)L", "W", s, flags = re.M)
        s = self.__re.sub(r"(?![Gg]reymuzzle|ur|[Rr]awr|[Ff]ur(sona|vert)?|[Pp]urrfect|[Vv]ore|[Dd]erg|[Pp]rotogen|[Ss]ergal|[Pp]opufur|[Mm]urr)r", "w", s, flags = re.M)
        s = self.__re.sub(r"(?!GREYMUZZLE|UR|RAWR|FUR(SONA|VERT)?|PURRFECT|VORE|DERG|PROTOGEN|SERGAL|POPUFUR|MURR)R", "W", s, flags = re.M)
        # above: 0.3.26a3, below: 0.3.26b1
        s = self.__re.sub(r"gweymuzzwe", "greymuzzle", s, flags = re.M)
        s = self.__re.sub(r"Gweymuzzwe", "Greymuzzle", s, flags = re.M)
        s = self.__re.sub(r"GWEYMUZZWE", "GREYMUZZLE", s, flags = re.M)
        s = self.__re.sub(r"taiwhowe", "tailhole", s, flags = re.M)
        s = self.__re.sub(r"Taiwhowe", "Tailhole", s, flags = re.M)
        s = self.__re.sub(r"TAIWHOWE", "TAILHOLE", s, flags = re.M)
        s = self.__re.sub(r"paw patwow", "paw patrol", s, flags = re.M)
        s = self.__re.sub(r"Paw Patwow", "Paw Patrol", s, flags = re.M)
        s = self.__re.sub(r"PAW PATWOW", "PAW PATROL", s, flags = re.M)
        s = self.__re.sub(r"pawwice", "pawlice", s, flags = re.M)
        s = self.__re.sub(r"Pawwice", "Pawlice", s, flags = re.M)
        s = self.__re.sub(r"PAWWICE", "PAWLICE", s, flags = re.M)
        s = self.__re.sub(r"wuv", "luv", s, flags = re.M)
        s = self.__re.sub(r"Wuv", "Luv", s, flags = re.M)
        s = self.__re.sub(r"WUV", "LUV", s, flags = re.M)
        s = self.__re.sub(r"wick", "lick", s, flags = re.M)
        s = self.__re.sub(r"Wick", "Lick", s, flags = re.M)
        s = self.__re.sub(r"WICK", "LICK", s, flags = re.M)
        s = self.__re.sub(r"fwuff", "fluff", s, flags = re.M)
        s = self.__re.sub(r"Fwuff", "Fluff", s, flags = re.M)
        s = self.__re.sub(r"FWUFF", "FLUFF", s, flags = re.M)
        s = self.__re.sub(r"sewgaw", "sergal", s, flags = re.M)
        s = self.__re.sub(r"Sewgaw", "Sergal", s, flags = re.M)
        s = self.__re.sub(r"SEWGAW", "SERGAL", s, flags = re.M)
        s = self.__re.sub(r"pawfuw", "pawful", s, flags = re.M)
        s = self.__re.sub(r"Pawfuw", "Pawful", s, flags = re.M)
        s = self.__re.sub(r"PAWFUW", "PAWFUL", s, flags = re.M)
        s = self.__re.sub(r"(?!uwu)uw", "ur", s, flags = re.M)
        s = self.__re.sub(r"(?!Uwu)Uw", "Ur", s, flags = re.M)
        s = self.__re.sub(r"(?!UWU)UW", "UR", s, flags = re.M)
        s = self.__re.sub(r"waww", "rawr", s, flags = re.M)
        s = self.__re.sub(r"Waww", "Rawr", s, flags = re.M)
        s = self.__re.sub(r"WAWW", "RAWR", s, flags = re.M)
        s = self.__re.sub(r"fuw", "fur", s, flags = re.M)
        s = self.__re.sub(r"Fuw", "Fur", s, flags = re.M)
        s = self.__re.sub(r"FUW", "FUR", s, flags = re.M)
        s = self.__re.sub(r"furvewt", "furvert", s, flags = re.M)
        s = self.__re.sub(r"Furvewt", "Furvert", s, flags = re.M)
        s = self.__re.sub(r"FURVEWT", "FURVERT", s, flags = re.M)
        s = self.__re.sub(r"puwwfect", "purrfect", s, flags = re.M)
        s = self.__re.sub(r"Puwwfect", "Purrfect", s, flags = re.M)
        s = self.__re.sub(r"PUWWFECT", "PURRFECT", s, flags = re.M)
        s = self.__re.sub(r"vowe", "vore", s, flags = re.M)
        s = self.__re.sub(r"Vowe", "Vore", s, flags = re.M)
        s = self.__re.sub(r"VOWE", "VORE", s, flags = re.M)
        s = self.__re.sub(r"dewg", "derg", s, flags = re.M)
        s = self.__re.sub(r"Dewg", "Derg", s, flags = re.M)
        s = self.__re.sub(r"DEWG", "DERG", s, flags = re.M)
        s = self.__re.sub(r"pwotogen", "protogen", s, flags = re.M)
        s = self.__re.sub(r"Pwotogen", "Protogen", s, flags = re.M)
        s = self.__re.sub(r"PWOTOGEN", "PROTOGEN", s, flags = re.M)
        s = self.__re.sub(r"popufuw", "popufur", s, flags = re.M)
        s = self.__re.sub(r"Popufuw", "Popufur", s, flags = re.M)
        s = self.__re.sub(r"POPUFUW", "POPUFUR", s, flags = re.M)
        s = self.__re.sub(r"muww", "murr", s, flags = re.M)
        s = self.__re.sub(r"Muww", "Murr", s, flags = re.M)
        s = self.__re.sub(r"MUWW", "MURR", s, flags = re.M)
        # end 0.3.26b1; start 0.3.26rc2
        s = self.__re.sub(r"furwy", "fuwwy", s, flags = re.M)
        s = self.__re.sub(r"Furwy", "Fuwwy", s, flags = re.M)
        s = self.__re.sub(r"FURWY", "FUWWY", s, flags = re.M)
        s = self.__re.sub(r"UrU", "UwU", s, flags = re.M)
        s = self.__re.sub(r"Uru", "Uwu", s, flags = re.M)
        s = self.__re.sub(r"uru", "uwu", s, flags = re.M)
        s = self.__re.sub(r"URU", "UWU", s, flags = re.M)
        s = self.__re.sub(r"femboy", "femboi", s, flags = re.M)
        s = self.__re.sub(r"Femboy", "Femboi", s, flags = re.M)
        s = self.__re.sub(r"FEMBOY", "FEMBOI", s, flags = re.M)
        s = self.__re.sub(r":<", "x3", s, flags = re.M)
        # end 0.3.26rc2; start 0.3.26
        s = self.__re.sub(r"ding", "beep", s, flags = re.M)
        s = self.__re.sub(r"Ding", "Beep", s, flags = re.M)
        s = self.__re.sub(r"DING", "BEEP", s, flags = re.M)
        s = self.__re.sub(r"shourd", "shouwd", s, flags = re.M)
        s = self.__re.sub(r"Shourd", "Shouwd", s, flags = re.M)
        s = self.__re.sub(r"SHOURD", "SHOUWD", s, flags = re.M)
        s = self.__re.sub(r"course", "couwse", s, flags = re.M)
        s = self.__re.sub(r"Course", "Couwse", s, flags = re.M)
        s = self.__re.sub(r"COURSE", "COUWSE", s, flags = re.M)
        return s
    
    @_cm
    def owoify(self, s: _uni[str, __tc.StringVar], /):
        """
        \\@since 0.3.9 \\
        \\@lifetime ≥ 0.3.9; < 0.3.24; ≥ 0.3.25
        ```
        "class method" in class Tense
        ```
        Joke method translating a string to furry equivalent. \\
        Basing on https://lingojam.com/FurryTalk. Several words \\
        aren't included normally (0.3.26a3, 0.3.26b1, 0.3.26rc2, \\
        0.3.26), still, most are, several have different translations
        """
        return self.__local_owoify_template(s if self.isString(s) else s.get())
    
    @_cm
    def uwuify(self, s: _uni[str, __tc.StringVar], /):
        """
        \\@since 0.3.27b2 \\
        \\@lifetime ≥ 0.3.27b2
        ```
        "class method" in class Tense
        ```
        Alias to `Tense.owoify()`
        """
        return self.__local_owoify_template(s if self.isString(s) else s.get())
    
    @_cm
    def aeify(self, s: _uni[str, __tc.StringVar], /):
        """
        \\@since 0.3.9 \\
        \\@lifetime ≥ 0.3.9; < 0.3.24; ≥ 0.3.26a4
        ```
        "class method" in class Tense
        ```
        Joke method which converts every a and e into \u00E6. Ensure your \\
        compiler reads characters from ISO/IEC 8859-1 encoding, because \\
        without it you might meet question marks instead
        """
        _s = s if self.isString(s) else s.get()
        _s = self.__re.sub(r"[ae]", "\u00E6", _s, flags = re.M)
        _s = self.__re.sub(r"[AE]", "\u00C6", _s, flags = re.M)
        return _s
    
    @_cm
    def oeify(self, s: _uni[str, __tc.StringVar], /):
        """
        \\@since 0.3.9 \\
        \\@lifetime ≥ 0.3.9; < 0.3.24; ≥ 0.3.26a4
        ```
        "class method" in class Tense
        ```
        Joke method which converts every o and e into \u0153. Ensure your \\
        compiler reads characters from ISO/IEC 8859-1 encoding, because \\
        without it you might meet question marks instead
        """
        _s = s if self.isString(s) else s.get()
        _s = self.__re.sub(r"[oe]", "\u0153", _s, flags = re.M)
        _s = self.__re.sub(r"[OE]", "\u0152", _s, flags = re.M)
        return _s
    __all__ = [n for n in locals() if n[:1] != "_"]
    "\\@since 0.3.26rc2"
    __dir__ = [n for n in locals() if n[:1] != "_"]
    "\\@since 0.3.26rc2"

tense = Tense
TS = Tense()
"\\@since 0.3.27a5. Instance of `Tense` to use for `>>` and `<<` operators especially"


class RGB(tc.Final):
    """
    \\@since 0.3.28
    
    Auxiliary class for `Color` class. Represents red-green-blue color representation.
    """
    def __init__(self, red = 0, green = 0, blue = 0, /):
        
        _parameters = {
            "red": red,
            "green": green,
            "blue": blue
        }
        
        for key in _parameters:
            
            if not isinstance(_parameters[key], int) or (isinstance(_parameters[key], int) and _parameters[key] not in abroad(0x100)):
                error = TypeError("expected a non-negative integer in parameter '" + key + "' in range 0-255")
                raise error
            
        self.__rgb = (red, green, blue)
        
    def __str__(self):
        """
        \\@since 0.3.28
        """
        return type(self).__name__ + "({})".format(", ".join([str(e) for e in self.__rgb]))
        
    def __repr__(self):
        """
        \\@since 0.3.28
        """
        return "<{} object: {}>".format(__module__ + "." + type(self).__name__, self.__str__())
    
    def __hex__(self):
        """
        \\@since 0.3.28
        
        Provides conversion to hexadecimal format
        """
        _r = hex(self.__rgb[0])[2:] if self.__rgb[0] >= 0x10 else "0" + hex(self.__rgb[0])[2:]
        _g = hex(self.__rgb[1])[2:] if self.__rgb[1] >= 0x10 else "0" + hex(self.__rgb[1])[2:]
        _b = hex(self.__rgb[2])[2:] if self.__rgb[2] >= 0x10 else "0" + hex(self.__rgb[2])[2:]
        return "0x" + _r + _g + _b
    
    def __int__(self):
        """
        \\@since 0.3.28
        
        Converts RGB tuple into its corresponding integer representation
        """
        return int(self.__hex__()[2:], base = 16)
    
    # little deviation from type hinting in methods below
    # read document strings to figure it out
    def __lt__(self, other):
        """
        \\@since 0.3.28
        
        To return true, following conditions must be satisfied:
        - `int(self) < int(other)`
        - `other` must be instance of `RGB` class
        """
        return self.__int__() < other.__int__() if isinstance(other, type(self)) else False
    
    def __gt__(self, other):
        """
        \\@since 0.3.28
        
        To return true, following conditions must be satisfied:
        - `int(self) > int(other)`
        - `other` must be instance of `RGB` class
        """
        return self.__int__() > other.__int__() if isinstance(other, type(self)) else False
    
    def __eq__(self, other):
        """
        \\@since 0.3.28
        
        To return true, following conditions must be satisfied:
        - `int(self) == int(other)`
        - `other` must be instance of `RGB` class
        """
        return self.__int__() == other.__int__() if isinstance(other, type(self)) else False
    
    def __le__(self, other):
        """
        \\@since 0.3.28
        
        To return true, following conditions must be satisfied:
        - `int(self) <= int(other)`
        - `other` must be instance of `RGB` class
        """
        return self.__int__() <= other.__int__() if isinstance(other, type(self)) else False
    
    def __ge__(self, other):
        """
        \\@since 0.3.28
        
        To return true, following conditions must be satisfied:
        - `int(self) >= int(other)`
        - `other` must be instance of `RGB` class
        """
        return self.__int__() >= other.__int__() if isinstance(other, type(self)) else False
    
    def __ne__(self, other):
        """
        \\@since 0.3.28
        
        To return true, following conditions must be satisfied:
        - `int(self) != int(other)`
        - `other` must be instance of `RGB` class
        """
        return self.__int__() != other.__int__() if isinstance(other, type(self)) else False
    
    def __pos__(self):
        """
        \\@since 0.3.28
        
        Returns a RGB tuple
        """
        return self.__rgb
    
    def __neg__(self):
        """
        \\@since 0.3.28
        
        Returns a RGB tuple
        """
        return self.__rgb
    
    def __invert__(self):
        """
        \\@since 0.3.28
        
        Returns a RGB tuple
        """
        return self.__rgb
    
    
class CMYK(tc.Final):
    """
    \\@since 0.3.28
    
    Auxiliary class for `Color` class. Represents cyan-magenta-yellow color representation. \\
    Once instantiated, returns `RGB` class instance, only with inverted color values, that is: \\
    255 is 0, 254 is 1, 253 is 2 and so on, up to 0 being 255.
    """
    
    def __new__(self, cyan = 0, magenta = 0, yellow = 0, /):
        
        _parameters = {
            "cyan": cyan,
            "magenta": magenta,
            "yellow": yellow
        }
        
        for key in _parameters:
            
            if not isinstance(_parameters[key], int) or (isinstance(_parameters[key], int) and _parameters[key] not in abroad(0x100)):
                error = TypeError("expected a non-negative integer in parameter '" + key + "' in range 0-255")
                raise error
            
        return RGB(
            0xff - cyan,
            0xff - magenta,
            0xff - yellow
        )
        
        
    

class _FileRead(tc.IntegerFlag):
    "\\@since 0.3.26rc2"
    CHARS = 0
    LINES = tc.auto()

# _FileReadType = _lit[_FileRead.CHARS, _FileRead.LINES] # unnecessary since 0.3.27b2
_T_stringOrIterable = _var("_T_stringOrIterable", bound = _uni[str, tc.Iterable[str]])

class File:
    """
    \\@since 0.3.25 \\
    \\@author Aveyzan
    ```
    // created 18.07.2024
    in module tense
    ```
    Providing file IO operations
    """
    from . import types_collection as __tc
    import pickle as __pi, io as __io, typing as __tp
    CHARS = _FileRead.CHARS
    LINES = _FileRead.LINES
    __filename = None
    __file = None
    __seq = None
    def __init__(self, file: _FileType, mode: _FileMode, buffering = -1, encoding: _opt[str] = None, errors: _opt[str] = None, newline: _opt[str] = None, closefd = True, opener: _opt[_FileOpener] = None) -> None:
        import io as io, typing as __tp
        if mode in ('rb+', 'r+b', '+rb', 'br+', 'b+r', '+br', 'wb+', 'w+b', '+wb', 'bw+', 'b+w', '+bw', 'ab+', 'a+b', '+ab', 'ba+', 'b+a', '+ba', 'xb+', 'x+b', '+xb', 'bx+', 'b+x', '+bx', 'rb', 'br', 'rbU', 'rUb', 'Urb', 'brU', 'bUr', 'Ubr', 'wb', 'bw', 'ab', 'ba', 'xb', 'bx'):
            if buffering == 0:
                # expected FileIO
                self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
            elif buffering in (-1, 1):
                if mode in ('wb', 'bw', 'ab', 'ba', 'xb', 'bx'):
                    # expected BufferedWriter
                    self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
                elif mode in ('rb', 'br', 'rbU', 'rUb', 'Urb', 'brU', 'bUr', 'Ubr'):
                    # expected BufferedReader
                    self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
                else:
                    # expected BufferedRandom
                    self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
            else:
                # expected BinaryIO
                self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
        elif mode in ('r+', '+r', 'rt+', 'r+t', '+rt', 'tr+', 't+r', '+tr', 'w+', '+w', 'wt+', 'w+t', '+wt', 'tw+', 't+w', '+tw', 'a+', '+a', 'at+', 'a+t', '+at', 'ta+', 't+a', '+ta', 'x+', '+x', 'xt+', 'x+t', '+xt', 'tx+', 't+x', '+tx', 'w', 'wt', 'tw', 'a', 'at', 'ta', 'x', 'xt', 'tx', 'r', 'rt', 'tr', 'U', 'rU', 'Ur', 'rtU', 'rUt', 'Urt', 'trU', 'tUr', 'Utr'):
            # expected TextIOWrapper
            self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
        else:
            # expected IO[Any]
            self.__fileinstance = open(file = file, mode = mode, buffering = buffering, encoding = encoding, errors = errors, newline = newline, closefd = closefd, opener = opener)
        self.__file = file
        self.__seq = [file, mode, buffering, encoding, errors, newline, closefd, opener]
    def read(self, size = -1, mode: _FileRead = CHARS):
        "\\@since 0.3.26rc2"
        if not Tense.isInteger(size):
            error = TypeError("Expected 'size' parameter to be an integer.")
            raise error
        if self.__fileinstance is not None:
            if mode == self.CHARS:
                _r = self.__fileinstance.read(size)
                return str(_r) if not Tense.isString(_r) else _r
            elif mode == self.LINES:
                _r = self.__fileinstance.readlines(size)
                return list(str(n) for n in _r if not Tense.isString(n))
            else:
                error = TypeError("Expected one of constants: 'CHARS', 'LINES'")
                raise error
        else:
            error = (self.__tc.NotInitializedError, "Class was not initialized")
            raise error
    def write(self, content: _T_stringOrIterable):
        "\\@since 0.3.26rc2"
        from collections.abc import Iterable
        if not Tense.isString(content) and not isinstance(content, Iterable):
            error = TypeError("Expected a string iterable or a string")
            raise error
        if self.__fileinstance is not None:
            if self.__fileinstance.writable():
                if Tense.isString(content):
                    self.__fileinstance.write(content)
                else:
                    self.__fileinstance.writelines(content)
            else:
                error = (IOError, "File is not writable")
                raise error
        else:
            error = (self.__tc.NotInitializedError, "Class was not initialized")
            raise error
    def pickle(self, o: object, protocol: _opt[int] = None, *, fixImports = True):
        "\\@since 0.3.26rc2"
        if isinstance(self.__fileinstance, (
            # only on binary mode files
            self.__io.BufferedRandom,
            self.__io.BufferedReader,
            self.__io.BufferedWriter
        )):
            self.__pi.dump(o, self.__fileinstance, protocol, fix_imports = fixImports)
        else:
            error = (IOError, "File is not open in binary mode")
            raise error
    def unpickle(self, *, fixImports = True, encoding = "ASCII", errors = "strict", buffers: _opt[__tp.Iterable[__tp.Any]] = ()):
        "\\@since 0.3.26rc2"
        a = []
        while True:
            try:
                a.append(self.__pi.load(self.__fileinstance, fix_imports = fixImports, encoding = encoding, errors = errors, buffers = buffers))
            except:
                break
        return a

class FinalVar:
    """
    \\@since 0.3.26rc1 \\
    \\@lifetime ≥ 0.3.26rc1
    ```
    in module tense
    ```
    A class-like function (since 0.3.26rc2 a class) referring \\
    to class `tense.types_collection.FinalVar`. This creates a final variable

    Use `~instance`, `+instance` or `-instance` to return \\
    value passed to the constructor.

    To allow it work in classes, you need to initialize them to obtain the value. \\
    In case of variables in global scope it works normally.
    """

    def __new__(cls, v: _T, /):
        """
        \\@since 0.3.26rc1 \\
        \\@lifetime ≥ 0.3.26rc1
        ```
        in module tense
        ```
        A class-like function (since 0.3.26rc2 a class) referring \\
        to class `tense.types_collection.FinalVar`. This creates a final variable

        Use `~instance`, `+instance` or `-instance` to return \\
        value passed to the constructor.

        To allow it work in classes, you need to initialize them to obtain the value. \\
        In case of variables in global scope it works normally.
        """
        from .types_collection import FinalVar as _FinalVar
        return _FinalVar(v)
    
class ClassLike:
    """
    \\@since 0.3.27a3 \\
    \\@lifetime ≥ 0.3.27a3
    ```
    in module tense
    ```
    A class being formal reference to class `tense.types_collection.ClassLike`
    """

    def __new__(cls, f: tc.Callable[_P, _T]):
        """
        \\@since 0.3.27a3 \\
        \\@lifetime ≥ 0.3.27a3
        ```
        in module tense
        ```
        A class being formal reference to class `tense.types_collection.ClassLike`
        """
        from .types_collection import ClassLike as _ClassLike
        return _ClassLike(f)

# class _ChangeVarState(tc.IntegerFlag): # to 0.3.28
class _ChangeVarState(tc.Enum):
    "\\@since 0.3.26rc1. Internal class for `ChangeVar.setState()` method"
    I = 1
    D = 2

# _ChangeVarStateSelection = _lit[_ChangeVarState.D, _ChangeVarState.I] # unnecessary since 0.3.27b2

class ChangeVar(tc.UnaryOperable, tc.Comparable, tc.AdditionReassignable, tc.SubtractionReassignable):
    """
    \\@since 0.3.26rc1 \\
    \\@lifetime ≥ 0.3.26rc1
    ```
    in module tense
    ```
    Auxiliary class for creating sentinel inside `while` loop.

    Use `~instance` to receive integer value. \\
    Use `+instance` to increment by 1. \\
    Use `-instance` to decrement by 1. \\
    Use `instance += any_int` to increment by `any_int`. \\
    Use `instance -= any_int` to decrement by `any_int`.
    """
    from . import types_collection as __tc
    D = _ChangeVarState.D
    I = _ChangeVarState.I
    __v = 0
    __m = 1
    __default = 0

    def __init__(self, initialValue = 0):
        if not Tense.isInteger(initialValue):
            error = TypeError("Expected an integer value")
            raise error
        self.__v = initialValue
        self.__default = initialValue

    def __pos__(self):
        self.__v += self.__m

    def __neg__(self):
        self.__v -= self.__m

    def __invert__(self):
        return self.__v
    
    def __eq__(self, other: int):
        return self.__v == other
    
    def __contains__(self, value: int):
        return self.__v == value
    
    def __ne__(self, other: int):
        return self.__v != other
    
    def __ge__(self, other: int):
        return self.__v >= other
    
    def __gt__(self, other: int):
        return self.__v > other
    
    def __le__(self, other: int):
        return self.__v <= other
    
    def __lt__(self, other: int):
        return self.__v < other
    
    def __iadd__(self, other: int):
        if not Tense.isInteger(self.__v):
            error = (self.__tc.NotInitializedError, "Class was not initialized")
            raise error
        _tmp = self.__v
        _tmp += other
        self.__v = _tmp
        return _tmp
    
    def __isub__(self, other: int):
        if not Tense.isInteger(self.__v):
            error = (self.__tc.NotInitializedError, "Class was not initialized")
            raise error
        _tmp = self.__v
        _tmp -= other
        self.__v = _tmp
        return _tmp
    
    def reset(self):
        """
        \\@since 0.3.26rc1

        Reset the counter to value passed to the constructor, or - \\
        if `setDefault()` was invoked before - to value passed \\
        to that method.
        """
        self.__v = self.__default

    def setDefault(self, value: int):
        """
        \\@since 0.3.26rc1

        Set a new default value. This overwrites current default value. \\
        Whether `reset()` method is used after, internal variable \\
        will have the default value, which was passed to this method. \\
        Otherwise it will refer to value passed to constructor
        """
        if not Tense.isInteger(value):
            error = TypeError("Expected an integer value")
            raise error
        self.__default = abs(value)

    def setState(self, s: _ChangeVarState = I, m: int = 1):
        """
        \\@since 0.3.26rc1

        Alternative for `+` and `-` unary operators.

        If `D` for `s` parameter is passed, sentinel will be decremented \\
        by 1, otherwise incremented by 1 (option `I`). Additionally, you \\
        can set a different step via `m` parameter.
        """
        _m = m
        if not Tense.isInteger(_m):
            err, _s = TypeError("Expected integer value for 'm' parameter")
            raise err(_s)
        elif abs(_m) == 0:
            _m = 1
        if s == self.D:
            self.__v -= abs(_m)
        elif s == self.I:
            self.__v += abs(_m)
        else:
            err, _s = TypeError("Expected 'ChangeVar.I' or 'ChangeVar.D' for 's' parameter")
            raise err(_s)
        
    def setModifier(self, m: int):
        """
        \\@since 0.3.26rc1

        Changes behavior for `+` and `-` unary operators. \\
        If passed integer value was negative, code will \\
        retrieve absolute value of it. If 0 passed, used will be 1
        """
        if not Tense.isInteger(m):
            error = TypeError("Expected integer value for 'm' parameter")
            raise error
        elif abs(m) == 0:
            self.__m == 1
        self.__m = abs(m)

_Color = tc.Union[tc.ColorType, RGB]

# class _ColorStyling(tc.IntegerFlag): ### to 0.3.27
class _ColorStyling(tc.Enum):
    "\\@since 0.3.26rc1. Internal class for `%` operator in class `tense.Color`."
    NORMAL = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    REVERSE = 7
    HIDE = 8
    STRIKE = 9
    PRIMARY_FONT = 10
    # 11-19 alternative font
    GOTHIC = 20
    DOUBLE_UNDERLINE = 21
    NORMAL_INTENSITY = 22
    NO_ITALIC = 23
    NO_UNDERLINE = 24
    NO_BLINK = 25
    PROPORTIONAL = 26 # corrected mistake! 0.3.26rc2
    NO_REVERSE = 27
    UNHIDE = 28
    NO_STRIKE = 29
    # 30-37 foreground color, 3-bit
    # 38 foreground color, 3 4 8 24-bit
    FOREGROUND_DEFAULT = 39
    # 40-47 background color, 3-bit
    # 48 background color, 3 4 8 24-bit
    BACKGROUND_DEFAULT = 49
    NO_PROPOTIONAL = 50
    FRAME = 51
    ENCIRCLE = 52
    OVERLINE = 53
    NO_FRAME = 54 # including "no encircle"
    NO_OVERLINE = 55
    # 56 and 57 undefined
    # 58 underline color, 3 4 8 24-bit
    UNDERLINE_DEFAULT = 59
    IDEOGRAM_UNDERLINE = 60
    IDEOGRAM_DOUBLE_UNDERLINE = 61
    IDEOGRAM_OVERLINE = 62
    IDEOGRAM_DOUBLE_OVERLINE = 63
    IDEOGRAM_STRESS = 64
    NO_IDEOGRAM = 65
    # 66-72 undefined
    SUPERSCRIPT = 73
    SUBSCRIPT = 74
    NO_SUPERSCRIPT = 75 # also counts as no subscript
    # 76 undefined but recommended value: no subscript
    # 77-89 undefined
    # 90-97 bright foreground color, 4-bit
    # 100-107 bright background color, 4-bit

# class _ColorAdvancedStyling(tc.IntegerFlag): ### to 0.3.27
class _ColorAdvancedStyling(tc.Enum):
    "\\@since 0.3.26rc2. Internal class for `%` operator in class `tense.Color`."
    # 2x
    BOLD_ITALIC = 1000
    BOLD_UNDERLINE = 1001
    BOLD_STRIKE = 1002
    BOLD_OVERLINE = 1003
    ITALIC_UNDERLINE = 1004
    ITALIC_STRIKE = 1005
    ITALIC_OVERLINE = 1006
    UNDERLINE_STRIKE = 1007
    UOLINE = 1008
    STRIKE_OVERLINE = 1009
    # 3x
    BOLD_ITALIC_UNDERLINE = 1100
    BOLD_ITALIC_STRIKE = 1101
    BOLD_ITALIC_OVERLINE = 1102
    BOLD_UNDERLINE_STRIKE = 1103
    BOLD_UOLINE = 1104
    ITALIC_UNDERLINE_STRIKE = 1105
    ITALIC_UOLINE = 1106
    ITALIC_STRIKE_OVERLINE = 1107
    STRIKE_UOLINE = 1108

_ColorStylingType = _lit[
    _ColorStyling.NORMAL,
    _ColorStyling.BOLD,
    _ColorStyling.FAINT,
    _ColorStyling.ITALIC,
    _ColorStyling.UNDERLINE,
    _ColorStyling.SLOW_BLINK,
    _ColorStyling.RAPID_BLINK,
    _ColorStyling.REVERSE,
    _ColorStyling.HIDE,
    _ColorStyling.STRIKE,
    _ColorStyling.DOUBLE_UNDERLINE,
    # _ColorStyling.PROPORTIONAL, cancelled 0.3.26rc2
    _ColorStyling.FRAME,
    _ColorStyling.ENCIRCLE,
    _ColorStyling.OVERLINE,
    # below: since 0.3.26rc2
    _ColorStyling.SUPERSCRIPT,
    _ColorStyling.SUBSCRIPT,
    # 2x
    _ColorAdvancedStyling.BOLD_ITALIC,
    _ColorAdvancedStyling.BOLD_UNDERLINE,
    _ColorAdvancedStyling.BOLD_STRIKE,
    _ColorAdvancedStyling.BOLD_OVERLINE,
    _ColorAdvancedStyling.ITALIC_UNDERLINE,
    _ColorAdvancedStyling.ITALIC_STRIKE,
    _ColorAdvancedStyling.ITALIC_OVERLINE,
    _ColorAdvancedStyling.UNDERLINE_STRIKE,
    _ColorAdvancedStyling.UOLINE,
    _ColorAdvancedStyling.STRIKE_OVERLINE,
    # 3x
    _ColorAdvancedStyling.BOLD_ITALIC_UNDERLINE,
    _ColorAdvancedStyling.BOLD_ITALIC_STRIKE,
    _ColorAdvancedStyling.BOLD_ITALIC_OVERLINE,
    _ColorAdvancedStyling.BOLD_UNDERLINE_STRIKE,
    _ColorAdvancedStyling.BOLD_UOLINE,
    _ColorAdvancedStyling.ITALIC_UNDERLINE_STRIKE,
    _ColorAdvancedStyling.ITALIC_UOLINE,
    _ColorAdvancedStyling.ITALIC_STRIKE_OVERLINE,
    _ColorAdvancedStyling.STRIKE_UOLINE
]

class Color(tc.ModuloOperable[_ColorStylingType, str], tc.UnaryOperable):
    """
    \\@since 0.3.26rc1 \\
    \\@lifetime ≥ 0.3.26rc1
    ```
    in module tense
    ```
    Deputy of experimental class `tense.extensions.ANSIColor` (≥ 0.3.24; < 0.3.26rc1).

    `+instance`, `-instance` and `~instance` allow to get colored string. \\
    `instance % _ColorStylingType` to decorate the string more. Examples::

        from tense import Color
        Color("Tense") % Color.BOLD
        Color("Countryside!", 8, 0o105) % Color.ITALIC # italic, blue text
        Color("Creativity!", 24, 0xc0ffee) % Color.BOLD # bold, c0ffee hex code text
        Color("Illusive!", 24, 0, 0xc0ffee) % Color.BOLD # bold, c0ffee hex code background, black text

    You are discouraged to do operations on these constants; also, since 0.3.26rc2 \\
    there are constants for advanced styling, like::

        Color("Lines!", 8, 93) % Color.UOLINE # lines above and below text

    **Warning**: 24-bit colors remains an experimental thing. Rather use 8-bit \\
    more than 24-bit color palette by then. `0xff` means blue, `0xff00` means lime, \\
    and `0xff0000` means red. For white use `0xffffff`, black is just `0x0`. Moreover, \\
    24-bit colors load a bit longer than 8-bit ones. Currently experimenting with aliased \\
    hex notation (as in CSS `#0f0` meaning `#00ff00`), with zeros preceding and placed on \\
    the end of the hex code notation.
    """
    import re as __re, os as __os
    __fg = None
    __bg = None
    if False: # 0.3.27
        __un = None
    __text = ""
    __bits = 24

    NORMAL = _ColorStyling.NORMAL
    "\\@since 0.3.26rc1. Mere text"
    BOLD = _ColorStyling.BOLD
    "\\@since 0.3.26rc1. Text becomes bold"
    FAINT = _ColorStyling.FAINT
    "\\@since 0.3.26rc1. Also works as 'decreased intensity' or 'dim'"
    ITALIC = _ColorStyling.ITALIC
    "\\@since 0.3.26rc1. Text becomes oblique. Not widely supported"
    UNDERLINE = _ColorStyling.UNDERLINE
    "\\@since 0.3.26rc1. Text becomes underlined. Marked *experimental* as experimenting with underline colors, but normally it is OK to use"
    SLOW_BLINK = _ColorStyling.SLOW_BLINK
    "\\@since 0.3.26rc1. Text will blink for less than 150 times per minute"
    RAPID_BLINK = _ColorStyling.RAPID_BLINK
    "\\@since 0.3.26rc1. Text will blink for more than 150 times per minute. Not widely supported"
    REVERSE = _ColorStyling.REVERSE
    "\\@since 0.3.26rc2. Swap text and background colors"
    HIDE = _ColorStyling.HIDE
    "\\@since 0.3.26rc1. Text becomes transparent"
    STRIKE = _ColorStyling.STRIKE
    "\\@since 0.3.26rc1. Text becomes crossed out"
    DOUBLE_UNDERLINE = _ColorStyling.DOUBLE_UNDERLINE
    "\\@since 0.3.26rc2. Text becomes doubly underlined"
    # PROPORTIONAL = _ColorStyling.PROPORTIONAL
    "\\@lifetime >= 0.3.26rc1; < 0.3.26rc2. Proportional spacing. *Experimental*"
    FRAME = _ColorStyling.FRAME
    "\\@since 0.3.26rc1. Implemented in mintty as 'emoji variation selector'"
    ENCIRCLE = _ColorStyling.ENCIRCLE
    "\\@since 0.3.26rc1. Implemented in mintty as 'emoji variation selector'"
    OVERLINE = _ColorStyling.OVERLINE
    "\\@since 0.3.26rc1. Text becomes overlined"
    SUPERSCRIPT = _ColorStyling.SUPERSCRIPT
    "\\@since 0.3.26rc2. Text becomes superscripted (implemented in mintty only)"
    SUBSCRIPT = _ColorStyling.SUBSCRIPT
    "\\@since 0.3.26rc2. Text becomes subscripted (implemented in mintty only)"
    # 2x
    BOLD_ITALIC = _ColorAdvancedStyling.BOLD_ITALIC
    "\\@since 0.3.26rc2. Text becomes bold and oblique"
    BOLD_UNDERLINE = _ColorAdvancedStyling.BOLD_UNDERLINE
    "\\@since 0.3.26rc2. Text becomes bold and underlined"
    BOLD_STRIKE = _ColorAdvancedStyling.BOLD_STRIKE
    "\\@since 0.3.26rc2. Text becomes bold and crossed out"
    BOLD_OVERLINE = _ColorAdvancedStyling.BOLD_OVERLINE
    "\\@since 0.3.26rc2. Text becomes bold and overlined"
    ITALIC_UNDERLINE = _ColorAdvancedStyling.ITALIC_UNDERLINE
    "\\@since 0.3.26rc2. Text becomes oblique and underlined"
    ITALIC_STRIKE = _ColorAdvancedStyling.ITALIC_STRIKE
    "\\@since 0.3.26rc2. Text becomes oblique and crossed out"
    ITALIC_OVERLINE = _ColorAdvancedStyling.ITALIC_OVERLINE
    "\\@since 0.3.26rc2. Text becomes oblique and overlined"
    UNDERLINE_STRIKE = _ColorAdvancedStyling.UNDERLINE_STRIKE
    "\\@since 0.3.26rc2. Text becomes underlined and crossed out"
    UOLINE = _ColorAdvancedStyling.UOLINE
    "\\@since 0.3.26rc2. Alias to underline-overline. Text gets lines above and below"
    STRIKE_OVERLINE = _ColorAdvancedStyling.STRIKE_OVERLINE
    "\\@since 0.3.26rc2. Text becomes crossed out and overlined"
    # 3x
    BOLD_ITALIC_UNDERLINE = _ColorAdvancedStyling.BOLD_ITALIC_UNDERLINE
    "\\@since 0.3.26rc2. Text becomes bold, oblique and underlined"
    BOLD_ITALIC_STRIKE = _ColorAdvancedStyling.BOLD_ITALIC_STRIKE
    "\\@since 0.3.26rc2"
    BOLD_ITALIC_OVERLINE = _ColorAdvancedStyling.BOLD_ITALIC_OVERLINE
    "\\@since 0.3.26rc2"
    BOLD_UNDERLINE_STRIKE = _ColorAdvancedStyling.BOLD_UNDERLINE_STRIKE
    "\\@since 0.3.26rc2"
    BOLD_UOLINE = _ColorAdvancedStyling.BOLD_UOLINE
    "\\@since 0.3.26rc2"
    ITALIC_UNDERLINE_STRIKE = _ColorAdvancedStyling.ITALIC_UNDERLINE_STRIKE
    "\\@since 0.3.26rc2"
    ITALIC_UOLINE = _ColorAdvancedStyling.ITALIC_UOLINE
    "\\@since 0.3.26rc2"
    ITALIC_STRIKE_OVERLINE = _ColorAdvancedStyling.ITALIC_STRIKE_OVERLINE
    "\\@since 0.3.26rc2"
    STRIKE_UOLINE = _ColorAdvancedStyling.STRIKE_UOLINE
    "\\@since 0.3.26rc2"
    
    def __isHex(self, target: str):
        _t = target
        HEX = "0123456789abcdef"
        
        if target.startswith(("0x", "#")):
            _t = self.__re.sub(r"^(0x|#)", "", _t)
        
        for c in target:
            if c not in HEX:
                return False
        return True
    
    def __isDec(self, target: str):
        DEC = "0123456789"
        
        for c in target:
            if c not in DEC:
                return False
        return True
    
    def __isOct(self, target: str):
        _t = target
        OCT = "01234567"
        
        if target.startswith("0o"):
            _t = self.__re.sub(r"^0o", "", _t)
        
        for c in target:
            if c not in OCT:
                return False
        return True
    
    def __isBin(self, target: str):
        _t = target
        BIN = "01"
        
        if target.startswith("0b"):
            _t = self.__re.sub(r"^0b", "", _t)
        
        for c in target:
            if c not in BIN:
                return False
        return True
    
    def __pre_convert(self, target: str):
        
        if self.__isHex(target):
            return int(target, 16)
        
        elif self.__isDec(target):
            return int(target, 10)
        
        elif self.__isOct(target):
            return int(target, 8)
        
        elif self.__isBin(target):
            return int(target, 2)
        
        else:
            return int(target)
        
    def __prepare_return(self):
        
        _s = "\033["
        # for e in (self.__fg, self.__bg, self.__un): ### removed 0.3.27
        _err = ValueError("Interal error. For 3-bit colors, expected integer or string value in range 0-7. One of foreground or background values doesn't match this requirement")
        for e in (self.__fg, self.__bg):
            
            if e is not None:
                if self.__bits == 3 and e not in abroad(0x8):
                    raise _err
                
                elif self.__bits == 4 and e not in abroad(0x10):
                    raise _err
                
                elif self.__bits == 8 and e not in abroad(0x100):
                    raise _err
                
                elif self.__bits == 24 and e not in abroad(0x1000000):
                    raise _err
        
        if self.__bits == 3:
            # 2 ** 3 = 8 (0x8 in hex)
            _s += str(30 + self.__fg) + ";" if self.__fg is not None else ""
            _s += str(40 + self.__bg) + ";" if self.__bg is not None else ""
            # _s += "58;5;" + str(self.__un) + ";" if self.__un is not None else "" ### removed 0.3.27
        
        elif self.__bits == 4:
            # 2 ** 4 = 16 (0x10 in hex); WARNING: bright colors notation isn't official
            _s += str(30 + self.__fg) + ";" if self.__fg is not None and self.__fg in abroad(0x8) else ""
            _s += str(40 + self.__bg) + ";" if self.__bg is not None and self.__bg in abroad(0x8) else ""
            _s += str(90 + self.__fg) + ";" if self.__fg is not None and self.__fg in abroad(0x8, 0x10) else ""
            _s += str(100 + self.__bg) + ";" if self.__bg is not None and self.__bg in abroad(0x8, 0x10) else ""
            # _s += "58;5;" + str(self.__un) + ";" if self.__un is not None else "" ### removed 0.3.27
        
        elif self.__bits == 8:
            # 2 ** 8 = 256 (0x100 in hex)
            _s += "38;5;" + str(self.__fg) + ";" if self.__fg is not None else ""
            _s += "48;5;" + str(self.__bg) + ";" if self.__bg is not None else ""
            # _s += "58;5;" + str(self.__un) + ";" if self.__un is not None else "" ### removed 0.3.27
        
        elif self.__bits == 24:
            # 2 ** 24 = 16777216 (0x1000000 in hex)
            # code reconstructed on 0.3.26rc2
            # acknowledgements: equivalent to rgb
            _f = hex(self.__fg) if self.__fg is not None else ""
            _b = hex(self.__bg) if self.__bg is not None else ""
            # _u = hex(self.__un) if self.__un is not None else "" ### removed 0.3.27
            _f = self.__re.sub(r"^(0x|#)", "", _f) if reckon(_f) > 0 else ""
            _b = self.__re.sub(r"^(0x|#)", "", _b) if reckon(_b) > 0 else ""
            # _u = self.__re.sub(r"^(0x|#)", "", _u) if reckon(_u) > 0 else "" ### removed 0.3.27
            # _hf, _hb, _hu = [None for _ in abroad(3)] ### removed 0.3.27
            _hf, _hb = [None, None]
            # for s in (_f, _b, _u): ### removed 0.3.27
            for s in (_f, _b):
                
                if reckon(s) == 6:
                    if s == _f:
                        _hf = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    else:
                        _hb = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    # else:
                    #    _hu = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2)) ### removed 0.3.27
                    
                elif reckon(s) == 5:
                    s = "0" + s
                    if s == "0" + _f:
                        _hf = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    else:
                        _hb = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    # else:
                    #    _hu = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    
                elif reckon(s) == 4:
                    s = "00" + s
                    if s == "00" + _f:
                        _hf = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    else:
                        _hb = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    # else:
                    #    _hu = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2)) ### removed 0.3.27
                    
                elif reckon(s) == 3:
                    _tmp = "".join(s[i] * 2 for i in abroad(s)) # aliased according to css hex fff notation
                    if s == _f:
                        s = _tmp
                        _hf = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    else:
                        s = _tmp
                        _hb = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    # else:
                    #    s = _tmp
                    #    _hu = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2)) ### removed 0.3.27
                    
                elif reckon(s) == 2:
                    s = "0000" + s
                    if s == "0000" + _f:
                        _hf = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    else:
                        _hb = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    # else:
                    #    _hu = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2)) ### removed 0.3.27
                    
                elif reckon(s) == 1:
                    s = "00000" + s
                    if s == "00000" + _f:
                        _hf = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    else:
                        _hb = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2))
                    # else:
                    #    _hu = tuple(int(s[i : i + 2], 16) for i in abroad(0, 5, 2)) ### removed 0.3.27
            
            _s += "38;2;" + str(_hf[0]) + ";" + str(_hf[1]) + ";" + str(_hf[2]) + ";" if _hf is not None else ""
            _s += "48;2;" + str(_hb[0]) + ";" + str(_hb[1]) + ";" + str(_hb[2]) + ";" if _hb is not None else ""
            # _s += "58;2;" + str(_hu[0]) + ";" + str(_hu[1]) + ";" + str(_hu[2]) + ";" if _hu is not None else "" ### removed 0.3.27
        else:
            error = ValueError(f"Internal 'bits' variable value is not one from following: 3, 4, 8, 24")
            raise error
        if _s != "\033[":
            _s = self.__re.sub(r";$", "m", _s)
            _s += self.__text + "\033[0m"
        else:
            _s = self.__text
        return _s
    
    if True: # since 0.3.27
        def __init__(self, text: str, /, bits: _Bits = 8, foregroundColor: _Color = None, backgroundColor: _Color = None): # slash since 0.3.26rc2
            """
            \\@since 0.3.26rc1. Parameters:
            - `text` - string to be colored. Required parameter
            - `bits` - number of bits, possible values: 3, 4, 8, 24. Defaults to 24 (since 0.3.26rc2 - 8)
            - `foregroundColor` - color of the foreground (text). String/integer/`None`. Defaults to `None`
            - `backgroundColor` - color of the background. String/integer/`None`. Defaults to `None`
            
            See https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit for color palette outside 24-bit colors
            """
            self.__os.system("color")
            
            if not Tense.isString(text):
                error = TypeError("Expected string value for 'text' parameter")
                raise error
            
            if not Tense.isInteger(bits) or (Tense.isInteger(bits) and bits not in (3, 4, 8, 24)):
                error = TypeError("Expected integer value: 3, 4, 8 or 24, for 'bits' parameter")
                raise error
            
            for e in (foregroundColor, backgroundColor):
                
                if not Tense.isInteger(e) and not Tense.isString(e) and not isinstance(e, RGB) and e is not None:
                    error = TypeError(f"Expected integer, string or 'None' value for '{e.__name__}' parameter")
                    raise error
                
                elif Tense.isString(e) and (
                    not self.__isHex(e) and
                    not self.__isDec(e) and
                    not self.__isOct(e) and
                    not self.__isBin(e)
                ):
                    error = TypeError(f"Malformed string in parameter 'e', expected clean binary, decimal, hexademical or octal string")
                    raise error
                
                elif bits == 24 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x1000000) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x1000000) or
                    isinstance(e, RGB) and int(e) not in abroad(0x1000000)
                ):
                    error = ValueError(f"For 24-bit colors, expected \"RGB\" class instance of integer value, integer or string value in range 0-16777215")
                    raise error
                
                elif bits == 8 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x100) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x100) or isinstance(e, RGB)
                ):
                    error = ValueError(f"For 8-bit colors, expected integer or string value in range 0-255. Cannot be used with \"RGB\" class instance")
                    raise error
                
                elif bits == 4 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x10) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x10) or isinstance(e, RGB)
                ):
                    error = ValueError(f"For 4-bit colors, expected integer or string value in range 0-15. Cannot be used with \"RGB\" class instance")
                    raise error
                
                elif bits == 3 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x8) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x8) or isinstance(e, RGB)
                ):
                    error = ValueError(f"For 3-bit colors, expected integer or string value in range 0-7. Cannot be used with \"RGB\" class instance")
                    raise error
            
            self.__text = text
            self.__bits = bits
            self.__fg = foregroundColor if Tense.isInteger(foregroundColor) else self.__pre_convert(foregroundColor) if Tense.isString(foregroundColor) else int(foregroundColor) if isinstance(foregroundColor, RGB) else None
            self.__bg = backgroundColor if Tense.isInteger(backgroundColor) else self.__pre_convert(backgroundColor) if Tense.isString(backgroundColor) else int(backgroundColor) if isinstance(backgroundColor, RGB) else None
            
    else:
        def __init__(self, text: str, /, bits: _Bits = 8, foregroundColor: _Color = None, backgroundColor: _Color = None, underlineColor: _Color = None):
            
            self.__os.system("color")
            
            if not Tense.isString(text):
                error = TypeError("Expected string value for 'text' parameter")
                raise error
            
            if not Tense.isInteger(bits) or (Tense.isInteger(bits) and bits not in (3, 4, 8, 24)):
                error = TypeError("Expected integer value: 3, 4, 8 or 24, for 'bits' parameter")
                raise error
            
            for e in (foregroundColor, backgroundColor, underlineColor):
                
                if not Tense.isInteger(e) and not Tense.isString(e) and e is not None:
                    error = TypeError(f"Expected integer, string or 'None' value for '{e.__name__}' parameter")
                    raise error
                
                elif Tense.isString(e) and (
                    not self.__isHex(e) and
                    not self.__isDec(e) and
                    not self.__isOct(e) and
                    not self.__isBin(e)
                ):
                    error = TypeError(f"Malformed string in parameter 'e', expected clean binary, decimal, hexademical or octal string")
                    raise error
                
                elif bits == 24 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x1000000) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x1000000)
                ):
                    error = ValueError(f"For 24-bit colors, expected integer or string value in range 0-16777215")
                    raise error
                
                elif bits == 8 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x100) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x100)
                ):
                    error = ValueError(f"For 8-bit colors, expected integer or string value in range 0-255")
                    raise error
                
                elif bits == 4 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x10) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x10)
                ):
                    error = ValueError(f"For 4-bit colors, expected integer or string value in range 0-15")
                    raise error
                
                elif bits == 3 and e is not None and (
                    Tense.isInteger(e) and e not in abroad(0x8) or
                    Tense.isString(e) and self.__pre_convert(e) not in abroad(0x8)
                ):
                    error = ValueError(f"For 3-bit colors, expected integer or string value in range 0-7")
                    raise error
                
            self.__text = text
            self.__bits = bits
            self.__fg = foregroundColor if Tense.isInteger(foregroundColor) else self.__pre_convert(foregroundColor) if Tense.isString(foregroundColor) else None
            self.__bg = backgroundColor if Tense.isInteger(backgroundColor) else self.__pre_convert(backgroundColor) if Tense.isString(backgroundColor) else None
            self.__un = underlineColor if Tense.isInteger(underlineColor) else self.__pre_convert(underlineColor) if Tense.isString(underlineColor) else None
    
    def clear(self):
        """
        \\@since 0.3.26rc1
        
        Clear every color for foreground, background and underline. Should \\
        be used before `setBits()` method invocation to avoid conflicts. \\
        By default bits value is reset to 24. Since 0.3.27b1 - 8.
        """
        self.__fg = None
        self.__bg = None
        if False: # 0.3.27
            self.__un = None
        self.__bits = 8
        return self
    
    def setBits(self, bits: _Bits = 8, /):
        """
        \\@since 0.3.26rc1

        Possible values: 3, 4, 8, 24. Default is 24. \\
        Since 0.3.26rc2 default value is 8.
        """
        
        if not Tense.isInteger(bits) or (Tense.isInteger(bits) and bits not in (3, 4, 8, 24)):
            error = TypeError("Expected integer value: 3, 4, 8 or 24, for 'bits' parameter")
            raise error
        
        # for e in (self.__fg, self.__bg, self.__un): ### removed 0.3.27
        for e in (self.__fg, self.__bg):
            
            if e is not None:
                
                if bits == 24 and e not in abroad(0x1000000):
                    error = ValueError("Internal conflict caught while setting 'bits' value to 24. One of foreground or background values is beyond range 0-16777215. To prevent this conflict, use method 'Color.clear()'.")
                    raise error
                
                elif bits == 8 and e not in abroad(0x100):
                    error = ValueError("Internal conflict caught while setting 'bits' value to 8. One of foreground or background values is beyond range 0-255. To prevent this conflict, use method 'Color.clear()'.")
                    raise error
                
                elif bits == 4 and e not in abroad(0x10):
                    error = ValueError("Internal conflict caught while setting 'bits' value to 4. One of foreground or background values is beyond range 0-15. To prevent this conflict, use method 'Color.clear()'.")
                    raise error
                
                elif bits == 3 and e not in abroad(0x8):
                    error = ValueError("Internal conflict caught while setting 'bits' value to 3. One of foreground or background values is beyond range 0-7. To prevent this conflict, use method 'Color.clear()'.")
                    raise error
                
        self.__bits = bits
    
    def setForegroundColor(self, color: _Color = None, /):
        """
        \\@since 0.3.26rc1
        
        Set foreground color manually.
        """
        _c = color if Tense.isInteger(color) or color is None else self.__pre_convert(color) if Tense.isString(color) else int(color) if isinstance(color, RGB) else None
        
        if _c is not None:
            
            if self.__bits == 3 and _c not in abroad(0x8):
                error = ValueError(f"For 3-bit colors, expected integer or string value in range 0-7")
                raise error
            
            elif self.__bits == 4 and _c not in abroad(0x10):
                error = ValueError(f"For 4-bit colors, expected integer or string value in range 0-15")
                raise error
            
            elif self.__bits == 8 and _c not in abroad(0x100):
                error = ValueError(f"For 8-bit colors, expected integer or string value in range 0-255")
                raise error
            
            elif self.__bits == 24 and _c not in abroad(0x1000000):
                error = ValueError(f"For 24-bit colors, expected integer or string value in range 0-16777215")
                raise error
            
            else:
                error = ValueError(f"Internal 'bits' variable value is not one from following: 3, 4, 8, 24")
                raise error
            
        self.__fg = _c
        return self
    
    def setBackgroundColor(self, color: _Color = None, /):
        """
        \\@since 0.3.26rc1
        
        Set background color manually.
        """
        _c = color if Tense.isInteger(color) or color is None else self.__pre_convert(color) if Tense.isString(color) else int(color) if isinstance(color, RGB) else None
        
        if _c is not None:
            
            if self.__bits == 3 and _c not in abroad(0x8):
                error = ValueError(f"For 3-bit colors, expected integer or string value in range 0-7")
                raise error
            
            elif self.__bits == 4 and _c not in abroad(0x10):
                error = ValueError(f"For 4-bit colors, expected integer or string value in range 0-15")
                raise error
            
            elif self.__bits == 8 and _c not in abroad(0x100):
                error = ValueError(f"For 8-bit colors, expected integer or string value in range 0-255")
                raise error
            
            elif self.__bits == 24 and _c not in abroad(0x1000000):
                error = ValueError(f"For 24-bit colors, expected integer or string value in range 0-16777215")
                raise error
            
            else:
                error = ValueError(f"Internal 'bits' variable value is not one from following: 3, 4, 8, 24")
                raise error
            
        self.__bg = _c
        return self
    
    if False:
        def setUnderlineColor(self, color: _Color = None, /):
            """
            \\@since 0.3.26rc1
            
            Set underline color manually. *Experimental* \\
            Since 0.3.26rc2 only accepted value is `None`.
            """
            _c = color if Tense.isInteger(color) or color is None else self.__pre_convert(color)
            if _c is not None:
                if self.__bits == 3 and _c not in abroad(0x8):
                    error = ValueError(f"For 3-bit colors, expected integer or string value in range 0-7")
                    raise error
                
                elif self.__bits == 4 and _c not in abroad(0x10):
                    error = ValueError(f"For 4-bit colors, expected integer or string value in range 0-15")
                    raise error
                
                elif self.__bits == 8 and _c not in abroad(0x100):
                    error = ValueError(f"For 8-bit colors, expected integer or string value in range 0-255")
                    raise error
                
                elif self.__bits == 24 and _c not in abroad(0x1000000):
                    error = ValueError(f"For 24-bit colors, expected integer or string value in range 0-16777215")
                    raise error
                
                else:
                    error = ValueError(f"Internal 'bits' variable value is not one from following: 3, 4, 8, 24")
                    raise error
                
            self.__un = _c
            return self
    
    def __pos__(self):
        """\\@since 0.3.26rc1. Receive colored string"""
        return self.__prepare_return()
    
    def __neg__(self):
        """\\@since 0.3.26rc1. Receive colored string"""
        return self.__prepare_return()
    
    def __invert__(self):
        """\\@since 0.3.26rc1. Receive colored string"""
        return self.__prepare_return()
    
    def __mod__(self, other: _ColorStylingType):
        """
        \\@since 0.3.26rc1
        
        Further styling. Use constant, which is in `__constants__` attribute.
        """
        # below: since 0.3.26rc1
        if other == self.NORMAL:
            return self.__prepare_return()
        
        elif other == self.BOLD:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;", self.__prepare_return())
        
        elif other == self.FAINT:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[2;", self.__prepare_return())
        
        elif other == self.ITALIC:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;", self.__prepare_return())
        
        elif other == self.UNDERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[4;", self.__prepare_return())
        
        elif other == self.SLOW_BLINK:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[5;", self.__prepare_return())
        
        elif other == self.RAPID_BLINK:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[6;", self.__prepare_return())
        
        # below: since 0.3.26rc2
        elif other == self.REVERSE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[7;", self.__prepare_return())
        
        # below: since 0.3.26rc1
        elif other == self.HIDE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[8;", self.__prepare_return())
        
        elif other == self.STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[9;", self.__prepare_return())
        
        elif other == self.DOUBLE_UNDERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[21;", self.__prepare_return())
        
        # elif other == self.PROPORTIONAL:
        #    return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[26;", self.__prepare_return())
        
        elif other == self.FRAME:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[51;", self.__prepare_return())
        
        elif other == self.ENCIRCLE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[52;", self.__prepare_return())
        
        elif other == self.OVERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[53;", self.__prepare_return())
        
        # below: since 0.3.26rc2
        elif other == self.SUPERSCRIPT:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[73;", self.__prepare_return())
        
        elif other == self.SUBSCRIPT:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[74;", self.__prepare_return())
        # 2x; since 0.3.26rc2
        elif other == self.BOLD_ITALIC:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;3;", self.__prepare_return())
        
        elif other == self.BOLD_UNDERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;4;", self.__prepare_return())
        
        elif other == self.BOLD_STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;9;", self.__prepare_return())
        
        elif other == self.BOLD_OVERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;53;", self.__prepare_return())
        
        elif other == self.ITALIC_UNDERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;4;", self.__prepare_return())
        
        elif other == self.ITALIC_STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;9;", self.__prepare_return())
        
        elif other == self.ITALIC_OVERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;53;", self.__prepare_return())
        
        elif other == self.UNDERLINE_STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[4;9;", self.__prepare_return())
        
        elif other == self.UOLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[4;53;", self.__prepare_return())
        
        elif other == self.STRIKE_OVERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[9;53;", self.__prepare_return())
        
        # 3x; since 0.3.26rc2
        elif other == self.BOLD_ITALIC_UNDERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;3;4;", self.__prepare_return())
        
        elif other == self.BOLD_ITALIC_STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;3;9;", self.__prepare_return())
        
        elif other == self.BOLD_ITALIC_OVERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;3;53;", self.__prepare_return())
        
        elif other == self.BOLD_UNDERLINE_STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;4;9;", self.__prepare_return())
        
        elif other == self.BOLD_UOLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[1;4;53;", self.__prepare_return())
        
        elif other == self.ITALIC_UNDERLINE_STRIKE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;4;9;", self.__prepare_return())
        
        elif other == self.ITALIC_UOLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;4;53;", self.__prepare_return())
        
        elif other == self.ITALIC_STRIKE_OVERLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[3;9;53;", self.__prepare_return())
        
        elif other == self.STRIKE_UOLINE:
            return self.__re.sub(r"^(\033\[|\u001b\[)", "\033[4;9;53;", self.__prepare_return())
        
        else:
            # replace error due to enumerator type change (0.3.27)
            if True:
                error = TypeError("expected one from following constant values: " + repr(self.__constants__))
            else:
                error = (TypeError,
                    "Expected any from constant values: " + repr(self.__constants__) + ". You are discouraged to do common operations on these constants, like union as in case of regular expression flags, to satisfy this requirement, because it "
                    "won't warrant that returned string will be styled as thought"
                )
            raise error
    __dir__ = [n for n in locals() if n[:1] != "_"]
    "\\@since 0.3.26rc2"
    __all__ = [n for n in locals() if n[:1] != "_"]
    "\\@since 0.3.26rc2. Returns list of all non-underscore-preceded members of class `tense.Color`"
    __constants__ = [n for n in locals() if n[:1] != "_" and n.isupper()]
    
    """
    \\@since 0.3.26rc2

    Returns list of constants. These can be used as right operand for `%` operator. \\
    They are sorted as in ANSI escape code table, in ascending order
    """

if __name__ == "__main__":
    error = (RuntimeError, "This file is not for compiling, consider importing it instead. Notice it is 'tense' module, but it should be treated as a module to import-only")
    raise error

del deque, tc, time, warnings, tp, ty # Not for export

__all__ = sorted([n for n in globals() if n[:1] != "_"])
__dir__ = __all__

__author__ = "Aveyzan <aveyzan@gmail.com>"
"\\@since 0.3.26rc3"
__license__ = "MIT"
"\\@since 0.3.26rc3"
__version__ = Tense.version
"\\@since 0.3.26rc3"