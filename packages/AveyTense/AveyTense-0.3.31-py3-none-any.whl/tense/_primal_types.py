"""
**Tense Primal Types** \n
\\@since 0.3.26rc3 \\
© 2024-Present Aveyzan // License: MIT
```
module tense._primal_types
```
Components from `typing` and `typing_extensions` modules mainly. \\
If you see (≥ PY_VERSION) on documented strings, which feature solutions \\
from `typing` module, that is since when that solution is in `typing`. Excluded \\
mean that version since a solution is in `typing` module is nondescript.
"""

from __future__ import annotations
import sys, subprocess as sb

try:
    import typing_extensions as tpe
except (ModuleNotFoundError, ImportError, NameError):
    sb.run([sys.executable, "-m", "pip", "install", "typing_extensions"])

import collections.abc as abc2, enum, inspect as ins, zipfile as zi, dis, types as ty, typing as tp, typing_extensions as tpe, string as st, functools as ft, uuid as uu, re
import timeit as tim, unittest as uni
from dataclasses import dataclass

###### UTILITY TYPES ######

# 'default' parameter inspection (available since 3.13)
# see PEP 696 for details. status: accepted (and used in memoryview class, default type 'int')
if sys.version_info < (3, 13):
    _TypeVar = tpe.TypeVar
else:
    _TypeVar = tp.TypeVar

# using hasattr() instead of sys.version_info due to unknown version which provides
# all of these below
if hasattr(tp, "Union"):
    _Union = tp.Union
else:
    _Union = tpe.Union

if hasattr(tp, "Optional"):
    _Optional = tp.Optional
else:
    _Optional = tpe.Optional

if hasattr(tp, "Callable"):
    _Callable = tp.Callable
else:
    _Callable = tpe.Callable

if hasattr(tp, "Generic"):
    _Generic = tp.Generic
else:
    _Generic = tpe.Generic

TypeVar = _TypeVar
"\\@since 0.3.26b3. [`typing.TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)"
Union = _Union
"\\@since 0.3.26rc1. [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union)"
Optional = _Optional
"\\@since 0.3.26b3. [`typing.Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)"
Callable = _Callable
"\\@since 0.3.26b3. [`typing.Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)"
Generic = _Generic
"\\@since 0.3.26b3. [`typing.Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)"
Callback = Callable
"\\@since 0.3.26rc3. [`typing.Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)"

_T = TypeVar("_T")
_T_sb = TypeVar("_T_sb", str, bytes)
_T_class = TypeVar("_T_class", bound = type)
_T_cov = TypeVar("_T_cov", covariant = True)
# _T_con = TypeVar("_T_con", contravariant = True)
# _KT = TypeVar("_KT")
# _KT_cov = TypeVar("_KT_cov", covariant = True)
# _KT_con = TypeVar("_KT_con", contravariant = True)
# _VT = TypeVar("_VT")
# _VT_cov = TypeVar("_VT_cov", covariant = True)

###### VERSION ASCENDING ######

# since Python 3.5.2
if sys.version_info >= (3, 5, 2):
    _NamedTuple = tp.NamedTuple
    _NewType = tp.NewType
else:
    _NamedTuple = tpe.NamedTuple
    _NewType = tpe.NewType

# since Python 3.5.3
if sys.version_info >= (3, 5, 3):
    # questionable: does this type have to be wrapped into string?
    _ClassVar = tp.ClassVar[_T]
else:
    _ClassVar = tpe.ClassVar[_T]

# since Python 3.6.2
if sys.version_info >= (3, 6, 2):
    _NoReturn = tp.NoReturn
else:
    _NoReturn = tpe.NoReturn

# since Python 3.7.4
if sys.version_info >= (3, 7, 4):
    _ForwardRef = tp.ForwardRef
else:
    _ForwardRef = tpe.ForwardRef

# since Python 3.8
if sys.version_info >= (3, 8):
    _Literal = tp.Literal
    _Final = tp.Final
    _Protocol = tp.Protocol
else:
    _Literal = tpe.Literal
    _Final = tpe.Final
    _Protocol = tpe.Protocol

# since Python 3.5.2
NamedTuple = _NamedTuple
"\\@since 0.3.26rc1. [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) (≥ 3.5.2)"
NewType = _NewType
"\\@since 0.3.26rc1. [`typing.NewType`](https://docs.python.org/3/library/typing.html#typing.NewType) (≥ 3.5.2)"

