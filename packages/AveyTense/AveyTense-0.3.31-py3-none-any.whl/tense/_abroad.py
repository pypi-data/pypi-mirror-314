"""
**Tense Nennai Types** \n
\\@since 0.3.29 \\
© 2023-Present Aveyzan // License: MIT
```ts
module tense._abroad
```
This internal module has been established to extend possibilities of `abroad()` \\
function and its variations.
"""

from . import _primal_types as _pt
from ._abc import Iterable as _Iterable

__module__ = "tense"
_var = _pt.TypeVar

_T = _var("_T")

class _AbroadUnknownInitializer(_pt.Generic[_T]):
    """\\@since 0.3.29"""
    
    def __init__(self, seq: _Iterable[_T], v1: int, v2: int, m: int, /):
        
        self.__l = list(seq)
        self.__p = (v1, v2, m)
        
    def __iter__(self):
        
        return iter(self.__l)
    
    def __str__(self):
        
        if len(self.__l) == 0:
            return "abroad(<Empty>)"
        
        else:
            _1 = str(self.__p[0])
            _2 = str(self.__p[1])
            _3 = str(self.__p[2])
            return "abroad({})".format(", ".join([_1, _2, _3]))
            
    def __repr__(self):
        
        return "<{}.{} object: {}>".format(__module__, type(self).__name__, self.__str__())
    
    def __pos__(self):
        """
        \\@since 0.3.28
        
        Returns sequence as a list. `+` can be claimed as "allow to change any items, this sequence can be updated"
        """
        return self.__l
    
    def __neg__(self):
        """
        \\@since 0.3.28
        
        Returns sequence as a tuple. `-` can be claimed as "do not change any items, this sequence cannot be updated"
        """
        return tuple(self.__l)
    
    def __invert__(self):
        """
        \\@since 0.3.28
        
        Returns sequence as a set. `~` can be claimed as "allow to change any items, this sequence can be updated, BUT items must be unique"
        """
        return set(self.__l)
    
    def __getitem__(self, key: int):
        """
        \\@since 0.3.29
        
        """
        try:
            return self.__l[key]
        
        except IndexError:
            error = IndexError("sequence out of range")
            raise error
       
    @property
    def params(self):
        """
        \\@since 0.3.29
        
        Returns parameters as integers
        """
        return self.__p
    
    @params.getter
    def params(self):
        return self.__p
    
    @params.deleter
    def params(self):
        error = TypeError("cannot delete property 'params'")
        raise error
    
    @params.setter
    def params(self, value):
        error = TypeError("cannot set new value to property 'params'")
        raise error
    
class AbroadInitializer(_AbroadUnknownInitializer[int]): ... # since 0.3.28
class AbroadStringInitializer(_AbroadUnknownInitializer[str]): ... # since 0.3.29
class AbroadFloatyInitializer(_AbroadUnknownInitializer[float]): ... # since 0.3.29