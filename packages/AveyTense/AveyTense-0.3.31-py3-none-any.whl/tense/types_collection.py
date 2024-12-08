"""
**Tense Types Collection**

\\@since 0.3.26b3 \\
© 2023-Present Aveyzan // License: MIT \\
https://aveyzan.glitch.me/tense/py/module.types_collection.html
```ts
module tense.types_collection
```
Types package for TensePy. It also contains ABCs (Abstract Base Classes) and exception classes. To 0.3.26rc3 `tense.tcs`. \\
Constants have been moved to separate submodule `tense.constants`.

Despite Python e.g. in version 3.10 provides union type expression with bar (`|`), in version 3.12 - preceding `type` keyword notations \\
still it is recommended to write the code in accordance to older Python versions.

If downloading `typing_extensions` module went unsuccessfully, try to manually run `pip install typing_extensions`.
"""
from __future__ import annotations
import sys

from ._primal_types import *
from ._abc import *
from ._exceptions import ErrorHandler as _E
from .constants import VERSION
import os, tkinter as tk, types as ty, io, math as ma, collections as ct, warnings as wa, functools as fn, abc, collections.abc as abc2, asyncio as aio, subprocess as sb, enum, inspect as ins
import zipfile as zi, urllib as url, hashlib as hl, dis, ast, typing as tp
from mmap import mmap
from array import array
from copy import copy

try:
    import typing_extensions as tpe # type: ignore
except (ModuleNotFoundError, ImportError, NameError):
    sb.run([sys.executable, "-m", "pip", "install", "typing_extensions"])

import typing_extensions as tpe # type: ignore

NULL = None # 0.3.26b3


###### TYPES ######

_var = TypeVar
_uni = Union
_opt = Optional
_cal = Callable
_par = ParamSpec
_any = Any
_pro = Protocol
_lit = Literal

_T = _var("_T")
_P = _par("_P")
_T_class = _var("_T_class", bound = type)
_T_func = _var("_T_func", bound = _cal[..., Any])
_T_sb = _var("_T_bs", bytes, str)
_T_cov = _var("_T_cov", covariant = True)
_T_con = _var("_T_con", contravariant = True)
_KT = _var("_KT")
_KT_cov = _var("_KT_cov", covariant = True)
_KT_con = _var("_KT_con", contravariant = True)
_VT = _var("_VT")
_VT_cov = _var("_VT_cov", covariant = True)
_CoroutineLike = _cal[_P, Generator[_any, _any, _T]]
# >>> _uni[_cal[_P, tp.Generator[_any, _any, _T]], _cal[..., _T]]
_DecoratorLike = _cal[_P, _T]
# abroad types basing on parameter names
_V1 = _var("_V1")
_V2 = _var("_V2")
_M = _var("_M")

###### ABCs OUTSIDE collections.abc ######
# Most of them are also undefined in _typeshed module, which is uncertain module to import at all.

@runtime
class NotReassignable(_pro[_T_con]):
    """
    \\@since 0.3.26b3

    This class does not support any form of re-assignment, those are augmented \\
    assignment operators: `+=`, `-=`, `*=`, `**=`, `/=`, `//=`, `%=`, `>>=`, `<<=`, \\
    `&=`, `|=`, `^=`. Setting new value also is prohibited.
    """
    __slots__ = ("__weakref__",)
    __op = (
        "; used operator '+='", # 0
        "; used operator '-='", # 1
        "; used operator '*='", # 2
        "; used operator '/='", # 3
        "; used operator '//='", # 4
        "; used operator '**='", # 5
        "; used operator '<<='", # 6
        "; used operator '>>='", # 7
        "; used operator '%='", # 8
        "; used operator '&='", # 9
        "; used operator '|='", # 10
        "; used operator '^='", # 11
    )
    def __set__(self, i: tp.Self, v: _T_con):
        # setting value not allowed...
        if self.__class__.__name__ == "FinalVar":
            s = " final variable"
            _E(100, s)
        else:
            s = " variable that isn't assignable and re-assignable"
            _E(102, s)
    def __iadd__(self, o: _T_con):
        i = 0
        _E(102, self.__op[i])
    def __isub__(self, o: _T_con):
        i = 1
        _E(102, self.__op[i])
    def __imul__(self, o: _T_con):
        i = 2
        _E(102, self.__op[i])
    def __ifloordiv__(self, o: _T_con):
        i = 4
        _E(102, self.__op[i])
    def __idiv__(self, o: _T_con):
        i = 3
        _E(102, self.__op[i])
    def __itruediv__(self, o: _T_con):
        i = 3
        _E(102, self.__op[i])
    def __imod__(self, o: _T_con):
        i = 8
        _E(102, self.__op[i])
    def __ipow__(self, o: _T_con):
        i = 5
        _E(102, self.__op[i])
    def __ilshift__(self, o: _T_con):
        i = 6
        _E(102, self.__op[i])
    def __irshift__(self, o: _T_con):
        i = 7
        _E(102, self.__op[i])
    def __iand__(self, o: _T_con):
        i = 9
        _E(102, self.__op[i])
    def __ior__(self, o: _T_con):
        i = 10
        _E(102, self.__op[i])
    def __ixor__(self, o: _T_con):
        i = 11
        _E(102, self.__op[i])