# since Python 3.5.3
ClassVar = _ClassVar[_T]
"\\@since 0.3.26b3. [`typing.ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar) (≥ 3.5.3)"

# since Python 3.6.2 (older doc, of version 3.6, says 3.6.5)
NoReturn = _NoReturn
"\\@since 0.3.26b3. [`typing.NoReturn`](https://docs.python.org/3/library/typing.html#typing.NoReturn) (≥ 3.6.2)"

# since Python 3.7.4
ForwardRef = _ForwardRef
"\\@since 0.3.26rc3. [`typing.ForwardRef`](https://docs.python.org/3/library/typing.html#typing.ForwardRef) (≥ 3.7.4)"

# since Python 3.8
Literal = _Literal
"\\@since 0.3.26rc1. [`typing.Literal`](https://docs.python.org/3/library/typing.html#typing.Literal) (≥ 3.8)"
Final2 = _Final
"\\@since 0.3.26rc1. [`typing.Final`](https://docs.python.org/3/library/typing.html#typing.Final) (≥ 3.8)"
Protocol = _Protocol
"\\@since 0.3.26rc1. [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) (≥ 3.8)"

# since Python 3.9
if sys.version_info >= (3, 9):
    from typing import IO # type: ignore[unused-import] # idea for pylance
    _Annotated = tp.Annotated
    _BinaryIO = tp.BinaryIO
    _TextIO = tp.TextIO
else:
    from typing_extensions import IO
    _Annotated = tpe.Annotated
    _BinaryIO = tpe.BinaryIO
    _TextIO = tpe.TextIO

Annotated = _Annotated
"\\@since 0.3.26rc1. [`typing.Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) (≥ 3.9)"
BinaryIO = _BinaryIO
"\\@since 0.3.26rc3. [`typing.BinaryIO`](https://docs.python.org/3/library/typing.html#abcs-for-working-with-io) (≥ 3.9)"
TextIO = _TextIO
"\\@since 0.3.26rc3. [`typing.TextIO`](https://docs.python.org/3/library/typing.html#abcs-for-working-with-io) (≥ 3.9)"

# since Python 3.10
if sys.version_info >= (3, 10):
    _SpecVar = tp.ParamSpec
    _SpecVarArgs = tp.ParamSpecArgs
    _SpecVarKwargs = tp.ParamSpecKwargs
    _TypeGuard = tp.TypeGuard[_T]
    _TypeAlias = tp.TypeAlias # not recommended to use it (deprecated feature)
    _Concatenate = tp.Concatenate
    ellipsis = ty.EllipsisType
    _Ellipsis = ty.EllipsisType
else:
    _SpecVar = tpe.ParamSpec
    _SpecVarArgs = tpe.ParamSpecArgs
    _SpecVarKwargs = tpe.ParamSpecKwargs
    _TypeGuard = tpe.TypeGuard[_T]
    _TypeAlias = tpe.TypeAlias
    _Concatenate = tpe.Concatenate
    @tp.final
    class ellipsis: ...
    _Ellipsis = ellipsis()

SpecVar = _SpecVar
"\\@since 0.3.26rc1. [`typing.ParamSpec`](https://docs.python.org/3/library/typing.html#typing.ParamSpec) (≥ 3.10)"
SpecVarArgs = _SpecVarArgs
"\\@since 0.3.26rc1. [`typing.ParamSpecArgs`](https://docs.python.org/3/library/typing.html#typing.ParamSpecArgs) (≥ 3.10)"
SpecVarKwargs = _SpecVarKwargs
"\\@since 0.3.26rc1. [`typing.ParamSpecKwargs`](https://docs.python.org/3/library/typing.html#typing.ParamSpecKwargs) (≥ 3.10)"
TypeAlias = _TypeAlias
"\\@since 0.3.26rc1. [`typing.TypeAlias`](https://docs.python.org/3/library/typing.html#typing.TypeAlias) (≥ 3.10)"
TypeGuard = _TypeGuard[_T]
"\\@since 0.3.26rc1. [`typing.TypeGuard`](https://docs.python.org/3/library/typing.html#typing.TypeGuard) (≥ 3.10)"
Concatenate = _Concatenate
"\\@since 0.3.26rc1. [`typing.Concatenate`](https://docs.python.org/3/library/typing.html#typing.Concatenate) (≥ 3.10)"
Pack = _Concatenate
"\\@since 0.3.26rc1. [`typing.Concatenate`](https://docs.python.org/3/library/typing.html#typing.Concatenate) (≥ 3.10)"
Ellipsis = _Ellipsis
"\\@since 0.3.26rc1. [`Ellipsis`](https://docs.python.org/dev/library/constants.html#Ellipsis)"
ParamSpec = SpecVar
"\\@since 0.3.26rc3. [`typing.ParamSpec`](https://docs.python.org/3/library/typing.html#typing.ParamSpec) (≥ 3.10)"
ParamSpecArgs = SpecVarArgs
"\\@since 0.3.26rc3. [`typing.ParamSpecArgs`](https://docs.python.org/3/library/typing.html#typing.ParamSpecArgs) (≥ 3.10)"
ParamSpecKwargs = SpecVarKwargs
"\\@since 0.3.26rc3. [`typing.ParamSpecKwargs`](https://docs.python.org/3/library/typing.html#typing.ParamSpecKwargs) (≥ 3.10)"

