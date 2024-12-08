"""
**Tense Databases** \n
\\@since 0.3.27a4 \\
© 2023-Present Aveyzan // License: MIT
```
module tense.databases
```
Connection with SQL. *Experimental*: not recommended to use it yet.
"""

from tense import *
from . import types_collection as tc

# toggle once tests are done
# missing 2 php files to do operations on
if False:
    class _TenseSQLDataTypes(tc.Enum):
        "\\@since 0.3.27a4. Internal auxiliary enumerator class containing every date type possible to assign to columns"
        TINYINT = 0
        SMALLINT = 1
        MEDIUMINT = 2
        INT = 3
        INTEGER = 4
        BIGINT = 5
        TINYINT_UNSIGNED = 10
        SMALLINT_UNSIGNED = 11
        MEDIUMINT_UNSIGNED = 12
        INT_UNSIGNED = 13
        INTEGER_UNSIGNED = 14
        BIGINT_UNSIGNED = 15
        BOOL = 20
        BOOLEAN = 21
        DECIMAL = 30
        DEC = 31
        NUMERIC = 32
        FIXED = 33
        FLOAT = 35
        DOUBLE = 36
        DATE = 40
        DATETIME = 41
        TIMESTAMP = 42
        TIME = 43
        YEAR = 44
        CHAR = 50
        VARCHAR = 51
        BINARY = 55
        VARBINARY = 56
        TINYBLOB = 60
        BLOB = 61
        MEDIUMBLOB = 62
        LONGBLOB = 63
        TINYTEXT = 65
        TEXT = 66
        MEDIUMTEXT = 67
        LONGTEXT = 68
        ENUM = 70
        SET = 71

    class KeyType(tc.Enum):
        "\\@since 0.3.27b3"
        NO_KEY = -1
        KEY = 0
        FOREIGN = 1
        PRIMARY = 2

    def _options_checker(unsigned: bool = False, zerofill: bool = False, null: bool = False, autoIncrement: bool = False, key: KeyType = KeyType.NO_KEY):
        v = ""
        if unsigned is True: v += " UNSIGNED"
        if zerofill is True: v += " ZEROFILL"
        if null is True: v += " NULL"
        else: v += " NOT NULL"
        if autoIncrement is True: v += " AUTO_INCREMENT"
        if key == KeyType.KEY: v += " KEY"
        elif key == KeyType.FOREIGN: v += " FOREIGN KEY"
        elif key == KeyType.PRIMARY: v += " PRIMARY KEY"
        return v

    class TINYINT:
        """
        \\@since 0.3.27b3

        Equivalent to MySQL data type `TINYINT`.
        """
        __v = ""

        def __init__(self, v: int = ..., /, unsigned: bool = False, zerofill: bool = False, null: bool = False, autoIncrement: bool = False, key: KeyType = KeyType.NO_KEY):
            err, s = (TypeError, "Expected integer value in range 1-255")
            self.__v = "TINYINT"
            if Tense.isInteger(v):
                if v in abroad(1, 0x100):
                    self.__v += f"({v})"
                else:
                    raise err(s)
            else:
                raise err(s)
            self.__v += _options_checker(unsigned = unsigned, zerofill = zerofill, null = null, autoIncrement = autoIncrement, key = key)

        def get(self):
            return self.__v

    class SMALLINT:
        """
        \\@since 0.3.27b3

        Equivalent to MySQL data type `SMALLINT`.
        """
        __v = ""

        def __init__(self, v: int = ..., /, unsigned: bool = False, zerofill: bool = False, null: bool = False, autoIncrement: bool = False, key: KeyType = KeyType.NO_KEY):
            err, s = (TypeError, "Expected integer value in range 1-255")
            self.__v = "SMALLINT"
            if Tense.isInteger(v):
                if v in abroad(1, 0x100):
                    self.__v += f"({v})"
                else:
                    raise err(s)
            else:
                raise err(s)
            self.__v += _options_checker(unsigned = unsigned, zerofill = zerofill, null = null, autoIncrement = autoIncrement, key = key)

        def get(self):
            return self.__v

    class MEDIUMINT:
        """
        \\@since 0.3.27b3

        Equivalent to MySQL data type `MEDIUMINT`.
        """
        __v = ""

        def __init__(self, v: int = ..., /, unsigned: bool = False, zerofill: bool = False, null: bool = False, autoIncrement: bool = False, key: KeyType = KeyType.NO_KEY):
            err, s = (TypeError, "Expected integer value in range 1-255")
            self.__v = "MEDIUMINT"
            if Tense.isInteger(v):
                if v in abroad(1, 0x100):
                    self.__v += f"({v})"
                else:
                    raise err(s)
            else:
                raise err(s)
            self.__v += _options_checker(unsigned = unsigned, zerofill = zerofill, null = null, autoIncrement = autoIncrement, key = key)

        def get(self):
            return self.__v

    class INT:
        """
        \\@since 0.3.27b3

        Equivalent to MySQL data type `INT`.
        """
        __v = ""

        def __init__(self, v: int = ..., /, unsigned: bool = False, zerofill: bool = False, null: bool = False, autoIncrement: bool = False, key: KeyType = KeyType.NO_KEY):
            err, s = (TypeError, "Expected integer value in range 1-255")
            self.__v = "INT"
            if Tense.isInteger(v):
                if v in abroad(1, 0x100):
                    self.__v += f"({v})"
                else:
                    raise err(s)
            else:
                raise err(s)
            self.__v += _options_checker(unsigned = unsigned, zerofill = zerofill, null = null, autoIncrement = autoIncrement, key = key)

        def get(self):
            return self.__v

    INTEGER = INT

    _DataType = tc.Union[
        TINYINT,
        SMALLINT,
        MEDIUMINT,
        INT
    ]

    def _error_message(code: int, v: tc.Optional[str]):
        if code == 100:
            return f"String in parameter '{v}' may only contain letters a-z, A-Z and digits 0-9."
        elif code == 101:
            return f"Expected string or None in parameter '{v}'"
        elif code == 102:
            return f"Expected integer or None in parameter '{v}'"
        elif code == 103:
            return f"Expected parameter '{v}' have positive integer value"
        else:
            return f"{v}"


    class TenseSQL:
        """
        \\@since 0.3.27a4
        ```
        in module tense.databases
        ```
        Class for SQL (Structured Query Language)
        """
        from . import types_collection as __tc
        import inspect as __ins, re as __re
        INDENT = "    " # 4 spaces
        __hostname = None
        __username = None
        __password = None
        __database = None
        __port = None
        __socket = None
        __tables = None
        __php_code = [
            "// This code was auto-generated by invocation of Python function 'TenseSQL.generate()'", # 0, line 0
            "// Go to file 'tsdbmanage.php' for further manipulations", # 1, line 1
            "// © 2023-Present Aveyzan // License: MIT", # 2, line 2
            "", # 3, line 3
            "", # 4, line 4
        ]
        def __init__(
            # reference: see PHP mysqli class constructor
            self, 
            hostname: __tc.Optional[str] = None, 
            username: __tc.Optional[str] = None, 
            password: __tc.Optional[str] = None, 
            database: __tc.Optional[str] = None, 
            port: __tc.Optional[int] = None, 
            socket: __tc.Optional[str] = None,
            /
        ):
            self.__php_code.clear()
            a = ("hostname", "username", "password", "database", "socket")
            i = 0
            for p in (hostname, username, password, database, socket):
                if not Tense.isString(p) and not Tense.isNone(p):
                    err, s = (TypeError, _error_message(101, a[i]))
                    raise err(s)
                i += 1
            if not Tense.isInteger(port) and not Tense.isNone(port):
                err, s = (TypeError, _error_message(102, "port"))
                raise err(s)
            elif port < 0:
                err, s = (ValueError, _error_message(103, "port"))
                raise err(s)
            i = 0
            for p in (hostname, username, password, database, socket):
                if Tense.isString(p):
                    # to ensure there won't be e.g. SQL injection, there is restricted range of characters supported
                    if self.__re.match(r"[^0-9a-zA-Z]", p):
                        err, s = (ValueError, _error_message(100, a[i]))
                        raise err(s)
                i += 1
            self.__hostname = hostname
            self.__username = username
            self.__password = password
            self.__database = database
            self.__port = port
            self.__socket = socket
            for p in (self.__hostname, self.__username, self.__password, self.__database, self.__port, self.__socket):
                if Tense.isString(p) and reckon(p) > 0:
                    self.__php_code.append(f"$_DATABASE_COMPONENTS[] = \"{p}\";")
                elif Tense.isInteger(p):
                    self.__php_code.append(f"$_DATABASE_COMPONENTS[] = {p};")
            self.__php_code.append("")
            if self.__hostname is None:
                self.__php_code.append("$connect = mysqli_connect();")
            else:
                self.__php_code.append("$connect = new mysqli(")
                i = 0
                for p in (self.__hostname, self.__username, self.__password, self.__database, self.__port, self.__socket):
                    if not Tense.isNone(p):
                        self.__php_code.append(self.INDENT + f"$_DATABASE_COMPONENTS[{i}],")
                    else:
                        break
                    i += 1
                # removing the last comma from the last parameter
                # its important because PHP throws an error in this case
                self.__php_code[-1] = self.__re.sub(r"],\s*$", "]", self.__php_code[-1])
                self.__php_code.append(f");")
                self.__php_code.append("if($connect->connect_error) die(\"Cannot connect to the database\");")
                self.__php_code.append("")
        
        def createTable(self, name: str, /, *columns: tuple[str, _DataType]): ...
            
    del tc