@runtime
class NotComparable(_pro[_T_con]):
    """
    \\@since 0.3.26b3

    Cannot be compared with operators `==`, `!=`, `>`, `<`, `>=`, `<=`, `in`
    """
    __slots__ = ()
    __op = (
        "; used operator '<'", # 0
        "; used operator '>'", # 1
        "; used operator '<='", # 2
        "; used operator '>='", # 3
        "; used operator '=='", # 4
        "; used operator '!='", # 5
        "; used operator 'in'", # 6
    )
    def __await_internal_sentinel(self, val = ""):
        _E(101, val)
    def __lt__(self, other: _T_con):
        i = 0
        _E(102, self.__op[i])
    def __gt__(self, other: _T_con):
        i = 1
        _E(102, self.__op[i])
    def __le__(self, other: _T_con):
        i = 2
        _E(102, self.__op[i])
    def __ge__(self, other: _T_con):
        i = 3
        _E(102, self.__op[i])
    def __eq__(self, other: _T_con):
        i = 4
        _E(102, self.__op[i])
    def __ne__(self, other: _T_con):
        i = 5
        _E(102, self.__op[i])
    def __contains__(self, other: _T_con):
        i = 6
        _E(102, self.__op[i])

if sys.version_info >= (3, 13):
    from warnings import deprecated as _depr
else:
    _depr = tpe.deprecated

deprecated = _depr
"\\@since 0.3.26"
Deprecated = deprecated
"\\@since 0.3.26b3. Alias *tense.types_collection.Deprecated*"

""""""
# class Deprecated:
#    """
#    \\@since 0.3.26b3 (experimental) (alias since 0.3.26)
#
#    This class marks a class as deprecated. Every keyword parameter accord to \\
#    the ones `warnings.warn()` method has. Instead of `skip_file_prefixes` you \\
#    can also use `skipFilePrefixes` and instead of `stacklevel` - `stackLevel`. \\
#    Excluded is only `category` parameter, which has value `DeprecationWarning`.
#
#    Parameters: `message`, `stacklevel`, `source`, `skip_file_prefixes`, as in:
#    ```py \\
#    class IAmDeprecatedClass(Deprecated, message = ..., stacklevel = ..., ...)
#    ```
#    """
    # def __init_subclass__(cls, /, *args, **kwds):
    #     wa.simplefilter("always", DeprecationWarning)
    #     wa.warn(
    #         str(kwds["message"]) if "message" in kwds else "Deprecated class.",
    #         DeprecationWarning,
    #         int(kwds["stacklevel"]) if "stacklevel" in kwds else 2,
    #         kwds["source"] if "source" in kwds else None,
    #         skip_file_prefixes = kwds["skipFilePrefixes"] if "skipFilePrefixes" in kwds else kwds["skip_file_prefixes"] if "skip_file_prefixes" in kwds else ()
    #     )
    #    wa.simplefilter("default", DeprecationWarning)

@runtime
class NotIterable(_pro):
    """
    \\@since 0.3.26b3

    Cannot be used with `for` loop
    """
    # usage as in typing module (0.3.26c3)
    __iter__ = None

@runtime
class NotInvocable(_pro[_T_cov]):
    """
    \\@since 0.3.26rc1

    Cannot be called as a function (as `self()`)
    """
    def __call__(self, *args, **kwds):
        _E(107)

@runtime
class NotUnaryOperable(_pro):
    """
    \\@since 0.3.26rc1

    Cannot be used with preceding operators `+`, `-` and `~`
    """
    ...
    def __pos__(self):
        _E(108)
    def __neg__(self):
        _E(108)
    def __invert__(self):
        _E(108)

# @runtime
# class AbroadOperable(_pro[_T_cov]):
    """
    \\@since 0.3.26c2?

    An ABC with one method `__abroad__`.

    This magic method is used for `abroad()` function
    """
    # def __abroad__(self) -> _T_cov: ...

@final
class ClassLike(Generic[_P, _T]):
    """
    \\@since 0.3.27a3
    
    A class decorator for functions, transforming them to declarations \\
    similar to classes. Example::
    
        @ClassLike
        def test():
            return 42

        a = test() # returns 42

    """
    def __init__(self, f: _cal[_P, _T]):
        self.f = f
    def __call__(self, *args: _P.args, **kwds: _P.kwargs):
        return self.f(*args, **kwds)
    