# since Python 3.11
if sys.version_info >= (3, 11):
    _TypeTupleVar = tp.TypeVarTuple
    _NotRequired = tp.NotRequired
    _Required = tp.Required
    _Unpack = tp.Unpack
    _Never = tp.Never
    _Any = tp.Any
    _LiteralString = tp.LiteralString
    _Self = tp.Self
else:
    _TypeTupleVar = tpe.TypeVarTuple
    _NotRequired = tpe.NotRequired
    _Required = tpe.Required
    _Unpack = tpe.Unpack
    _Never = tpe.Never
    _Any = tpe.Any
    _LiteralString = tpe.LiteralString
    _Self = tpe.Self

Any = _Any
"\\@since 0.3.26rc1. [`typing.Any`](https://docs.python.org/3/library/typing.html#typing.Any)"
TypeTupleVar = _TypeTupleVar
"\\@since 0.3.26rc1. [`typing.TypeVarTuple`](https://docs.python.org/3/library/typing.html#typing.TypeVarTuple) (≥ 3.11)"
NotRequired = _NotRequired
"\\@since 0.3.26rc1. [`typing.NotRequired`](https://docs.python.org/3/library/typing.html#typing.NotRequired) (≥ 3.11)"
Required = _Required
"\\@since 0.3.26rc1. [`typing.Required`](https://docs.python.org/3/library/typing.html#typing.Required) (≥ 3.11)"
Unpack = _Unpack
"\\@since 0.3.26rc1. [`typing.Unpack`](https://docs.python.org/3/library/typing.html#typing.Unpack) (≥ 3.11)"
Never = _Never
"\\@since 0.3.26rc1. [`typing.Never`](https://docs.python.org/3/library/typing.html#typing.Never) (≥ 3.11)"
LiteralString = _LiteralString
"\\@since 0.3.26rc1. [`typing.LiteralString`](https://docs.python.org/3/library/typing.html#typing.LiteralString) (≥ 3.11)"
Self = _Self
"\\@since 0.3.26rc1. [`typing.Self`](https://docs.python.org/3/library/typing.html#typing.Self) (≥ 3.11)"
TypeVarTuple = TypeTupleVar
"\\@since 0.3.26rc3. [`typing.TypeVarTuple`](https://docs.python.org/3/library/typing.html#typing.TypeVarTuple) (≥ 3.11)"

# since Python 3.12
if sys.version_info >= (3, 12):
    _TypeAliasType = tp.TypeAliasType
else:
    _TypeAliasType = tpe.TypeAliasType

TypeAliasType = _TypeAliasType
"\\@since 0.3.26rc1. [`typing.TypeAliasType`](https://docs.python.org/3/library/typing.html#typing.TypeAliasType) (≥ 3.12)"

# since Python 3.13
if sys.version_info >= (3, 13):
    _NoDefault = tp.NoDefault
    _TypeIs = tp.TypeIs[_T]
    _ReadOnly = tp.ReadOnly[_T]
else:
    _NoDefault = tpe.NoDefault
    _TypeIs = tpe.TypeIs[_T]
    _ReadOnly = tpe.ReadOnly[_T] # type: ignore

