"""
**Tense Operators** \n
\\@since 0.3.27a3 \\
© 2023-Present Aveyzan // License: MIT
```
module tense.operators
```
Functions handling operations. Extension of standard `operator` library. \\
It does not import anything else, like submodules of TensePy. Preferred \\
import method: `import tense.operators as operators`
"""

from operator import *

def tdiv(x, y): return x / y
def fdiv(x, y): return x // y
def mmul(x, y): return x @ y
def band(x, y): return x & y
def bor(x, y): return x | y
def bxor(x, y): return x ^ y
def bleft(x, y): return x << y
def bright(x, y): return x >> y

def isNot(x, y): return x is not y
def in_(x, y): return x in y
def isNotIn(x, y): return x not in y
def land(x, y): return x and y
def lor(x, y): return x or y
def lxor(x, y): return x and not y
def isNone(x): return x is None
def isNotNone(x): return x is not None
def isEllipsis(x): return x is ...
def isNotEllipsis(x): return x is not ...
def isTrue(x): return x is True
def isFalse(x): return x is False

def setitem(x, y, v): x[y] = v

__all__ = sorted([n for n in globals()])
"\\@since 0.3.27a3. Every declaration in module `tense.operators`, including dunder-named ones"