classlike = ClassLike # since 0.3.27a3

class FinalVar(NotReassignable[_T], NotIterable, Comparable, UnaryOperable): # 0.3.26b3
    """
    \\@since 0.3.26b3 \\
    https://aveyzan.glitch.me/tense/py/module.types_collection.html#FinalVar

    Indicates a name should be final, and may not be re-assigned. In this case, names \\
    marked with `tense.types_collection.FinalVar` are treated as *immutable*, \\
    as constants.
    ```py \\
    reassign_me = 96000 # ok
    reassign_me += 3 # ok; gets value 96003
    reassign_me = FinalVar(96000) # ok
    reassign_me += 3 # error
    ```
    To receive value, use one of following:
    ```py \\
    f = FinalVar(69)
    Tense.print(+f) # 69
    Tense.print(-f) # 69
    Tense.print(~f) # 69
    Tense.print(f()) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f[0]) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f | 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f & 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f ^ 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f + 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f - 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f ** 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f << 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(f >> 0) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(abs(f)) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    Tense.print(math.trunc(f)) # 69, deprecated since 0.3.26rc1, removed on 0.3.27a3
    ```
    This class itself is final and cannot be subclassed (since 0.3.26rc1). On 0.3.27rc1 \\
    actually returned inheritance possibility.
    """
    __var: _T = None
    __slots__ = ()
    def __e(self, code = 1):
        if code == 1:
            _E(105, self.__class__.__qualname__)
        elif code == 2:
            _E(112)
        elif code == 3:
            _E(106)
        else:
            _E(100)

    def __init__(self, v: _T, /):
        # patched issue: self.__class__ instead of self
        # if not that, None will be always deduced
        self.__class__.__var = v

    # subclassing is projected; for now use enum.Enum
    def __init_subclass__(cls):
        
        # all augmented assignment methods
        reassignment = {
            "__iadd__": "+=",
            "__isub__": "-=",
            "__imul__": "*=",
            "__itruediv__": "/=",
            "__ifloordiv__": "//=",
            "__imod__": "",
            "__imatmul__": "@=",
            "__iand__": "&=",
            "__ior__": "|=",
            "__ixor__": "^=",
            "__ilshift__": "<<=",
            "__irshift__": ">>=",
            "__ipow__": "**="
        }
        
        # no reassignment; must return callback so assigned attributes can be methods
        def _no_re(op: str): 
            def _no_re_internal(self: pt.Self, other: _T):
                _o = " with operator " + op
                _E(102, _o)
            return _no_re_internal
        
        for key in reassignment:
            exec("cls.{} = _no_re(\"{}\")".format(key, reassignment[key])) # f-strings since python 3.6
        
        cls = frozen(cls)
        if False:
            _E(113, cls.__name__) # 0.3.27rc1 - skipped return statement because __init prefixed methods cannot return anything
    
    def __subclasscheck__(self, s: type):
        if True: # toggled on 0.3.27rc2
            return issubclass(s, type(self))
        s1 = "'FinalVar' class "
        t = "'issubclass()' function"
        _E(114, s1, t)

    def __instancecheck__(self, o: object):
        return isinstance(o, type(self))
    
    def __setattr__(self, name: str, value: sys.Any):
        if name not in self.__class__.__dict__:
            if isinstance(value, type(self)):
                self.__class__.__dict__[name] = value
        else:
            if name in self.__class__.__dict__:
                if isinstance(value, type(self)):
                    self.__e(2)
    
    # same as getattr() builtin
    def __getattr__(self, name: str):
        return getattr(self, name)
    
    @property
    def __mro__(self):
        return None
    
    def __mro_entries__(self):
        return None
    
    def __pos__(self):
        """
        \\@since 0.3.26b3

        Receive value of the final variable. `None` is deduced only in case of an error
        """
        return self.__var
    
    def __neg__(self):
        """
        \\@since 0.3.26b3

        Receive value of the final variable. `None` is deduced only in case of an error
        """
        return self.__var
    
    def __invert__(self):
        """
        \\@since 0.3.26b3

        Receive value of the final variable. `None` is deduced only in case of an error
        """
        return self.__var
    
    def __lt__(self, other: _T):
        """
        \\@since 0.3.26b3

        Comparisons specification
        """
        tmp = True
        if self.__var is None:
            self.__e(1)
        try:
            tmp = bool(self.__var < other)
        except (SyntaxError, TypeError, ValueError):
            self.__e(3)
        return tmp
    
    def __gt__(self, other: _T):
        """
        \\@since 0.3.26b3

        Comparisons specification
        """
        tmp = True
        if self.__var is None:
            self.__e(1)
        try:
            tmp = bool(self.__var > other)
        except (SyntaxError, TypeError, ValueError):
            self.__e(3)
        return tmp
    
    def __le__(self, other: _T):
        """
        \\@since 0.3.26b3

        Comparisons specification
        """
        tmp = True
        if self.__var is None:
            self.__e(1)
        try:
            tmp = bool(self.__var <= other)
        except (SyntaxError, TypeError, ValueError):
            self.__e(3)
        return tmp
    
    def __ge__(self, other: _T):
        """
        \\@since 0.3.26b3

        Comparisons specification
        """
        tmp = True
        if self.__var is None:
            self.__e(1)
        try:
            tmp = bool(self.__var >= other)
        except (SyntaxError, TypeError, ValueError):
            self.__e(3)
        return tmp
    
    def __eq__(self, other: _T):
        """
        \\@since 0.3.26b3

        Comparisons specification
        """
        return self.__var == other
    
    def __ne__(self, other: _T):
        """
        \\@since 0.3.26b3

        Comparisons specification
        """
        return self.__var != other
    
    def __contains__(self, value: _T):
        """
        \\@since 0.3.26rc1

        Determine, whether a value equals the one inside final variable. This manner is \\
        definite exception as in case of iterable objects, which by default use the `in` \\
        keyword.

        In contrast to `==`, expected parameter becomes left operand instead of right.
        """
        return self.__var == value
    