NoDefault = _NoDefault
"\\@since 0.3.26rc1. [`typing.NoDefault`](https://docs.python.org/3/library/typing.html#typing.NoDefault) (≥ 3.13)"
TypeIs = _TypeIs[_T]
"\\@since 0.3.26rc1. [`typing.TypeIs`](https://docs.python.org/3/library/typing.html#typing.TypeIs) (≥ 3.13)"
ReadOnly = _ReadOnly[_T]
"\\@since 0.3.26rc1. [`typing.ReadOnly`](https://docs.python.org/3/library/typing.html#typing.ReadOnly) (≥ 3.13)"

_T_func = TypeVar("_T_func", bound = Callable[..., Any])
_P = SpecVar("_P")
_CoroutineLike = Callable[_P, tp.Generator[Any, Any, _T]]
_DecoratorLike = Callable[_P, _T]

def runtime(c: _T_class):
    """
    \\@since 0.3.26rc1. See [`typing.runtime_checkable`](https://docs.python.org/3/library/typing.html#typing.runtime_checkable)

    A decorator which formalizes protocol class to a protocol runtime. \\
    Protocol class injected with this decorator can be used in `isinstance()` \\
    and `issubclass()` type checking functions.
    """
    if sys.version_info >= (3, 8):
        from typing import runtime_checkable
    else:
        from typing_extensions import runtime_checkable
    return runtime_checkable(c)
    
class Auto(enum.auto):
    "\\@since 0.3.26rc1. See [`enum.auto`](https://docs.python.org/3/library/enum.html#enum.auto)"
    ...

auto = enum.auto
"\\@since 0.3.26. See [`enum.auto`](https://docs.python.org/3/library/enum.html#enum.auto)"

if sys.version_info >= (3, 11):
    class verify(enum.verify):
        "\\@since 0.3.26rc2. See [`enum.verify`](https://docs.python.org/3/library/enum.html#enum.verify)"
        ...
    EnumCheck = enum.EnumCheck
    "\\@since 0.3.26rc1. Various conditions to check an enumeration for. [`enum.EnumCheck`](https://docs.python.org/3/library/enum.html#enum.EnumCheck)"
    ReprEnum = enum.ReprEnum
    "\\@since 0.3.26rc1"
    FlagBoundary = enum.FlagBoundary
    "\\@since 0.3.26rc1"

class IntegerFlag(enum.IntFlag):
    "\\@since 0.3.26rc1. Support for integer-based flags. See [`enum.IntFlag`](https://docs.python.org/3/library/enum.html#enum.IntFlag)"
    ...

class IntegerEnum(enum.IntEnum):
    "\\@since 0.3.26rc1. Enum where members are also (and must be) integers. See [`enum.IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum)"
    ...

class Enum(enum.Enum):
    "\\@since 0.3.26rc1. Create a collection of name/value pairs. See [`enum.Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)"
    ...

EnumType = enum.EnumType
"\\@since 0.3.26rc2. See [`enum.EnumType`](https://docs.python.org/3/library/enum.html#enum.EnumType)"

class StringEnum(enum.StrEnum):
    "\\@since 0.3.26rc1. Enum where members are also (and must be) strings. See [`enum.StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)"
    ...

class Flag(enum.Flag):
    "\\@since 0.3.26rc1. Support for flags. See [`enum.Flag`](https://docs.python.org/3/library/enum.html#enum.Flag)"
    ...

# try: # before 0.3.36 to be applied
import tkinter as tk

@tpe.deprecated("Deprecated since 0.3.31, will be removed on 0.3.36. Deviating from Tkinter technology.")
class IntegerVar(tk.IntVar):
    "\\@since 0.3.26rc1. Value holder for integer variables. See `tkinter.IntVar` (doc not available)"
    ...

@tpe.deprecated("Deprecated since 0.3.31, will be removed on 0.3.36. Deviating from Tkinter technology.")
class StringVar(tk.StringVar):
    "\\@since 0.3.26rc1. Value holder for string variables. See `tkinter.StringVar` (doc not available)"
    ...

@tpe.deprecated("Deprecated since 0.3.31, will be removed on 0.3.36. Deviating from Tkinter technology.")
class BooleanVar(tk.BooleanVar):
    "\\@since 0.3.26rc1. Value holder for boolean variables. See `tkinter.BooleanVar` (doc not available)"
    ...

