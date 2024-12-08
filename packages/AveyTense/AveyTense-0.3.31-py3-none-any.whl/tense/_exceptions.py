"""
**Tense Exceptions**

\\@since 0.3.27a1 \\
© 2024-Present Aveyzan // License: MIT
```ts
module tense._exceptions
```
Exception classes for TensePy
"""
class MissingValueError(Exception):
    """
    \\@since 0.3.19
    ```
    in module tense.types_collection
    # 0.3.26b3 - 0.3.26c3 in module tense.tcs
    # to 0.3.26b3 in module tense.primary
    ```
    Missing value (empty parameter)
    """
    ...
class IncorrectValueError(Exception):
    """
    \\@since 0.3.19
    ```
    in module tense.types_collection
    # 0.3.26b3 - 0.3.26c3 in module tense.tcs
    # to 0.3.26b3 in module tense.primary
    ```
    Incorrect value of a parameter, having correct type
    """
    ...
class NotInitializedError(Exception):
    """
    \\@since 0.3.25
    ```
    in module tense.types_collection
    # 0.3.26b3 - 0.3.26c3 in module tense.tcs
    # to 0.3.26b3 in module tense.primary
    ```
    Class was not instantiated
    """
    ...
class InitializedError(Exception):
    """
    \\@since 0.3.26b3
    ```
    in module tense.types_collection
    ```
    Class was instantiated
    """
    ...
class NotReassignableError(Exception):
    """
    \\@since 0.3.26b3
    ```
    in module tense.types_collection
    ```
    Attempt to re-assign a value
    """
    ...
class NotComparableError(Exception):
    """
    \\@since 0.3.26rc1
    ```
    in module tense.types_collection
    ```
    Attempt to compare a value with another one
    """
    ...
class NotIterableError(Exception):
    """
    \\@since 0.3.26rc1
    ```
    in module tense.types_collection
    ```
    Attempt to iterate
    """
    ...
class NotInvocableError(Exception):
    """
    \\@since 0.3.26rc1
    ```
    in module tense.types_collection
    ```
    Attempt to call an object
    """
    ...
    
class SubclassedError(Exception):
    """
    \\@since 0.3.27rc1
    ```
    in module tense.types_collection
    ```
    Class has been inherited by the other class
    """
    ...

class ErrorHandler:
    """
    \\@since 0.3.26rc1
    ```
    in module tense.types_collection
    ```
    Internal class for error handling. Does not exist at runtime

    - `100` - cannot modify a final variable (`any`)
    - `101` - cannot use comparison operators on type which doesn't support them + ...
    - `102` - cannot assign a new value or re-assign a value with any of augmented \\
    assignment operators on type which doesn't support them + ...
    - `103` - object is not iterable (`any`)
    - `104` - attempt to initialize an abstract class + ...
    - `105` - class (`any`) was not initialized
    - `106` - could not compare types - at least one of them does not support comparison \\
    operators
    - `107` - object cannot be called
    - `108` - object cannot use any of unary operators: '+', '-', '~', cannot be called nor be value \\
    of `abs()` in-built function
    - `109` - object cannot use unary +|- operator
    - `110` - object cannot use bitwise NOT operator '~'
    - `111` - this file is not for compiling, moreover, this file does not have a complete \\
    Tense declarations collection. Consider importing module `tense` instead
    - any other - unknown error occured
    """
    def __new__(cls, code: int, *args: str):
        _arg0 = "" if len(args) == 0 else args[0]
        _arg1 = "" if len(args) == 1 else args[1]
        if code == 100:
            _error = (NotReassignableError, "cannot modify a final variable '{}'".format(_arg0) if _arg0 not in (None, "") else "cannot modify a final variable")
        elif code == 101:
            _error = (NotComparableError, "cannot use comparison operators on type which doesn't support them" + _arg0)
        elif code == 102:
            _error = (NotReassignableError, "cannot assign a new value or re-assign" + _arg0)
        elif code == 103:
            _error = (NotIterableError, "object is not iterable ('{}')".format(_arg0) if _arg0 not in (None, "") else "cannot modify a final variable")
        elif code == 104:
            _error = (InitializedError, "attempt to initialize an abstract class " + _arg0)
        elif code == 105:
            _error = (NotInitializedError, "class '{}' was not initalized".format(_arg0))
        elif code == 106:
            _error = (NotComparableError, "could not compare types - at least one of them does not support comparison operators")
        elif code == 107:
            _error = (NotInvocableError, f"class {_arg0} cannot be called")
        elif code == 108:
            _error = (TypeError, "object cannot use any of unary operators: '+', '-', '~', cannot be called nor be value of abs() in-built function")
        elif code == 109:
            _error = (TypeError, "object cannot use unary '{}' operator".format(_arg0))
        elif code == 110:
            _error = (TypeError, "object cannot use bitwise NOT operator '~'")
        elif code == 111:
            _error = (RuntimeError, "this file is not for compiling, moreover, this file does not have a complete TensePy declarations collection. Consider importing module 'tense' instead.")
        elif code == 112:
            _error = (AttributeError, "cannot modify a final attribute {}".format(_arg0))
        elif code == 113:
            _error = (SubclassedError, "attempt to subclass a final class {}".format(_arg0))
        elif code == 114:
            _error = (TypeError, "{} cannot be used on {}".format(_arg0, _arg1))
        elif code == 115:
            _error = (TypeError, "cannot inspect because class {} is abstract".format(_arg0))
        elif code == 116:
            _error = (TypeError, "cannot inspect because class {} is final".format(_arg0))
        elif code == 117:
            _error = (AttributeError, "attempt to delete item {}".format(_arg0))
        elif code == 118:
            _error = (AttributeError, "attempt to reassign item {}".format(_arg0))
        elif code == 119:
            _error = (AttributeError, "cannot modify any fields in class {}".format(_arg0))
        elif code == 120:
            _error = (TypeError, "cannot recast method {}".format(_arg0))
        elif code == 121:
            _error = (TypeError, "cannot modify field {} with operator {}".format(_arg0, _arg1))
        else:
            _error = (RuntimeError, "unknown error occured")
        error = _error[0](_error[1])
        raise error