class Allocator:
    """
    \\@since 0.3.27b3

    An allocator class. Classes extending this class have access to `__alloc__` magic method, \\
    but it is advisable to use it wisely.
    """
    __a = bytearray()

    def __init__(self, b: _uni[bytearray, BytearrayConvertible], /):
        if isinstance(b, BytearrayConvertible):
            self.__a = b.__bytearray__()
        elif isinstance(b, bytearray):
            self.__a = b
        else:
            err, s = (TypeError, "Expected a bytearray object or object of class extending 'BytearrayConvertible' class")
            raise err(s)
    
    def __alloc__(self):
        return self.__a.__alloc__()

if False: # cancelled on 0.3.27rc1
    @deprecated("Deprecated since 0.3.27a3, use class 'tense.types_collection.ClassVar' instead.")
    def classvar(v: _T, /):
        """
        \\@since 0.3.26b3 (experimental) \\
        \\@deprecated 0.3.27a3

        Transform variable in a class to a class variable.

        This will be valid only whether this function is \\
        invoked inside a class.
        Use it as:
        ```py \\
        class Example:
            test = classvar(96000) # has value 96000
        ```
        """
        class _t:
            _v: ClassVar[_T] = v
        return _t._v

    @deprecated("Deprecated since 0.3.26c3, use class 'tense.FinalVar' instead.")
    def finalvar(v: _T, /):
        """
        \\@since 0.3.26b3 \\
        \\@deprecated 0.3.26c3 (use `tense.FinalVar` class-like instead)

        Use it as:
        ```py \\
        reassign_me = finalvar(96000) # has value 96000
        reassign_me += 3 # error
        ```
        """
        return FinalVar(v)
    

RichComparable = _uni[LeastComparable[Any], GreaterComparable[Any]]

EnchantedBookQuantity = _lit[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36] # 0.3.26b3
FileType = _uni[str, int, bytes, os.PathLike[str], os.PathLike[bytes]] # 0.3.26b3
FileMode = _lit[
    'r+', '+r', 'rt+', 'r+t', '+rt', 'tr+', 't+r', '+tr', 'w+', '+w', 'wt+', 'w+t', '+wt', 'tw+', 't+w', '+tw', 'a+', '+a', 'at+', 'a+t', '+at', 'ta+', 't+a', '+ta', 'x+', '+x', 'xt+',
    'x+t', '+xt', 'tx+', 't+x', '+tx', 'w', 'wt', 'tw', 'a', 'at', 'ta', 'x', 'xt', 'tx', 'r', 'rt', 'tr', 'U', 'rU', 'Ur', 'rtU', 'rUt', 'Urt', 'trU', 'tUr', 'Utr', 'rb+', 'r+b', '+rb',
    'br+', 'b+r', '+br', 'wb+', 'w+b', '+wb', 'bw+', 'b+w', '+bw', 'ab+', 'a+b', '+ab', 'ba+', 'b+a', '+ba', 'xb+', 'x+b', '+xb', 'bx+', 'b+x', '+bx', 'rb', 'br', 'rbU', 'rUb', 'Urb',
    'brU', 'bUr', 'Ubr', 'wb', 'bw', 'ab', 'ba', 'xb', 'bx'
] # 0.3.26b3
FileOpener = _cal[[str, int], int] # 0.3.26b3
TicTacToeBoard = list[list[str]] # 0.3.26b3
AnySequence = _uni[Sequence[_T], MutableSequence[_T], Uniqual[_T], MutableUniqual[_T]] # 0.3.26c3