@tpe.deprecated("Deprecated since 0.3.31, will be removed on 0.3.36. Deviating from Tkinter technology.")
class Variable(tk.Variable):
    "\\@since 0.3.26rc1. See `tkinter.Variable` (doc not available)"
    ...

@tpe.deprecated("Deprecated since 0.3.31, will be removed on 0.3.36. Deviating from Tkinter technology.")
class FloatVar(tk.DoubleVar):
    "\\@since 0.3.26rc1. Value holder for float variables. See `tkinter.DoubleVar` (doc not available)"
    ...
        
# except (ImportError, ModuleNotFoundError):
#     pass

class ZipFile(zi.ZipFile):
    "\\@since 0.3.26rc2. Class with methods to open, read, write, close, list zip files. See [`zipfile.ZipFile`](https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile)"
    ...

class ZipExtFile(zi.ZipExtFile):
    "\\@since 0.3.26rc2. File-like object for reading an archive member. Returned by `ZipFile.open()`. See [`zipfile.ZipExtFile`](https://docs.python.org/3/library/zipfile.html#zipfile.ZipExtFile)"
    ...

class ZipPath(zi.Path):
    "\\@since 0.3.26rc2. A pathlib-compatible interface for zip files. See [`zipfile.Path`](https://docs.python.org/3/library/zipfile.html#zipfile.Path)"
    ...

StringUnion = Union[_T, str]
"\\@since 0.3.26rc3"
IntegerUnion = Union[_T, int]
"\\@since 0.3.26rc3"
FloatUnion = Union[_T, float]
"\\@since 0.3.26rc3"
ComplexUnion = Union[_T, complex]
"\\@since 0.3.26rc3"
IntegerFloatUnion = Union[_T, int, float]
"\\@since 0.3.26rc3"
IntegerStringUnion = Union[_T, int, str]
"\\@since 0.3.26rc3"
BooleanUnion = Union[_T, bool]
"\\@since 0.3.26rc3"
TrueUnion = Union[_T, Literal[True]]
"\\@since 0.3.26rc3"
FalseUnion = Union[_T, Literal[False]]
"\\@since 0.3.26rc3"
OptionalCallable = Optional[Callable[_P, _T]]
"\\@since 0.3.26rc3. `typing.Optional[typing.Callable[**P, T]]` = `((**P) -> T) | None`"
AnyCallable = Callable[..., Any]
"\\@since 0.3.26rc3. `typing.Callable[..., typing.Any]` = `(...) -> Any`"
OptionalUnion = Optional[Union[_T]]
"\\@since 0.3.26rc3. `typing.Optional[typing.Union[T]]`"

ArgInfo = ins.ArgInfo
"\\@since 0.3.26rc3. See `inspect.ArgInfo` (no doc available)"

Arguments = ins.Arguments
"\\@since 0.3.26rc3. See `inspect.Arguments` (no doc available)"

Attribute = ins.Attribute
"\\@since 0.3.26rc3. See `inspect.Attribute` (no doc available)"

class BlockFinder(ins.BlockFinder):
    """
    \\@since 0.3.26rc3. See `inspect.BlockFinder` (no doc available)
    
    Provide a `tokeneater()` method to detect the end of a code block
    """
    ...

class BoundArguments(ins.BoundArguments):
    """
    \\@since 0.3.26rc3. See [`inspect.BoundArguments`](https://docs.python.org/3/library/inspect.html#inspect.BoundArguments)
    
    Result of `Signature.bind()` call. Holds the mapping of arguments \\
    to the function's parameters
    """
    ...

if sys.version_info >= (3, 12):
    # BufferFlags enum class was introduced for 3.12
    # see https://docs.python.org/3/library/inspect.html#inspect.BufferFlags
    _BufferFlags = ins.BufferFlags
else:
    class _BufferFlags(IntegerFlag):
        SIMPLE = 0x0
        WRITABLE = 0x1
        FORMAT = 0x4
        ND = 0x8
        STRIDES = 0x10 | ND
        C_CONTIGUOUS = 0x20 | STRIDES
        F_CONTIGUOUS = 0x40 | STRIDES
        ANY_CONTIGUOUS = 0x80 | STRIDES
        INDIRECT = 0x100 | STRIDES
        CONTIG = ND | WRITABLE
        CONTIG_RO = ND
        STRIDED = STRIDES | WRITABLE
        STRIDED_RO = STRIDES
        RECORDS = STRIDES | WRITABLE | FORMAT
        RECORDS_RO = STRIDES | FORMAT
        FULL = INDIRECT | WRITABLE | FORMAT
        FULL_RO = INDIRECT | FORMAT
        READ = 0x100
        WRITE = 0x200

