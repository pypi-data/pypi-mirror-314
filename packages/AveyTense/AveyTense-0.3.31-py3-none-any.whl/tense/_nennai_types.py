"""
**Tense Nennai Types** \n
\\@since 0.3.24 \\
© 2023-Present Aveyzan // License: MIT
```
module tense._nennai_types
```
Provides Nennai classes, types in overall.
"""
from __future__ import annotations
import sys

if sys.version_info < (3, 9):
    err, s = (RuntimeError, "To use TensePy library, consider having Python 3.9 or newer.")
    raise err(s)

import warnings, uuid, random as ra, re, math as m
from ._primal import abroad, reckon, tc
from . import _abroad as _ab_mod

__module__ = "tense"

# between @since and @author there is unnecessarily long line spacing
# hence this warning is being thrown; it is being disabled.
warnings.filterwarnings("ignore", category = SyntaxWarning)

_var = tc.TypeVar
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
_T3 = _var("_T3")

_V1 = _var("_V1")
_V2 = _var("_V2")
_M = _var("_M")

# _T_fi = _var("_T_fi", bound = _uni[int, float]) # int/float
# _T_sb = _var("_T_sb", bound = _uni[str, bytes]) # str/bytes

_ReplaceFlagType = _lit[
    # including only official inside "re" module of class "RegexFlag"
    re.RegexFlag.NOFLAG,
    re.RegexFlag.A,
    re.RegexFlag.I,
    re.RegexFlag.L,
    re.RegexFlag.U,
    re.RegexFlag.M,
    re.RegexFlag.S,
    re.RegexFlag.X
]

_ReckonNGT = tc.ReckonNGT
_AbroadValue1 = _uni[tc.AbroadValue1[_T]]
_AbroadValue2 = _uni[tc.AbroadValue2[_T]]
_AbroadModifier = _uni[tc.AbroadModifier[_T]]
_AbroadPackType = tc.AbroadPackType[_T]
_AbroadConvectType = tc.AbroadConvectType[_T]
_AbroadLiveType = tc.AbroadLiveType[_T]
_AbroadVividType = tc.AbroadVividType[_V1, _V2, _M]
_RandomizeType = tc.PickSequence[_T]

_AbroadStringInitializer = _ab_mod.AbroadStringInitializer
_AbroadFloatyInitializer = _ab_mod.AbroadFloatyInitializer
_AbroadMultiInitializer = tc.AbroadInitializer[tc.AbroadInitializer[int]]
_AbroadImmutableInitializer = tuple[int, ...]
_AbroadIntFloatInitializer = list[_T]

def _disassign(self, array: list[_T], *items: _T):
    """Since 0.3.17, unavailable for 0.3.24"""
    a: list[_T] = []
    for i1 in abroad(array):
        for i2 in abroad(items):
            if array[i1] != items[i2]: a.append(array[i1])
    return a


# class _AbroadHexMode(tc.IntegerFlag): ### to 0.3.27
class _AbroadHexMode(tc.Enum):
    "\\@since 0.3.26rc2. Internal class for class method `Tense.abroadHex()` parameter `mode`"
    INCLUDE = 0
    INCLUDE_HASH = 1
    EXCLUDE = 2

if False: # can be shortened to _AbroadHexMode (0.3.27)
    _AbroadHexModeType = _lit[
        _AbroadHexMode.INCLUDE,
        _AbroadHexMode.INCLUDE_HASH,
        _AbroadHexMode.EXCLUDE
    ]
    "\\@since 0.3.26rc2"

_AbroadEachType = _opt[_cal[[int], _T]]
"\\@since 0.3.26rc2"