SequencePickType = _uni[
    list[_T],
    tuple[_T, ...],
    set[_T],
    frozenset[_T],
    AnySequence[_T],
    ListConvertible[_T]
] # 0.3.26c3

SequencePickNGT = _uni[
    list,
    tuple,
    set,
    frozenset,
    AnySequence,
    ListConvertible
] # 0.3.26c3

ReckonType = _uni[
        # dict[_T], # removed 0.3.27a5 (inherits from MutableMapping)
        # list[_T], # removed 0.3.27a5 (inherits from MutableSequence)
        # tuple[_T, ...], # removed 0.3.27a5 (inherits from Sequence)
        # str, # removed 0.3.27a5 (inherits from Sequence)
        # ct.deque[_T], # removed 0.3.27a5 (inherits from MutableSequence)
        # set[_T], # removed 0.3.27a5 (inherits from MutableSet)
        # bytes, # removed 0.3.27a5 (inherits from Sequence)
        # bytearray, # removed 0.3.27a5 (inherits from MutableSequence)
        # memoryview, # removed 0.3.27a5 (inherits from Sequence)
        # range, # removed 0.3.27a5 (inherits from Sequence)
        # mmap, # removed 0.3.27a5 (inherits from Sized)
        # array[_T], # removed 0.3.27a5 (inherits from MutableSequence)
        # enumerate[_T], # removed 0.3.27a5 (inherits from Iterator -> Iterable)
        # frozenset[_T], # removed 0.3.27a5 (inherits from AbstractSet)
        # ct.Counter[_T], # removed 0.3.27a5 (inherits from dict -> MutableMapping)
        # ct.defaultdict[_T], # removed 0.3.27a5 (inherits from dict -> MutableMapping)
        # io.TextIOWrapper, # removed 0.3.27a5 (inherits from IO)
        ### LOG: since 0.3.24
        # io.FileIO, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedWriter, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedRandom, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedReader, # removed 0.3.27a5 (inherits from IO)
        IO[Any],
        # LOG: since 0.3.25
        # tp.TextIO, # removed 0.3.27a5 (inherits from IO)
        # tp.BinaryIO, # removed 0.3.27a5 (inherits from IO)
        # io.StringIO, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedRWPair, # removed 0.3.27a5 (inherits from IO)
        # tp.Sequence[_T], # removed 0.3.27a5 (inherits from Iterable)
        # tp.MutableSequence[_T], # removed 0.3.27a5 (inherits from Sequence)
        # io.BytesIO, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedIOBase, # removed 0.3.27a5 (unneeded)
        # tp.Mapping[_T, Any], # removed 0.3.27a5 (inherits from Iterable)
        # tp.MutableMapping[_T, Any], # removed 0.3.27a5 (inherits from Mapping)
        # tp.MutableSet[_T], # removed 0.3.27a5 (inherits from AbstractSet)
        # tp.AbstractSet[_T], # removed 0.3.27a5 (inherits from Iterable)
        Iterable[_T], 
        # ct.ChainMap[_T], # removed 0.3.27a5 (inherits from MutableMapping)
        # ct.OrderedDict[_T], # removed 0.3.27a5 (inherits from dict -> MutableMapping)
        ### LOG: 0.3.26b3
        # tp.AsyncIterable[_T], # removed 0.3.27a5 (inherits from Iterable)
        ### LOG: 0.3.26c1
        ReckonOperable,
        tk.StringVar, # remove support on 0.3.36
        # LOG: 0.3.27a5
        Sizeable
]
"""
\\@since 0.3.25 \\
\\@author Aveyzan
```
in module tense.types_collection # to 0.3.26b3 in module tense.types
```
Package of types, which are considered countable and satisfy type requirement \\
for function `reckon()`. To 0.3.26b3 also known as `SupportsCountables`.
"""
ReckonNGT = _uni[
        # dict[_T], # removed 0.3.27a5 (inherits from MutableMapping)
        # list[_T], # removed 0.3.27a5 (inherits from MutableSequence)
        # tuple[_T, ...], # removed 0.3.27a5 (inherits from Sequence)
        # str, # removed 0.3.27a5 (inherits from Sequence)
        # ct.deque[_T], # removed 0.3.27a5 (inherits from MutableSequence)
        # set[_T], # removed 0.3.27a5 (inherits from MutableSet)
        # bytes, # removed 0.3.27a5 (inherits from Sequence)
        # bytearray, # removed 0.3.27a5 (inherits from MutableSequence)
        # memoryview, # removed 0.3.27a5 (inherits from Sequence)
        # range, # removed 0.3.27a5 (inherits from Sequence)
        # mmap, # removed 0.3.27a5 (inherits from Sized)
        # array[_T], # removed 0.3.27a5 (inherits from MutableSequence)
        # enumerate[_T], # removed 0.3.27a5 (inherits from Iterator -> Iterable)
        # frozenset[_T], # removed 0.3.27a5 (inherits from AbstractSet)
        # ct.Counter[_T], # removed 0.3.27a5 (inherits from dict -> MutableMapping)
        # ct.defaultdict[_T], # removed 0.3.27a5 (inherits from dict -> MutableMapping)
        # io.TextIOWrapper, # removed 0.3.27a5 (inherits from IO)
        ### LOG: since 0.3.24
        # io.FileIO, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedWriter, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedRandom, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedReader, # removed 0.3.27a5 (inherits from IO)
        IO,
        # LOG: since 0.3.25
        # tp.TextIO, # removed 0.3.27a5 (inherits from IO)
        # tp.BinaryIO, # removed 0.3.27a5 (inherits from IO)
        # io.StringIO, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedRWPair, # removed 0.3.27a5 (inherits from IO)
        # tp.Sequence[_T], # removed 0.3.27a5 (inherits from Iterable)
        # tp.MutableSequence[_T], # removed 0.3.27a5 (inherits from Sequence)
        # io.BytesIO, # removed 0.3.27a5 (inherits from IO)
        # io.BufferedIOBase, # removed 0.3.27a5 (unneeded)
        # tp.Mapping[_T, Any], # removed 0.3.27a5 (inherits from Iterable)
        # tp.MutableMapping[_T, Any], # removed 0.3.27a5 (inherits from Mapping)
        # tp.MutableSet[_T], # removed 0.3.27a5 (inherits from AbstractSet)
        # tp.AbstractSet[_T], # removed 0.3.27a5 (inherits from Iterable)
        Iterable, 
        # ct.ChainMap[_T], # removed 0.3.27a5 (inherits from MutableMapping)
        # ct.OrderedDict[_T], # removed 0.3.27a5 (inherits from dict -> MutableMapping)
        ### LOG: 0.3.26b3
        # tp.AsyncIterable[_T], # removed 0.3.27a5 (inherits from Iterable)
        ### LOG: 0.3.26c1
        ReckonOperable,
        tk.StringVar, # remove support on 0.3.36
        # LOG: 0.3.27a5
        Sizeable
] # since 0.3.25, renamed from SupportsCountablesLackOfGeneric (0.3.26b3)