BufferFlags = _BufferFlags
"\\@since 0.3.26rc2. See [`inspect.BufferFlags`](https://docs.python.org/3/library/inspect.html#inspect.BufferFlags)"

ByteCode = dis.Bytecode
"\\@since 0.3.26rc3. See [`dis.Bytecode`](https://docs.python.org/3/library/dis.html#dis.Bytecode)"

CodeType = ty.CodeType
"\\@since 0.3.26rc3. See [`types.CodeType`](https://docs.python.org/3/library/types.html#types.CodeType)"

ClosureVar = ins.ClosureVars
"\\@since 0.3.26rc3. See `inspect.ClosureVars` (no doc available)"

class CompletedProcess(sb.CompletedProcess):
    """
    \\@since 0.3.26rc3. See [`subprocess.CompletedProcess`](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess)

    Returned by `subprocess.run()` function
    """
    ...

EOBError = ins.EndOfBlock
"\\@since 0.3.26rc3. See `inspect.EndOfBlock` (no doc available)"

FrameInfo = ins.FrameInfo
"\\@since 0.3.26rc3. See [`inspect.FrameInfo`](https://docs.python.org/3/library/inspect.html#inspect.FrameInfo)"

FullArgSpec = ins.FullArgSpec
"\\@since 0.3.26rc3. See `inspect.FullArgSpec` (no doc available)"

GenericAlias = ty.GenericAlias # not really a class
"""\\@since 0.3.26rc3. See [`types.GenericAlias`](https://docs.python.org/3/library/types.html#types.GenericAlias) \n
Type for parameterized generics
"""

Instruction = dis.Instruction
"\\@since 0.3.26rc3. See [`dis.Instruction`](https://docs.python.org/3/library/dis.html#dis.Instruction)"

Match = re.Match[_T_sb]
"\\@since 0.3.26. See [`re.Match`](https://docs.python.org/3/library/re.html#re.Match)"

ModuleType = ty.ModuleType
"\\@since 0.3.26rc3. See [`types.ModuleType`](https://docs.python.org/3/library/types.html#types.ModuleType)"

class Parameter(ins.Parameter):
    """\\@since 0.3.26rc3. See [`inspect.Parameter`](https://docs.python.org/3/library/inspect.html#inspect.Parameter) \n
    Represent a parameter in a function signature"""
    ...

class Partial(ft.partial):
    "\\@since 0.3.26rc3. See [`functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial)"
    ...

partial = ft.partial
"\\@since 0.3.26. See [`functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial)"

Pattern = re.Pattern[_T_sb]
"\\@since 0.3.26. See [`re.Pattern`](https://docs.python.org/3/library/re.html#re.Pattern)"

class Positions(dis.Positions):
    "\\@since 0.3.26rc3. See [`dis.Positions`](https://docs.python.org/3/library/dis.html#dis.Positions)"
    ...

if sys.version_info >= (3, 7):
    _SafeUUID = uu.SafeUUID
else:
    class _SafeUUID(Enum):
        safe = 0
        unsafe = -1
        unknown = None

SafeUUID = _SafeUUID
"""\\@since 0.3.26rc3. An enumerator class for `is_safe` parameter in `uuid.UUID` constructor \n
See [`uuid.SafeUUID`](https://docs.python.org/3/library/uuid.html#uuid.SafeUUID)"""

class StringFormatter(st.Formatter):
    "\\@since 0.3.26rc3. See [`string.Formatter`](https://docs.python.org/3/library/string.html#string.Formatter)"
    ...

class StringTemplate(st.Template):
    "\\@since 0.3.26rc3. See [`string.Template`](https://docs.python.org/3/library/string.html#string.Template)"
    ...

class TestCase(uni.TestCase):
    "\\@since 0.3.26rc3. See [`unittest.TestCase`](https://docs.python.org/3/library/unittest.html#unittest.TestCase)"
    ...

class TestLoader(uni.TestLoader):
    "\\@since 0.3.26rc3. See [`unittest.TestLoader`](https://docs.python.org/3/library/unittest.html#unittest.TestLoader)"
    ...

