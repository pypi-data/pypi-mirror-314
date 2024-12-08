"""
**Tense Fencord Types** \n
\\@since 0.3.26rc3 \\
© 2023-Present Aveyzan // License: MIT
```ts
module tense.fencord._types
```
Types wrapper for TensePy Fencord.
"""

from __future__ import annotations
import sys

if sys.version_info < (3, 9):
    err, s = (RuntimeError, "Not allowed to import this module when having Python version least than 3.9.")
    raise err(s)

import subprocess as sb

try:
    import discord as dc
except (NameError, ModuleNotFoundError, ImportError):
    sb.run([sys.executable, "-m", "pip", "install", "discord"])

import discord as dc, typing as tp, datetime as dt
from .. import types_collection as tc

abc = dc.abc
"\\@since 0.3.27a1"
ap = dc.app_commands
"\\@since 0.3.27a1"
apc = dc.app_commands.commands
"\\@since 0.3.27a1"
trf = dc.app_commands.transformers
"\\@since 0.3.27a1"
trs = dc.app_commands.translator
"\\@since 0.3.27a1"
ui = dc.ui
"\\@since 0.3.27a1"
uti = dc.utils
"\\@since 0.3.27a1"
datetime = dt.datetime
"\\@since 0.3.27a1"

_var = tc.TypeVar
_par = tc.ParamSpec

if tp.TYPE_CHECKING:
    T_client = _var("T_client", bound = dc.Client, covariant = True, default = dc.Client)
else:
    T_client = _var("T_client", bound = dc.Client, covariant = True)

_P = _par("_P")
_T = _var("_T")
_L = _var("_L", bound = trs.TranslationContextLocation)
"\\@since 0.3.27a1"
MISSING = dc.abc.MISSING
"\\@since 0.3.26rc3"

T_coroutine = _var("T_coroutine", bound = tc.Callable[..., tc.Coroutine[tc.Any, tc.Any, list[ap.AppCommand]]])
"""
Bound to `(...) -> Coroutine[Any, Any, discord.app_commands.AppCommand]`. \\
Required for `Fencord.event()` decorator. Equivalent to Discord.py's `CoroT`
"""

del tp, dc, tc, dt # not for export