Hash = type(hl.sha3_256())
"\\@since 0.3.26rc3"
VarLenHash = type(hl.shake_256())
"\\@since 0.3.26rc3"
BlakeHash = hl.blake2b
"\\@since 0.3.26rc3"
List = list[_T] # 0.3.26b3
"\\@since 0.3.26b3"
Tuple = tuple[_T, ...] # 0.3.26b3
"\\@since 0.3.26b3"
Deque = ct.deque[_T] # 0.3.26b3
"\\@since 0.3.26b3"
# Array = array[_T] # 0.3.26b3
"\\@since 0.3.26b3"
Dict = dict[_KT, _VT] # 0.3.26b3
"\\@since 0.3.26b3"
Bytes = bytes # 0.3.26b3
"\\@since 0.3.26b3"
ByteArray = bytearray # 0.3.26b3
"\\@since 0.3.26b3"
Filter = filter # 0.3.26b3
"\\@since 0.3.26b3"
Type = type # 0.3.26b3
"\\@since 0.3.26b3"
Zip = zip # 0.3.26b3
"\\@since 0.3.26b3"
Slice = slice # 0.3.26c1
"\\@since 0.3.26rc1"
Object = object
"\\@since 0.3.26rc3"

ColorType = IntegerStringUnion[None] # since 0.3.25, renamed from SupportsColor (0.3.26b3)
ColourType = ColorType # 0.3.26b3
AbroadValue1 = _uni[int, float, complex, ReckonType[_T]] # since 0.3.25, renamed from SupportsAbroadValue1 (0.3.26b3)
AbroadValue2 = _opt[_uni[int, float, bool, ReckonType[_T]]] # since 0.3.25, renamed from SupportsAbroadValue2 (0.3.26b3)
AbroadModifier = _opt[_uni[AbroadValue1[_T]]] # since 0.3.25, renamed from SupportsAbroadModifier (0.3.26b3)
ModernReplace = _uni[list[_T], tuple[_T, ...], _T] # since 0.3.25, expected string; renamed from SupportsModernReplace (0.3.26b3)
PickSequence = _uni[list[_T], tuple[_T, ...], set[_T], frozenset[_T], ct.deque[_T], tp.Sequence[_T], tp.MutableSequence[_T]] # since 0.3.25, added support for Sequence and MutableSequence, renamed from SupportsPick (0.3.26b3)
SanitizeMode = _lit[0, 1, 2, 3, 4, 5] # since 0.3.25, renamed from SupportsSanitizeMode (0.3.26b3)
TenseVersionType = tuple[_T, _T, _T] # since 0.3.25, renamed from SupportsTenseVersion (0.3.26b3)
AbroadPackType = _uni[list[_T], tuple[_T, ...], ct.deque[_T], set[_T], enumerate[_T], frozenset[_T]] # since 0.3.25, lose of dict and defaultdict support, added frozenset, renamed from SupportsAbroadPackValues (0.3.26b3)
AbroadConvectType = AbroadValue1[_T] # since 0.3.25, renamed from SupportsAbroadConvectValues (0.3.26b3)
AbroadLiveType = AbroadConvectType[_T] # since 0.3.25, renamed from SupportsAbroadLiveValues (0.3.26b3)
AbroadVividType = _uni[tuple[AbroadValue1[_V1]], tuple[AbroadValue1[_V1], AbroadValue2[_V2]], tuple[AbroadValue1[_V1], AbroadValue2[_V2], AbroadModifier[_M]]] # since 0.3.25, renamed from SupportsAbroadVividValues (0.3.26)
# SupportsAbroadDivisor = _uni[int, float] # for 0.3.25 - 0.3.26b3, use FloatOrInteger instead
AbroadInitializer = list[_T] # since 0.3.25
AbroadMultiInitializer = list[list[_T]] # since 0.3.25
FloatOrInteger = _uni[int, float] # since 0.3.25
ProbabilityType = _uni[_T, list[_opt[_T]], tuple[_T, _opt[_T]], dict[_T, _opt[_T]], ct.deque[_opt[_T]], set[_opt[_T]], frozenset[_opt[_T]]] # since 0.3.25, expected integer; renamed from SupportsProbabilityValuesAndFrequencies (0.3.26b3)
ShuffleType = _uni[str, list[_T], tp.MutableSequence[_T]] # since 0.3.26rc1
TypeOrFinalVarType = _uni[_T, FinalVar[_T]] # since 0.3.26rc1