class NennaiAbroads:
    """
    \\@since 0.3.24
    ```
    in module tense
    ```
    Reference from TenseTS (Tense TypeScript; former Tense03). \\
    Basing on former class `Tense03NennaiAbroads`; has special \\
    variations of `abroad()` function.
    """
    from . import types_collection as __tc
    ABROAD_HEX_INCLUDE = _AbroadHexMode.INCLUDE
    "\\@since 0.3.26rc2"
    ABROAD_HEX_INCLUDE_HASH = _AbroadHexMode.INCLUDE_HASH
    "\\@since 0.3.26rc2"
    ABROAD_HEX_EXCLUDE = _AbroadHexMode.EXCLUDE
    "\\@since 0.3.26rc2"
    @_cm
    def abroadPositive(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None):
        """
        \\@since 0.3.24 \\
        \\@modified 0.3.25 (moved slash to between `value1` and `value2`), 0.3.29
        ```
        "class method" in class NennaiAbroads
        ```
        Every negative integer is coerced to positive.
        """
        ab = abroad(value1, value2, modifier)
        return type(ab)([abs(e) for e in ab], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadNegative(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None):
        """
        \\@since 0.3.24 \\
        \\@modified 0.3.25 (moved slash to between `value1` and `value2`), 0.3.29
        ```
        "class method" in class NennaiAbroads
        ```
        Every positive integer is coerced to negative.
        """
        ab = abroad(value1, value2, modifier)
        return type(ab)([-abs(e) for e in ab], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadPositiveFlip(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None):
        """
        \\@since 0.3.24 \\
        \\@modified 0.3.25 (moved slash to between `value1` and `value2`), 0.3.29
        ```
        "class method" in class NennaiAbroads
        ```
        Every negative integer is coerced to positive, then sequence is reversed.
        """
        ab = abroad(value1, value2, modifier)
        return type(ab)([abs(e) for e in ab][::-1], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadNegativeFlip(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None):
        """
        \\@since 0.3.24 \\
        \\@modified 0.3.25 (moved slash to between `value1` and `value2`), 0.3.29
        ```
        "class method" in class NennaiAbroads
        ```
        Every positive integer is coerced to negative, then sequence is reversed.
        """
        ab = abroad(value1, value2, modifier)
        return type(ab)([-abs(e) for e in ab][::-1], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadPack(self, *values: _AbroadPackType[_T]):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.29
        ```
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function bases on `zip()` Python function.
        """
        from ._primal import reckonLeast
        ab = abroad(reckonLeast(*values))
        a = [e for e in ab]
        return type(ab)(a, ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadExclude(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, *excludedIntegers: int):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.29
        ```
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function is the same as `abroad()` function, \\
        but it also allows to exclude specific integers from the returned list. \\
        If all are excluded, returned is empty integer list. If integers excluded \\
        do not exist in returned sequence normally, this issue is omitted.
        """
        for e in excludedIntegers:
            if not isinstance(e, int):
                error = TypeError("every item in parameter 'excludedIntegers' must be an integer")
                raise error
        
        ab = abroad(value1, value2, modifier)
        return type(ab)([e for e in ab if e not in excludedIntegers], ab.params[0], ab.params[1], ab.params[2])
    

    @_cm
    def abroadPrecede(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, prefix: _opt[str] = None):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.29
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function returns strings in a list. If `prefix` is `None`, \\
        returned are integers in strings, otherwise added is special string prefix before integers.
        """
        if prefix is not None and not isinstance(prefix, str):
            error = TypeError(f"Parameter '{prefix.__name__}' is not a string. Ensure argument got value of type 'str'. Received type: {type(prefix).__name__}")
            raise error

        ab = abroad(value1, value2, modifier)
        return _AbroadStringInitializer([str(e) for e in ab] if prefix is None else [prefix + str(e) for e in ab], ab.params[0], ab.params[1], ab.params[2])
            

    @_cm
    def abroadSufcede(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, suffix: _opt[str] = None):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.29
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function returns strings in a list. If `prefix` is `None`, \\
        returned are integers in strings, otherwise added is special string suffix after integers.
        """
        if suffix is not None and not isinstance(suffix, str):
            error = TypeError(f"Parameter '{suffix.__name__}' is not a string. Ensure argument got value of type 'str'. Received type: {type(suffix).__name__}")
            raise error

        ab = abroad(value1, value2, modifier)
        return _AbroadStringInitializer([str(e) for e in ab] if suffix is None else [str(e) + suffix for e in ab], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadInside(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, string: _opt[str] = None):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.29
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function returns strings in a list. If `string` is `None`, \\
        returned are integers in strings, otherwise integers are placed inside `{}` of the string.
        """
        if string is not None and not isinstance(string, str):
            error = TypeError(f"Parameter '{string.__name__}' is not a string. Ensure argument got value of type 'str'. Received type: {type(string).__name__}")
            raise error

        ab = abroad(value1, value2, modifier)
        return _AbroadStringInitializer([str(e) for e in ab] if string is None else [string.format(str(e)) for e in ab], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    @tc.deprecated("Pending removal on 0.3.30 due to reorganization of sequences returned by abroad() function and many of its variations (retrieve tuple via -abroad(...)) during 0.3.28 - 0.3.29")
    def abroadImmutable(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None) -> _AbroadImmutableInitializer:
        """
        \\@since 0.3.25
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        Immutable variation of `abroad()` function - instead of list returned is tuple. \\
        Equals `tuple(abroad(...))`.
        """
        return tuple(abroad(value1, value2, modifier))
    
    @_cm
    def abroadConvect(self, *values: _AbroadConvectType[_T]):
        """
        \\@since 0.3.25
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        Typical math sum operation before returned is list from `abroad()` function. \\
        If from values a value is:
        - an integer - added is this integer
        - a float - added is this number, without fraction
        - a complex - added are both real and imaginary parts
        - sizeable object - added is its length

        Notice: you can also provide negative entities! If resulted number is negative, \\
        up to `abroad()` function, sequence will go in range `[values_sum, -1]`. \\
        Otherwise, it will take this form: `[0, values_sum - 1]`.
        """
        i = 0
        if reckon(values) == 0:
            err, s = (self.__tc.MissingValueError, "Expected at least one item in parameter 'values'.")
            raise err(s)
        for e in values:
            if not isinstance(e, (_ReckonNGT, int, float, complex)):
                err, s = (TypeError, f"From gamut of supported types, parameter 'values' has at least one unsupported type: '{type(e).__name__}'")
                raise err(s)
            elif isinstance(e, int):
                i += e
            elif isinstance(e, float):
                i += m.trunc(e)
            elif isinstance(e, complex):
                i += m.trunc(e.real) + m.trunc(e.imag)
            else:
                i += reckon(e)
        return abroad(i)
    
    @_cm
    def abroadLive(self, *values: _AbroadLiveType[_T]):
        """
        \\@since 0.3.25
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        Concept from non-monotonous sequences from math. Like graph, \\
        which changes per time. If from values a value is:
        - an integer - this is next point
        - a float - next point doesn't have fraction
        - a complex - next point is sum of real and imaginary parts
        - sizeable object - its length is next point
        """
        a: list[int] = []
        ret: list[int] = []
        if reckon(values) == 0:
            err, s = (self.__tc.MissingValueError, "Expected at least one item in parameter 'values'.")
            raise err(s)
        for e in values:
            if not isinstance(e, (_ReckonNGT, int, float, complex)):
                err, s = TypeError, f"From gamut of supported types, parameter 'values' has at least one unsupported type: '{type(e).__name__}'"
                raise err(s)
            elif isinstance(e, int):
                a.append(e)
            elif isinstance(e, float):
                a.append(m.trunc(e))
            elif isinstance(e, complex):
                a.append(m.trunc(e.real) + m.trunc(e.imag))
            else:
                a.append(reckon(e))
        for i1 in abroad(1, a):
            tmp = a[i1]
            if tmp < 0: tmp -= 1
            else: tmp += 1
            for i2 in abroad(a[i1 - 1], tmp): 
                ret.append(i2)
        return ret
    
    @_cm
    def abroadFloaty(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, div: tc.FloatOrInteger = 10):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.29
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        Every item from `abroad()` function will be divided by parameter `div`. \\
        It's default value is `10`.
        """
        if not isinstance(div, (int, float)):
            error = TypeError (f"Parameter 'div' is not an integer nor floating-point number. Ensure argument got value of type 'int' or 'float'. Received type: {type(div).__name__}")
            raise error
        
        elif isinstance(div, float) and div in (m.nan, m.inf):
            error = ValueError ("Parameter 'div' may not be infinity or not a number.")
            raise error
        
        elif (isinstance(div, int) and div == 0) or (isinstance(div, float) and div == .0):
            error = ZeroDivisionError ("Parameter 'div' may not be equal zero. This is attempt to divide by zero")
            raise error
        
        ab = abroad(value1, value2, modifier)
        return _AbroadFloatyInitializer([e / div for e in ab], ab.params[0], ab.params[1], ab.params[2])
    
    @_cm
    def abroadSplit(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, limit = 2) -> _AbroadMultiInitializer:
        """
        \\@since 0.3.25
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        Reference to string slicing. Limit is amount of items, \\
        which can be in one sub-list. May not be equal or below 1.
        """
        lim = 0
        tmp: list[int] = []
        a: list[list[int]] = [[]]
        if not isinstance(limit, int):
            err, s = (TypeError, f"Parameter 'limit' is not an integer. Ensure argument got value of type 'int'. Received type: {type(limit).__name__}")
            raise err(s)
        elif limit < 1:
            err, s = (ValueError, "Parameter 'limit' may not be negative, or have value 0 or 1. Start from 2.")
            raise err(s)
        for i in abroad(value1, value2, modifier):
            if lim % limit == 0:
                a.append(tmp)
                tmp.clear()
            else:
                tmp.append(i)
            lim += 1
        return a
    
    @_cm
    def abroadVivid(self, *values: _AbroadVividType[_V1, _V2, _M]) -> _AbroadMultiInitializer:
        """
        \\@since 0.3.25
        ```
        # created 09.07.2024
        "class method" in class NennaiAbroads
        ```
        For every value in `values` returned is list `[abroad(V1_1, V2_1?, M_1?), abroad(V1_2, V2_2?, M_2?), ...]`. \\
        Question marks are here to indicate optional values.
        """
        a: list[list[int]] = [[]]
        if reckon(values) < 2:
            err, s = (ValueError, "Expected at least 2 items in parameter 'values'.")
            raise err(s)
        for e in values:
            if not isinstance(e, tuple):
                err, s = (TypeError, f"Parameter 'values' has an item, which isn't a tuple. Ensure every item is of type 'tuple'. Received type: {type(e).__name__}")
                raise err(s)
            if reckon(e) == 1:
                a.append(abroad(e[0]))
            elif reckon(e) == 2:
                a.append(abroad(e[0], e[1]))
            elif reckon(e) == 3:
                a.append(abroad(e[0], e[1], e[2]))
            else:
                err, s = (ValueError, "Parameter 'values' may not have empty tuples, nor tuples of size above 3.")
                raise err(s)
        return a
    
    @_cm
    def abroadEach(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, each: _AbroadEachType[_T] = None) -> _AbroadIntFloatInitializer[_T]:
        """
        \\@since 0.3.25 (experimental for 0.3.25 - 0.3.26b1)
        ```
        # created 10.07.2024
        "class method" in class NennaiAbroads
        ```
        Invoked is `each` callback for every item in `abroad()` function.
        """
        a: list[int] = []
        if each is None:
            a: list[int] = []
        else:
            a: list[_uni[int, float]] = []
        for i in abroad(value1, value2, modifier):
            if each is None:
                a.append(i)
            else:
                tmp = each(i)
                if not isinstance(tmp, (int, float)):
                    err, s = (ValueError, "Parameter 'each' returns invalid type or has invalid parameter type (expected 'int' or 'float'), has too much parameters, or is not a callable object. Use 'lambda' expression, like 'lambda x: Tense.cbrt(x)'.")
                    raise err(s)
                a.append(tmp)
        return a
    
    @_cm
    def abroadHex(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, mode: _AbroadHexMode = ABROAD_HEX_INCLUDE) -> _AbroadStringInitializer:
        """
        \\@since 0.3.25
        ```
        # created 10.07.2024
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function returns hexadecimal representation of each integer.

        Modes (for 0.3.26rc2; to 0.3.27 support for integers):
        - `self.ABROAD_HEX_INCLUDE` - appends `0x` to each string. It faciliates casting to integer.
        - `self.ABROAD_HEX_INCLUDE_HASH` - appends `#` to each string. Reference from CSS.
        - `self.ABROAD_HEX_EXCLUDE` - nothing is appended.
        """
        a: list[str] = []
        for i in abroad(value1, value2, modifier):
            if not isinstance(mode, _AbroadHexMode):
                err, s = (ValueError, "expected a constant preceded with 'ABROAD_HEX_'")
                raise err(s)
            elif mode == self.ABROAD_HEX_INCLUDE:
                a.append(hex(i))
            elif mode == self.ABROAD_HEX_INCLUDE_HASH:
                a.append(re.sub(r"^0x", "#", hex(i)))
            else:
                a.append(re.sub(r"^0x", "", hex(i)))
        return a
    
    @_cm
    def abroadBinary(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None, include_0b = True) -> _AbroadStringInitializer:
        """
        \\@since 0.3.25
        ```
        # created 10.07.2024
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function returns binary representation of each integer. \\
        Parameter `include_0b` allows to append `0b` before binary notation, what allows \\
        to faciliate casting to integer. Defaults to `True`
        """
        a: list[str] = []
        for i in abroad(value1, value2, modifier):
            if not isinstance(include_0b, bool):
                err, s = (TypeError, "Expected parameter 'include_0b' to be of type 'bool'.")
                raise err(s)
            elif include_0b:
                a.append(bin(i))
            else:
                a.append(re.sub(r"^0b", "", bin(i)))
        return a
    
    @_cm
    def abroadOctal(self, value1: _AbroadValue1[_T1], /, value2: _AbroadValue2[_T2] = None, modifier: _AbroadModifier[_T3] = None) -> _AbroadStringInitializer:
        """
        \\@since 0.3.25
        ```
        # created 18.07.2024
        "class method" in class NennaiAbroads
        ```
        This variation of `abroad()` function returns octal representation of each integer. \\
        Every string will be preceded with `0o`
        """
        a: list[str] = []
        for i in abroad(value1, value2, modifier):
            # if not isinstance(include_0o, bool):
            #    err, s = (TypeError, "Expected parameter 'include_0o' to be of type 'bool'.")
            #    raise err(s)
            # elif include_0o:
                a.append(oct(i))
            # else:
            #   a.append(re.sub(r"^0o", "", oct(i)))
        return a
    
# class _SanitizeMode(tc.IntegerFlag): ### to 0.3.27
class _SanitizeMode(tc.Enum):
    "\\@since 0.3.26rc2. Interal class for method `Tense.sanitize()` parameter `mode`"
    AROUND = 0
    ALL = 1
    ACF = 2
    LEFT = 3
    RIGHT = 4
    CENTER = 5

if False: # can be shortened to _SanitizeMode (0.3.27)
    _SanitizeModeType = _lit[
        _SanitizeMode.AROUND,
        _SanitizeMode.ALL,
        _SanitizeMode.ACF,
        _SanitizeMode.LEFT,
        _SanitizeMode.RIGHT,
        _SanitizeMode.CENTER
    ]
    "\\@since 0.3.26rc2"

@tc.deprecated("Class will be removed on 0.3.28; consider not using it since it is weak addition")
class NennaiStringz:
    """
    \\@since 0.3.25
    ```
    in module tense
    ```
    You are discouraged to use this class (general note for 0.3.27). \\
    In overall class during experiments.
    """
    from . import types_collection as __tc
    import re as __re
    # SANITIZE_AROUND = TenseType(8376.1)
    # SANITIZE_ALL = TenseType(8376.2)
    # SANITIZE_ACF = TenseType(8376.3)
    # SANITIZE_LEFT = TenseType(8376.4)
    # SANITIZE_RIGHT = TenseType(8376.5)
    # SANITIZE_CENTER = TenseType(8376.6)
    SANITIZE_AROUND = _SanitizeMode.AROUND
    SANITIZE_ALL = _SanitizeMode.ALL
    SANITIZE_ACF = _SanitizeMode.ACF
    SANITIZE_LEFT = _SanitizeMode.LEFT
    SANITIZE_RIGHT = _SanitizeMode.RIGHT
    SANITIZE_CENTER = _SanitizeMode.CENTER
    
    @_cm
    def sanitize(self, string: str, /, mode: _SanitizeMode = SANITIZE_AROUND):
        """
        \\@since 0.3.25 (experimental)
        ```
        "class method" in class NennaiStringz
        ```
        1 of 6 options (`SANITIZE_ACF`) is experimental, expect behavior to change! \\
        All other are supported normally.
        """
        if not isinstance(string, str):
            err = TypeError
            s = f"Parameter 'string' is not a string. Ensure argument got value of type 'str'. Received type: {type(string).__name__}"
            raise err(s)
        elif not isinstance(mode, int):
            err = TypeError
            s = f"Parameter 'mode' is not an instance of 'TenseType'. Ensure argument got value of type 'TenseType'. Received type: {type(mode).__name__}"
            raise err(s)
        checkout = [i / 10 for i in abroad(83761, 83767)]
        for e in checkout:
            if mode.receive() == e: break
        if mode.receive() not in checkout:
            err = ValueError
            s = f"Parameter 'mode' has incorrect 'TenseType' value. Ensure you are using one of constants starting with 'SANITIZE_' as value of this parameter."
            raise err(s)
        def ws(char: str): return reckon(char) == 1 and char in "\n\f\r\v\t"
        ret = ""
        arr = [""]
        arr.clear()
        for c in string: arr.append(c)
        if mode == self.SANITIZE_AROUND:
            ret = string.strip()
        elif mode == self.SANITIZE_ALL:
            for i in abroad(ret):
                if not ws(arr[i]): ret += arr[i]
        elif mode == self.SANITIZE_LEFT:
            ret = string.lstrip()
        elif mode == self.SANITIZE_RIGHT:
            ret = string.rstrip()
        elif mode == self.SANITIZE_CENTER:
            g1, g2 = (0, reckon(arr) - 1)
            while ws(arr[g1]): g1 += 1
            while ws(arr[g2]): g2 -= 1
            for _ in abroad(g1): ret += " "
            for i in abroad(g1, g2 + 1):
                if not ws(arr[i]): ret += arr[i]
            for _ in abroad(g2 + 1, arr): ret += " "
            ret = str(ret)
        return ret
    
    @_cm
    def sanitizeAround(self, string: str, /, left: int = -1, right: int = -1):
        """
        \\@since 0.3.25 (experimental)
        ```
        "class method" in class NennaiStringz
        ```
        Alias to `self.sanitize(string, mode = self.SANITIZE_AROUND)`. \\
        Parameters `left` and `right` allow to describe, how many whitespaces \\
        shall be excluded from returned string.
        """
        ret = ""
        if not isinstance(string, str):
            err, s = (TypeError, f"Parameter 'string' is not a string. Ensure argument got value of type 'str'. Received type: {type(string).__name__}")
            raise err(s)
        if not isinstance(left, int):
            err, s = (TypeError, f"Parameter 'left' is not an integer. Ensure argument got value of type 'int'. Received type: {type(left).__name__}")
            raise err(s)
        if not isinstance(right, int):
            err, s = (TypeError, f"Parameter 'left' is not an integer. Ensure argument got value of type 'int'. Received type: {type(right).__name__}")
            raise err(s)
        if left < -1 or right < -1:
            err, s = (ValueError, f"Either 'left' or 'right' is below -1. Make sure both parameter have positive values or -1. Received values: 'left' -> {left}, 'right' -> {right}")
            raise err(s)
        if left == 0 and right == 0:
            return string
        if left == -1:
            ret = string.lstrip()
        elif left > 0:
            ret = self.__re.sub("^[\f\r\n\t\v]{" + str(left) + "}", "", string)
        if right == -1:
            ret = string.rstrip()
        elif right > 0:
            ret = self.__re.sub("[\f\r\n\t\v]{" + str(right) + "}$", "", string)
        return ret
    
    @_cm
    def replace(self, string: str, pattern: _uni[str, __tc.Pattern[str]], replace: _uni[str, __tc.Callable[[__tc.Match[str]], str]], count = 0, flags: _ReplaceFlagType = 0):
        """
        \\@since 0.3.26
        ```
        "class method" in class NennaiStringz
        ```
        Equivalent to `re.sub()`, just `string` parameter in code \\
        is placed on the beginning of parameter list.
        """
        return self.__re.sub(pattern, replace, string, count, flags)

class NennaiRandomize:
    """
    \\@since 0.3.25
    ```
    # created 14.07.2024
    in module tense
    ```
    Class for randomizing things
    """
    
    @_cm
    def randomize(self, sequence: _RandomizeType[_T], /) -> _T:
        """
        \\@since 0.3.25
        ```
        # created 14.07.2024
        "class method" in class NennaiRandomize
        ```
        Same as `Tense.pick()`, returns any item from a sequence.

        As much wanting to provide version with `*items` parameter, \\
        returned type may be unfortunately an united one, if list is \\
        of united type, what can force additional type checking
        """
        from random import randint
        return sequence[randint(0, reckon(sequence) - 1)]
    
    @_cm
    def randomizeInt(self, x: int, y: int, /):
        """
        \\@since 0.3.25
        ```
        # created 15.07.2024
        "class method" in class NennaiRandomize
        ```
        Same as `Tense.random()`.
        """
        from random import randint
        def _rand(x = 0, y = 1):
            return randint(x, y)
        if x > y:
            return _rand(y, x)
        elif x == y:
            return x
        else:
            return _rand(x, y)
        
    @_cm
    def randomizeStr(self, lower = True, upper = True, digits = True, special = True, length = 10):
        """
        \\@since 0.3.9 \\
        \\@lifetime ≥ 0.3.9; < 0.3.24; ≥ 0.3.25
        ```
        # created 15.07.2024
        "class method" in class NennaiRandomize
        ```
        - `lower` - determine, if you want to include all lowercased letters from english alphabet. Defaults to `True`
        - `upper` - determine, if you want to include all uppercased letters from english alphabet. Defaults to `True`
        - `digits` - determine, if you want to include all numbers. Defaults to `True`
        - `special` - determine, if you want to include all remaining chars accessible normally via English keyboard. \\
        Defaults to `True`
        - `length` - allows to specify the length of returned string. Defaults to `10`.
        """
        conv: list[str] = []
        ret = ""
        if lower:
            for e in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"):
                conv.append(e)
        if upper:
            for e in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"):
                conv.append(e)
        if digits:
            for e in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
                conv.append(e)
        if special:
            for e in ("!", "@", "~", "`", "^", "%", "#", "&", "*", "/", "+", "-", "_", "|", "\\", "\"", "'", ":", ";", ">", "<", "?", ",", "."):
                conv.append(e)
        for _ in abroad(length): ret += self.randomize(conv)
        return ret
    
    @_cm
    def randomizeStr2(self, string: str, /):
        """
        \\@since 0.3.26b3
        ```
        # created 25.07.2024
        "class method" in class NennaiRandomize
        ```
        Return shuffled string
        """
        tmp = list(string)
        ra.shuffle(tmp)
        return "".join(tmp)
    
    @_cm
    def randomizeUuid(self):
        """
        \\@since 0.3.26a1
        ```
        # created 20.07.2024
        "class method" in class NennaiRandomize
        ```
        Return a random UUID. Alias to `Tense.uuidRandom()`
        """
        return uuid.uuid4()

# between @since and @author there is unnecessarily long line spacing
# hence this warning is being thrown; it is being disabled.
warnings.filterwarnings("ignore", r"^invalid escape sequence '\\@'", SyntaxWarning)


if __name__ == "__main__":
    err = RuntimeError
    s = "This file is not for compiling, moreover, this file does not have a complete TensePy declarations collection. Consider importing module 'tense' instead."
    raise err(s)

# not for export
del warnings, uuid, sys, m

__all__ = sorted([n for n in globals() if n[:1] != "_"])
__dir__ = __all__
            