class Signature(ins.Signature):
    """
    \\@since 0.3.26rc2. See [`inspect.Signature`](https://docs.python.org/3/library/inspect.html#inspect.Signature)
    
    A `Signature` object represents the overall signature of a function. It stores a `Parameter` object for each \\
    parameter accepted by the function, as well as information specific to the function itself.
    """
    ...

class Timer(tim.Timer):
    "\\@since 0.3.26rc3. See [`timeit.Timer`](https://docs.python.org/3/library/timeit.html#timeit.Timer)"
    ...

class Traceback(ins.Traceback):
    "\\@since 0.3.26rc3. See [`inspect.Traceback`](https://docs.python.org/3/library/inspect.html#inspect.Traceback)"
    ...

TracebackType = ty.TracebackType
"\\@since 0.3.26rc3"

UUID = uu.UUID
"\\@since 0.3.26rc3. See [`uuid.UUID`](https://docs.python.org/3/library/uuid.html#uuid.UUID)"

def overload(f: _T_func): # 0.3.26rc1
    """
    \\@since 0.3.26rc1. See [`typing.overload`](https://docs.python.org/3/library/typing.html#typing.overload)

    A decorator for overloaded functions and methods
    """
    if sys.version_info >= (3, 11):
        from typing import overload as _overload
    else:
        from typing_extensions import overload as _overload
    return _overload(f)
        
def override(m: _T_func): # 0.3.26rc1
    """
    \\@since 0.3.26rc1. See [`typing.override`](https://docs.python.org/3/library/typing.html#typing.override)

    A decorator for creating methods to override by subclasses \\
    of their class parents
    """
    try:
        m.__override__ = True
    except (AttributeError, TypeError):
        # Skip the attribute silently if it is not writable.
        # AttributeError happens if the object has __slots__ or a
        # read-only property, TypeError if it's a builtin class.
        pass
    return m

def getArgs(t):
    """
    \\@since 0.3.26rc1

    See [`typing.get_args`](https://docs.python.org/3/library/typing.html#typing.get_args)
    """
    if sys.version_info >= (3, 8):
        return tp.get_args(t)
    else:
        return tpe.get_args(t)

    
def coroutine(f: _CoroutineLike[_P, _T]):
    """
    \\@since 0.3.26rc1

    This function converts regular generator function to a coroutine.
    """
    return ty.coroutine(f)



class abstractproperty(property):
    """
    \\@since 0.3.26rc1

    A decorator class for abstract properties.

    Equivalent invoking decorators `tense.types_collection.abstract` and in-built `property`.
    """
    __isabstractmethod__ = True

class abstractstaticmethod(staticmethod):
    """
    \\@since 0.3.26rc1

    A decorator class for abstract static methods.

    Equivalent invoking decorators `tense.types_collection.abstract` and in-built `staticmethod`.
    """
    __isabstractmethod__ = True
    def __init__(self, f: Callable[_P, _T_cov]):
        f.__isabstractmethod__ = True
        super().__init__(f)

class abstractclassmethod(classmethod):
    """
    \\@since 0.3.26rc1

    A decorator class for abstract class methods.

    Equivalent invoking decorators `tense.types_collection.abstract` and in-built `classmethod`.
    """
    __isabstractmethod__ = True
    def __init__(self, f: Callable[Concatenate[type[_T], _P], _T_cov]):
        f.__isabstractmethod__ = True
        super().__init__(f)

def noTypeCheck(f: _T_func): # 0.3.26rc1
    "\\@since 0.3.26rc1"
    return tp.no_type_check(f)

def noTypeCheckDecorator(d: _DecoratorLike[_P, _T]): # 0.3.26rc1
    "\\@since 0.3.26rc1"
    return tp.no_type_check_decorator(d)

def newClass(name: str, bases: abc2.Iterable[object] = (), keywords: Optional[dict[str, Any]] = None, execBody: Optional[Callable[[str, Any], object]] = None): # 0.3.26rc3
    """
    \\@since 0.3.26rc3

    Create a class object dynamically using the appropriate metaclass
    """
    from types import new_class
    return new_class(name, bases, keywords, execBody)

del abc2, ins, sb, tk, zi, enum, ty, tp, tpe, st, ft, tim, uu, uni, re # not for export