_IntegerConvertible = _uni[str, Buffer, IntegerConvertible, Indexable, Truncable] # since 0.3.26rc1
_FloatConvertible = _uni[str, Buffer, FloatConvertible, Indexable] # since 0.3.26rc1
_ComplexConvertible = _uni[complex, FloatConvertible, Indexable] # since 0.3.26rc1

if sys.version_info >= (3, 10):
    from types import NoneType as NoneType
    "\\@since 0.3.26"
else:
    # Used by type checkers for checks involving None (does not exist at runtime)
    @final
    class NoneType:
        "\\@since 0.3.26"
        def __bool__(self) -> Literal[False]: ...

class Integer:
    """
    \\@since 0.3.26b3
    
    Equivalent to `int`. Once instantiated, it returns \\
    integer of type `int`. (0.3.26c1)
    """
    def __new__(cls, x: _IntegerConvertible = ..., /):
        """
        \\@since 0.3.26b3
        
        Equivalent to `int`. Once instantiated, it returns \\
        integer of type `int`. (0.3.26c1)
        """
        return int(x)
    def __instancecheck__(self, obj: object, /) -> TypeIs[int]:
        return isinstance(obj, int)

class Float:
    """
    \\@since 0.3.26b3
    
    Equivalent to `float`. Once instantiated, it returns \\
    number of type `float`. (0.3.26c1)
    """
    def __new__(cls, x: _FloatConvertible = ..., /):
        """
        \\@since 0.3.26b3
        
        Equivalent to `float`. Once instantiated, it returns \\
        number of type `float`. (0.3.26c1)
        """
        return float(x)
    def __instancecheck__(self, obj: object, /) -> TypeIs[float]:
        return isinstance(obj, float)
    
class Complex:
    """
    \\@since 0.3.26b3
    
    Equivalent to `complex`. Once instantiated, it returns \\
    number of type `complex`. (0.3.26c1)
    """
    def __new__(cls, r: _uni[ComplexConvertible, _ComplexConvertible] = ..., i: _ComplexConvertible = ..., /):
        """
        \\@since 0.3.26b3
        
        Equivalent to `complex`. Once instantiated, it returns \\
        number of type `complex`. (0.3.26c1)
        """
        return complex(r, i)
    def __instancecheck__(self, obj: object, /) -> TypeIs[complex]:
        return isinstance(obj, complex)
    
class String:
    """
    \\@since 0.3.26b3
    
    Equivalent to `str`. Once instantiated, it returns \\
    string of type `str`. (0.3.26c1)
    """
    def __new__(cls, x: object = ..., /):
        """
        \\@since 0.3.26b3
        
        Equivalent to `str`. Once instantiated, it returns \\
        string of type `str`. (0.3.26c1)
        """
        return str(x)
    def __instancecheck__(self, obj: object, /) -> TypeIs[str]:
        return isinstance(obj, str)

class Boolean:
    """
    \\@since 0.3.26b3
    
    Equivalent to `bool`. Once instantiated, it returns \\
    boolean of type `bool`. (0.3.26c1)
    """
    def __new__(cls, x: object = ..., /):
        """
        \\@since 0.3.26b3
        
        Equivalent to `bool`. Once instantiated, it returns \\
        boolean of type `bool`. (0.3.26c1)
        """
        return bool(x)
    def __instancecheck__(self, obj: object, /) -> TypeIs[bool]:
        return obj is True or obj is False

def _isAbstract(o: object):
    "\\@since 0.3.26rc3"
    from inspect import isabstract
    return isabstract(o)

################ TypeScript References ################
false: Literal[False] = False
"\\@since 0.3.26rc3"
true: Literal[True] = True
"\\@since 0.3.26rc3"
never = Never
"\\@since 0.3.26rc3"
number = Union[int, str] # on JavaScript there is no 'complex' number type
"\\@since 0.3.26rc3"
void = type(None)
"\\@since 0.3.26rc3"

if __name__ == "__main__":
    _E(111)

del os, ma, mmap, array, copy, tp, tpe, ty, ct, io, tk, wa, fn, abc, abc2, aio, sb, enum, ins, zi, url, hl, dis, ast # Not for export

__all__ = sorted([n for n in globals() if n[:1] != "_"])
"\\@since 0.3.26rc1? Whole gamut of declarations written in `tense.types_collection` module"

__constants__ = sorted([n for n in globals() if n[:1] != "_" and n.isupper()])
"\\@since 0.3.26c3. All constants in `tense.types_collection` module"

__non_constants__ = sorted([n for n in globals() if n[:1] != "_" and not n.isupper()])
"\\@since 0.3.26c3. All non-constants (functions, classes, type aliases) in `tense.types_collection` module"

__typing_util__ = sorted([
    # let me know if I missed some types from typing module!
    Optional.__name__,
    Union.__name__,
    Callable.__name__,
    Concatenate.__name__,
    Pack.__name__ + " (alias to 'Concatenate')",
    Annotated.__name__,
    TypeAlias.__name__,
    "TypeAliasType", # its __name__ is instance of 'property' built-in
    TypeGuard.__name__,
    TypeIs.__name__,
    Unpack.__name__,
    "Any",
    Final2.__name__,
    Literal.__name__,
    LiteralString.__name__,
    ClassVar.__name__,
    Generic.__name__,
    Protocol.__name__,
    "NoDefault", # its __name__ is Any
    NotRequired.__name__,
    Required.__name__,
    Self.__name__,
    "SpecVar (known as ParamSpec)", # its __name__ is instance of 'property' built-in
    SpecVarArgs.__name__ + " (known as ParamSpecArgs)",
    SpecVarKwargs.__name__ + " (known as ParamSpecKwargs)",
    NamedTuple.__name__,
    NewType.__name__,
    NoReturn.__name__,
    ForwardRef.__name__,
])
"\\@since 0.3.26c3. Utility types from `typing` module in `tense.tcs` module"

__abc__ = sorted([n for n in globals() if n[:1] != "_" and ((_isAbstract(globals()[n]) or n.startswith((
    "Async", "Bitwise"
)) and not n.endswith(("Provider", "Abc"))) or n.endswith((
    "Operable",
    "Reassignable",
    "Comparable",
    "Collection",
    "Convertible",
    "Representable"
)) or n in (
    "Invocable",
    "Absolute",
    "Negative",
    "Positive",
    "Iterable",
    "Reversible",
    "Formattable",
    "Ceilable",
    "Floorable",
    "Truncable",
    "Awaitable",
    "Containable",
    "Indexed",
    "Indexable",
    "Hashable"
    )
)])
"\\@since 0.3.26c3. ABCs (Abstract Base Classes) in `tense.tcs` module"

__author__ = "Aveyzan, <p1k4zx@gmail.com>"
"\\@since 0.3.26rc3"
__license__ = "MIT"
"\\@since 0.3.26rc3"
__version__ = VERSION
"\\@since 0.3.26rc3"