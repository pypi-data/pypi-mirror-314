"""
**Tense Fencord** \n
\\@since 0.3.24 \\
\\@modified 0.3.25 \\
© 2023-Present Aveyzan // License: MIT
```ts
module tense.fencord
```
Since 0.3.25 this module is called `tense.fencord` instead of `tense.core`. \\
Import this module only, if:
- you have Python 3.9 or above
- you have discord.py via `pip install discord`

This Tense module features `Fencord` class.
"""
import sys

if sys.version_info < (3, 9):
    err, s = (RuntimeError, "Not allowed to import this module when having Python version least than 3.9.")
    raise err(s)

import subprocess as sb

try:
    import discord as dc
except (NameError, ModuleNotFoundError, ImportError):
    sb.run([sys.executable, "-m", "pip", "install", "discord"])

import re, warnings as wa, inspect as ins, collections as ct
from tense import *
from .. import types_collection as tc
from . import _types as dct
import discord as dc

# between @since and @author there is unnecessarily long line spacing
# hence this warning is being thrown; it is being disabled.
wa.filterwarnings("ignore", category = SyntaxWarning)

_var = tc.TypeVar
# _spec = tc.SpecVar

_cm = classmethod
_sm = staticmethod
_p = property

_T = _var("_T")
# _P = _spec("_P")

_LocaleString = dc.app_commands.translator.locale_str
"\\@since 0.3.27a4"

class LocaleString:
    "\\@since 0.3.26rc3; class since 0.3.27a1. Since 0.3.27a4 in module `tense.fencord`"
    from .. import types_collection as __tc
    def __new__(cls, message: str, /, **extras: __tc.Any):
        return _LocaleString(message, kwargs = extras)

if False: # experiments since 0.3.27
    class Servers:
        """
        \\@since 0.3.27a4
        ```
        in module tense.fencord
        ```
        Alternative type for `servers` parameter in `Fencord.slashCommand()` callback
        """
        import discord as __dc
        from .. import types_collection as __tc
        __objs = None

        def __init__(self, *ids: int):
            if reckon(ids) == 0:
                err, s = (ValueError, "Expected at least one integer value")
                raise err(s)
            a = [self.__dc.Object(ids[0], type = self.__dc.Guild)]
            a.clear()
            for e in ids:
                # haven't tested yet! this has to affirm that id refers to a guild/server
                # if self.__dc.Object(e).type != self.__dc.Guild:
                #    err, s = (ValueError, f"Invalid Discord guild/server ID: '{e}'")
                #    raise err(s)
                if not Tense.isInteger(e):
                    err, s = (TypeError, "Expected every value to be integers")
                    raise err(s)
                else:
                    a.append(self.__dc.Object(e, type = self.__dc.Guild))
            self.__objs = a
        
        @_p
        def list(self): # marking the returned type isn't actually necessary. 'Object' instances have 'id' attribute
            """
            \\@since 0.3.27a4
            ```
            "property" in class Servers
            ```
            Only used in `Fencord.slashCommand()` for `servers` parameter. \\
            In overall you shouldn't use this property. It returns list of \\
            `discord.Object` class instances.
            """
            if Tense.isNone(self.__objs):
                err, s = (self.__tc.NotInitializedError, "Class wasn't initialized")
                raise err(s)
            return self.__objs
                
    Guilds = Servers # since 0.3.27a4

_SlashCommandServers = tc.Union[tc.Sequence[_T], _T, None] # since 0.3.25
_EmbedType = tc.Literal['rich', 'image', 'video', 'gifv', 'article', 'link'] # since 0.3.26


class _FontStyles(tc.Enum):
    """
    \\@since 0.3.27
    
    Internal class for font styles of discord
    """
    
    ### 1x
    # Non-mixed styles
    NORMAL = 0
    BOLD = 1
    ITALIC = 2
    UNDERLINE = 3
    STRIKE = 4
    CODE = 5
    BIG = 6
    MEDIUM = 7
    SMALL = 8
    SMALLER = 9
    QUOTE = 10
    SPOILER = 11
    URL = 12
    SILENT = 13
    
    if False: # leave for later (0.3.27)
        ### 2x
        # usually to prevent more parameters
        BOLD_ITALIC = 20
        BOLD_UNDERLINE = 21
        BOLD_STRIKE = 22
        BOLD_CODE = 23
        BOLD_SMALLER = 24
        BOLD_QUOTE = 25
        BOLD_SPOILER = 26
        BOLD_URL = 27
        BOLD_SILENT = 28
        
        ITALIC_UNDERLINE = 30
        ITALIC_STRIKE = 31
        ITALIC_CODE = 32
        ITALIC_BIG = 33
        ITALIC_MEDIUM = 34
        ITALIC_SMALL = 35
        ITALIC_SMALLER = 36
        ITALIC_QUOTE = 37
        ITALIC_SPOILER = 38
        ITALIC_URL = 39
        ITALIC_SILENT = 40
        
        UNDERLINE_STRIKE = 45
        UNDERLINE_CODE = 46
        UNDERLINE_BIG = 47
        UNDERLINE_MEDIUM = 48
        UNDERLINE_SMALL = 49
        UNDERLINE_SMALLER = 50
        UNDERLINE_QUOTE = 51
        UNDERLINE_SPOILER = 52
        UNDERLINE_URL = 53
        UNDERLINE_SILENT = 54
        
        STRIKE_CODE = 60
        STRIKE_BIG = 61
        STRIKE_MEDIUM = 62
        STRIKE_SMALL = 63
        STRIKE_SMALLER = 64
        STRIKE_QUOTE = 65
        STRIKE_SPOILER = 66
        STRIKE_URL = 67
        STRIKE_SILENT = 68
        
        CODE_BIG = 70
        CODE_SMALL = 71
        CODE_SMALLER = 72
        CODE_QUOTE = 73
        CODE_SPOILER = 74
        CODE_URL = 75
        CODE_SILENT = 76
        
        BIG_QUOTE = 80
        BIG_SPOILER = 81
        BIG_URL = 82
        BIG_SILENT = 83
        
        MEDIUM_QUOTE = 90
        MEDIUM_SPOILER = 91
        MEDIUM_URL = 92
        MEDIUM_SILENT = 93
        
        SMALL_QUOTE = 100
        SMALL_SPOILER = 101
        SMALL_URL = 102
        SMALL_SILENT = 103
        
        SMALLER_QUOTE = 110
        SMALLER_SPOILER = 111
        SMALLER_URL = 112
        SMALLER_SILENT = 113
        
        QUOTE_SPOILER = 120
        QUOTE_URL = 121
        QUOTE_SILENT = 122
        
        SPOILER_URL = 125
        SPOILER_SILENT = 126
        
        URL_SILENT = 129
        
        # duplicates
        ITALIC_BOLD = BOLD_ITALIC
        UNDERLINE_BOLD = BOLD_UNDERLINE
        UNDERLINE_ITALIC = ITALIC_UNDERLINE
        STRIKE_BOLD = BOLD_STRIKE
        STRIKE_ITALIC = ITALIC_STRIKE
        STRIKE_UNDERLINE = UNDERLINE_STRIKE
        CODE_BOLD = BOLD_CODE
        CODE_ITALIC = ITALIC_CODE
        CODE_UNDERLINE = UNDERLINE_CODE
        CODE_STRIKE = STRIKE_CODE
    

class FontStyler:
    """
    \\@since 0.3.27a1
    ```
    in module tense.fencord
    ```
    Proving font styles from Discord
    """
    from .. import types_collection as __tc
    
    NORMAL = _FontStyles.NORMAL
    BOLD = _FontStyles.BOLD
    ITALIC = _FontStyles.ITALIC
    UNDERLINE = _FontStyles.UNDERLINE
    STRIKE = _FontStyles.STRIKE
    CODE = _FontStyles.CODE
    BIG = _FontStyles.BIG
    MEDIUM = _FontStyles.MEDIUM
    SMALL = _FontStyles.SMALL
    SMALLER = _FontStyles.SMALLER
    QUOTE = _FontStyles.QUOTE
    SPOILER = _FontStyles.SPOILER
    URL = _FontStyles.URL
    SILENT = _FontStyles.SILENT
    
    __mode = None
    __text = ""
    
    def __init__(self, text: tc.Union[str, tc.StringConvertible], style: _FontStyles = _FontStyles.NORMAL, value: tc.Optional[str] = None, visible: bool = True, /):
        """
        \\@since 0.3.27
        
        Append entry text along with styling
        """
        _text = str(text) if not isinstance(text, str) else text
        
        if reckon(_text) == 0:
            err, s = (ValueError, "expected a non-empty string in parameter 'text'")
            raise err(s)
        
        if style == self.NORMAL:
            self.__text = _text
            
        elif style == self.BOLD:
            self.__text = "**{}**".format(_text)
            
        elif style == self.ITALIC:
            self.__text = "*{}*".format(_text)
            
        elif style == self.UNDERLINE:
            self.__text = "__{}__".format(_text)
            
        elif style == self.STRIKE:
            self.__text = "~~{}~~".format(_text)
            
        elif style == self.CODE:
            if not Tense.isNone(value):
                self.__text = """```{}
                {}
                ```""".format(value, _text)
            else:
                self.__text = "`{}`".format(_text)
                
        elif style == self.BIG:
            self.__text = "# {}".format(_text)
            
        elif style == self.MEDIUM:
            self.__text = "## {}".format(_text)
            
        elif style == self.SMALL:
            self.__text = "### {}".format(_text)
            
        elif style == self.SMALLER:
            self.__text = "-# {}".format(_text)
            
        elif style == self.QUOTE:
            self.__text = "> {}".format(_text)
            
        elif style == self.SPOILER:
            self.__text = "||{}||".format(_text)
            
        elif style == self.URL:
            if not Tense.isNone(value):
                self.__text = "[{}]({})".format(value, _text) if visible else "[{}](<{}>)".format(value, _text)
            else:
                err, s = (ValueError, "expected a link in a string in parameter 'value'")
                
        elif style == self.SILENT:
            self.__text = "@silent {}".format(_text)
            
        else:
            err, s = (TypeError, "expected a valid font style")
            raise err(s)
        
    def __str__(self):
        """
        \\@since 0.3.27
        
        Return styled string
        """
        return self.__text
    
    @_sm
    def bold(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text bold
        """
        return f"**{text}**"
    @_sm
    def italic(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text italic
        """
        return f"*{text}*"
    @_sm
    def underline(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text underlined
        """
        return f"__{text}__"
    @_sm
    def code(text: str, language: __tc.Optional[str] = None, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: coded text
        """
        if language is None:
            return f"`{text}`"
        else:
            return f"```{language}\n{text}\n```"
    @_sm
    def big(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text big
        """
        return f"# {text}"
    @_sm
    def medium(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text medium
        """
        return f"## {text}"
    @_sm
    def small(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text small
        """
        return f"### {text}"
    @_sm
    def smaller(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text smaller
        """
        return f"-# {text}"
    @_sm
    def quote(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: transform text to quote
        """
        return f"> {text}"
    @_sm
    def spoiler(text: str, /):
        """
        \\@since 0.3.25
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text spoiled
        """
        return f"||{text}||"
    @_sm
    def textUrl(text: str, url: str, hideEmbed = True):
        """
        \\@since 0.3.26a2
        ```
        "class method" in class FontStyles
        ```
        On Discord: make text become hyperlink, leading to specified URL
        """
        return f"[{text}](<{url}>)" if hideEmbed else f"[{text}]({url})"
    @_sm
    def silent(text: str):
        """
        \\@since 0.3.26a3
        ```
        "class method" in class FontStyles
        ```
        Make a message silent. Usable for Direct Messages. \\
        As a tip, refer `@silent` as `> ` (quote), and message \\
        MUST be prefixed with `@silent`.
        """
        return f"@silent {text}"

class Fencord:
    """
    Fencord
    +++++++
    \\@since 0.3.24 (before 0.3.25 as `DC`)
    ```
    in module tense.fencord
    ```
    Providing methods to help integrating with Discord.

    During 0.3.24 - 0.3.26 this class was final. Since 0.3.27a1 \\
    this class can be subclassed
    """
    from .. import types_collection as __tc
    from . import _types as __dct
    import discord.app_commands as __app, discord as __dc
    
    __commandtree = None
    __client = None
    __intents = None
    __synccorountine = None
    
    @_p
    def user(self):
        """
        \\@since 0.3.25
        ```
        "property" in class Fencord
        ```
        Returns user of this client. The `None` type is deduced \\
        only if class wasn't initialized.
        """
        return self.__client.user
    
    @_p
    def servers(self):
        """
        \\@since 0.3.25
        ```
        "property" in class Fencord
        ```
        Returns servers/guilds tuple in which client is
        """
        return tuple([x for x in self.__client.guilds])

    if False: # removed 0.3.27
        @_p
        @__tc.deprecated("Deprecated since 0.3.27a2, consider using 'Fencord.client' property instead")
        def getClient(self):
            """
            \\@since 0.3.25 \\
            \\@deprecated 0.3.27a2
            ```
            "property" in class Fencord
            ```
            Returns reference to `Client` instance inside the class. \\
            The `None` type is deduced only if class wasn't initialized.
            """
            return self.__client
    @_p
    def client(self):
        """
        \\@since 0.3.27a2
        ```
        "property" in class Fencord
        ```
        Returns reference to `Client` instance inside the class. \\
        The `None` type is deduced only if class wasn't initialized.
        """
        return self.__client
    
    if False: # removed 0.3.27
        @_p
        @__tc.deprecated("Deprecated since 0.3.27a2, consider using 'Fencord.tree' property instead")
        def getTree(self):
            """
            \\@since 0.3.25 \\
            \\@deprecated 0.3.27a2
            ```
            "property" in class Fencord
            ```
            Returns reference to `CommandTree` instance inside the class.

            This might be needed to invoke decorator `CommandTree.command()` \\
            for slash/application commands, and `CommandTree.sync()` method \\
            in `on_ready()` event. `None` is returned only whether class wasn't \\
            initialized.
            """
            return self.__commandtree
    @_p
    def tree(self):
        """
        \\@since 0.3.27a2
        ```
        "property" in class Fencord
        ```
        Returns reference to `CommandTree` instance inside the class.

        This might be needed to invoke decorator `CommandTree.command()` \\
        for slash/application commands, and `CommandTree.sync()` method \\
        in `on_ready()` event. `None` is returned only whether class wasn't \\
        initialized.
        """
        return self.__commandtree
    @_p
    def latency(self):
        """
        \\@since 0.3.26rc3
        ```
        "property" in class Fencord
        ```
        Returns ping of a client; factual description: \\
        Measures latency between a HEARTBEAT and a HEARTBEAT_ACK in seconds.
        """
        return self.__client.latency
    @_p
    def id(self):
        """
        \\@since 0.3.27a2
        ```
        "property" in class Fencord
        ```
        Returns id of the client
        """
        return self.__client.user.id
    @_p
    def display(self):
        """
        \\@since 0.3.27a2
        ```
        "property" in class Fencord
        ```
        Returns display name of the client
        """
        return self.__client.user.display_name
    @_p
    def style(self):
        """
        \\@since 0.3.27a4
        ```
        "property" in class Fencord
        ```
        Return reference to class `FontStyles`
        """
        return FontStyler

    def __init__(self, intents: __dc.Intents = ..., presences: bool = False, members: bool = False, messageContent: bool = True):
        """
        Fencord
        +++++++
        \\@since 0.3.24 (before 0.3.25 as `DC`)
        ```
        in module tense.fencord
        ```
        Providing methods to help integrating with Discord.
        Parameters:
        - `intents` - Instance of `discord.Intents`.
        - `messageContent` - When `True`, `client.message_content` setting is set to `True`, \\
        `False` otherwise. Defaults to `True`.
        """
        if not isinstance(intents, self.__dc.Intents) and not Tense.isEllipsis(intents):
            err = TypeError
            s = f"Parameter 'intends' must have instance of class 'discord.Intents' or an ellipsis, instead received: '{type(intents).__name__}'"
            raise err(s)
        i = 0
        a = ("presences", "members", "messageContent")
        for e in (presences, members, messageContent):
            if not Tense.isBoolean(e):
                err, s = (TypeError, f"Expected a boolean type in parameter '{a[i]}'")
                raise err(s)
            i += 1
        if not isinstance(messageContent, bool):
            err = TypeError
            s = f"Parameter 'messageContent' must have boolean value, instead received: '{type(intents).__name__}'"
            raise err(s)
        if Tense.isEllipsis(intents): self.__intents = self.__dc.Intents.default()
        else: self.__intents = intents
        self.__intents.message_content = messageContent
        self.__intents.presences = presences
        self.__intents.members = members
        self.__client = self.__dc.Client(intents = self.__intents)
        self.__commandtree = self.__app.CommandTree(self.__client)
        if FencordOptions.initializationMessage is True:
            e = Tense.fencordFormat()
            print(f"\33[1;90m{e}\33[1;36m INITIALIZATION\33[0m Class '{__class__.__name__}' was successfully initalized. Line {ins.currentframe().f_back.f_lineno}")
    @_sm
    def returnName(handler: __tc.Union[__dc.Interaction[__dc.Client], __dc.Message], /, target: __tc.Optional[__dc.Member] = None, mention: __tc.Optional[bool] = None, name: __tc.Optional[bool] = None):
        """
        \\@since 0.3.24
        ```
        "static method" in class Fencord
        ```
        Shorthand method for faciliating returning name: display name, mention or just username
        """
        from discord import Member, Interaction
        m = ""
        if isinstance(target, Member):
            if mention is True:
                m = target.mention
            else:
                if name is True: m = target.name
                else: m = target.display_name
        else:
            if isinstance(handler, Interaction):
                if mention is True:
                    m = handler.user.mention
                else:
                    if name is True: m = handler.user.name
                    else: m = handler.user.display_name
            else:
                if mention is True:
                    m = handler.author.mention
                else:
                    if name is True: m = handler.author.name
                    else: m = handler.author.display_name
        return m
    @_sm
    def initClient():
        """
        \\@since 0.3.24
        ```
        "static method" in class Fencord
        ```
        Shortcut to the following lines of code: 
        ```py \\
        intends = discord.Intends.default()
        intends.message_content = True
        client = discord.Client(intends = intends)
        ```
        Returned is new instance of `Client` class. \\
        It does not apply to variables inside this class.
        """
        from discord import Intents, Client
        intends = Intents.default()
        intends.message_content = True
        return Client(intents = intends)
    @_sm
    def commandInvoked(name: str, author: __tc.Union[__dc.Interaction, __dc.Message], /, parameters: __tc.Optional[dict[str, str]] = None, error: __tc.Optional[str] = None):
        """
        \\@since 0.3.24
        ```
        "static method" in class Fencord
        ```
        Prints `INVOCATION` to the console. If `error` is a string, it is returned as `INVOCATION ERROR`
        """
        from discord import Message
        e = Tense.fencordFormat()
        if error is None:
            if isinstance(author, Message): t = f"\33[1;90m{e}\33[1;38;5;99m INVOCATION\33[0m Invoked message command '{name.lower()}' by '{Fencord.returnName(author, name = True)}'"
            else: t = f"\33[1;90m{e}\33[1;38;5;99m INVOCATION\33[0m Invoked slash command '{name.lower()}' by '{Fencord.returnName(author, name = True)}'"
        else:
            if isinstance(author, Message): t = f"\33[1;90m{e}\33[1;38;5;9m INVOCATION ERROR\33[0m Attempt to invoke message command '{name.lower()}' by '{Fencord.returnName(author, name = True)}'"
            else: t = f"\33[1;90m{e}\33[1;38;5;9m INVOCATION ERROR\33[0m Attempt to invoke slash command '{name.lower()}' by '{Fencord.returnName(author, name = True)}'"
        if parameters is not None:
            t += " with parameter values: "
            for e in parameters:
                t += f"'{e}' -> {parameters[e]}, "
            t = re.sub(r", $", "", t)
        if error is not None: t += f"; \33[4m{error}\33[0m"
        return t
    @_sm
    def commandEquals(message: __dc.Message, *words: str):
        """
        \\@since 0.3.24
        ```
        "static method" in class Fencord
        ```
        In reality just string comparison operation; an auxiliary \\
        method for message commands. Case is insensitive
        """
        for string in words:
            if message.content.lower() == string: return True
        return False
    
    def slashCommand(
        self,
        name: __tc.Union[str, _LocaleString, None] = None,
        description: __tc.Union[str, _LocaleString, None] = None,
        nsfw: bool = False,
        parent: __tc.Optional[__app.Group] = None,
        servers: _SlashCommandServers[__dc.abc.Snowflake] = None,
        autoLocaleStrings: bool = True,
        extras: dict[__tc.Any, __tc.Any] = {},
        override: bool = False
        ) -> __tc.Callable[[__app.commands.CommandCallback[__app.Group]], __app.commands.Command[__app.Group, ..., __tc.Any]]: # type: ignore # see scrap of code below for more information
        """
        \\@since 0.3.25 (experimental to 0.3.26rc2) \\
        https://aveyzan.glitch.me/tense/py/method.slashCommand.html
        ```
        "method" in class Fencord
        ```
        A decorator for slash/application commands. Typically a slight remake of `command()` decorator, but in reality \\
        it invokes method `add_command()`. `LocaleString` = `discord.app_commands.translator.locale_str`

        Parameters (all are optional):
        - `name` - The name of the command (string or instance of `locale_str`). If none provided, command name will \\
        be name of the callback, fully lowercased. If `name` was provided, method will convert the string to lowercase, \\
        if there is necessity. Defaults to `None`.
        - `description` - Description of the command (string or instance of `locale_str`). This shows up in the UI to describe \\
        the command. If not given, it defaults to the first line of the docstring of the callback shortened to 100 \\
        characters. Defaults to `None`.
        - `nsfw` - Indicate, whether this command is NSFW (Not Safe For Work) or not. Defaults to `False`.
        - `parent` (since 0.3.26rc3) - The parent application command. `None` if there isn't one. Defaults to `None`.
        - `servers` - single or many instances of `discord.Object` class in a sequence. These represent servers, \\
        to which restrict the command. If `None` given, command becomes global. Notice there **isn't** such parameter as \\
        `server`, because you can pass normal `discord.Object` class instance to this parameter. Defaults to `None`.
        - `autoLocaleStrings` - When it is `True`, then all translatable strings will implicitly be wrapped into `locale_str` \\
        rather than `str`. This could avoid some repetition and be more ergonomic for certain defaults such as default \\
        command names, command descriptions, and parameter names. Defaults to `True`.
        - `extras` - A dictionary that can be used to store additional data. The library will not touch any values or keys \\
        within this dictionary. Defaults to `None`.
        - `override` - If set to `True`, no exception is raised and command may be simply overwritten. Defaults to `False`.
        """
        if self.__commandtree is None:
            err, s = (self.__tc.IncorrectValueError, f"Since 0.3.25 the '{self!s}' class must be concretized and needs to take '{self.__dc.Client!s}' class argument.")
            raise err(s)
        else:
            from ._types import MISSING
            from discord.abc import Snowflake
            from discord.app_commands import Group
            from discord.app_commands.commands import CommandCallback
            if isinstance(servers, Snowflake):
                _servers = tuple([servers])
            elif isinstance(servers, self.__tc.Sequence):
                _servers = tuple([n for n in servers])
            # elif isinstance(servers, Servers): # since 0.3.27a4 (0.3.27 - experimental)
            #    _servers = tuple(servers.list)
            else:
                _servers = None
            # suprisingly unexpected error: pylance said that we need 3 type parameters instead of 1
            # but compiler says we need only 1 instead of 3 (typing module TYPE_CHECKING value = true)
            # hence 'type: ignore' in there, still should work as intended
            def _decorator(f: CommandCallback[Group]): # type: ignore
                nonlocal name, description, nsfw, parent, autoLocaleStrings, extras, override
                if not ins.iscoroutinefunction(f):
                    err, s = (TypeError, "Expected command function to be a coroutine")
                    raise err(s)
                cmd = self.__app.Command(
                    name = name.lower() if Tense.isString(name) and reckon(name) > 0 else name if name is not None else f.__name__,
                    description = description if description is not None else "..." if f.__doc__ is None else f.__doc__[:100],
                    callback = f,
                    nsfw = nsfw,
                    parent = parent,
                    auto_locale_strings = autoLocaleStrings,
                    extras = extras if reckon(extras) > 0 else MISSING
                )
                self.__commandtree.add_command(
                    cmd,
                    # finally came up with a solution with will merge these both parameters
                    # note it always throws an error except something what would bypass this problem
                    guild = _servers[0] if _servers is not None and reckon(_servers) == 1 else None,
                    guilds = _servers if _servers is not None and reckon(_servers) > 1 else MISSING,
                    override = override
                )
                return cmd
            return _decorator

    if False: # under experiments since 0.3.27
        @_sm
        def fixedEmbed(
            nameValue: __tc.Union[dict[str, str], __tc.Sequence[tuple[str, str]]],
            /,
            title: __tc.Optional[str] = None,
            color: __tc.Union[int, __dc.Color, None] = None,
            type: _EmbedType = "rich",
            url: __tc.Optional[str] = None,
            description: __tc.Optional[str] = None,
            timestamp: __tc.Optional[__dct.datetime] = None,
            inline: bool = True,
            footer: __tc.Optional[str] = None,
            footerUrl: __tc.Optional[str] = None,
            author: __tc.Optional[str] = None,
            authorUrl: __tc.Optional[str] = None,
            authorIconUrl: __tc.Optional[str] = None,
            imageUrl: __tc.Optional[str] = None,
            thumbnailUrl: __tc.Optional[str] = None
        ):
            """
            \\@since 0.3.26
            ```
            "static method" in class Fencord
            ```
            Create an `Embed` without 25-field overflow. Good practice for `/help` slash/application command, \\
            hereupon this method has auxiliary character. Amount of `Embed` instances in returned tuple depend \\
            on amount of pairs in `nameValue` parameter: for `(n * 25) + x`, where n ≥ 0 and x ∈ (0; 25) \\
            (assuming x ∈ N; in abridgement: x is integer in range 1-24, including both points) returned are `n` \\
            embed instances. For example: if there was one pair key-value dictionary or sequence with one tuple \\
            with 2 string items, returned will be only one embed, with field declared in parameter `nameValue`: \\
            first item becomes its name, and second - its value.

            :param nameValue: (Field attribute) Dictionary with string keys and string values, list or tuple (since 0.3.27a1 - any sequence)
                with tuples containing 2 string items. Required parameter
            :param title: Title of every embed (string). Defaults to `None`
            :param color: Color of every embed (integer or instance of `discord.Color`/`discord.Colour`). Defaults to `None`
            :param type: Type of every embed from following: 'rich', 'image', 'video', 'gifv', 'article', 'link'. Default is 'rich'.
            :param url: URL of every embed (string). Defaults to `None`
            :param description: Description of every embed (string). Max to 4096 characters. Defaults to `None`.
            :param timestamp: The timestamp of every embed content (instance of `datetime.datetime`). This is an aware datetime.
                If a naive datetime is passed, it is converted to an aware datetime with the local timezone. Defaults to `None`
            :param inline: (Field attribute) Whether the field should be displayed inline (boolean). Defaults to `True`
            :param footer: (Footer attribute) A footer text for every embed (string). If specified, method invokes `set_footer()`
                method, with value specified in the parameter below. Defaults to `None`
            :param footerUrl: (Footer attribute) Footer icon for every embed (string). Defaults to `None`
            :param author: (Author attribute) Author name (string). If specified, method invokes `set_author()` method, with values
                specified in 2 parameters below. Defaults to `None`
            :param authorUrl: (Author attribute) URL of the author (string). Defaults to `None`
            :param authorIconUrl: (Author attribute) URL of the author icon (string). Defaults to `None`
            :param imageUrl: The image URL (string). Defaults to `None`
            :param thumbnailUrl: The thumbnail URL (string). Defaults to `None`
            """
            from ..types_collection import Sequence
            embed = [Fencord.__dc.Embed(color = color, title = title, type = type, url = url, description = description, timestamp = timestamp)]
            i1 = i2 = 0
            if isinstance(nameValue, (Sequence, list, tuple, set, frozenset)):
                d = sorted([n for n in nameValue])
            else:
                d = sorted([(_k, _v) for _k, _v in nameValue.items()])
            if reckon(d) == 0:
                err, s = (ValueError, "Expected 'nameValue' to be non-empty either dictionary or sequence with 2 string items")
                raise err(s)
            for k, v in d:
                if not Tense.isString(k) or not Tense.isString(v):
                    err, s = (TypeError, f"Lacking item or invalid type of a pair: '{k}' -> '{v}'")
                    raise err(s)
                if (i1 - 1) % 25 == 0:
                    embed.append(Fencord.__dc.Embed(color = color, title = title, type = type, url = url, description = description, timestamp = timestamp))
                    i2 += 1
                embed[i2].add_field(name = k, value = v, inline = inline)
                i1 += 1
            for e in embed:
                if not Tense.isNone(author):
                    e.set_author(name = author, url = authorUrl, icon_url = authorIconUrl)
                if not Tense.isNone(imageUrl):
                    e.set_image(url = imageUrl)
                if not Tense.isNone(thumbnailUrl):
                    e.set_thumbnail(url = thumbnailUrl)
                if not Tense.isNone(footer):
                    e.set_footer(text = footer, icon_url = footerUrl)
            return tuple(embed)
    
    def response(
        self,
        interaction: __dc.Interaction,
        content: __tc.Optional[str] = None,
        embeds: __tc.Union[__dc.Embed, __tc.Sequence[__dc.Embed], None] = None,
        files: __tc.Union[__dc.File, __tc.Sequence[__dc.File], None] = None,
        view: __tc.Optional[__dc.ui.View] = None,
        textToSpeech: bool = False,
        restricted: bool = False,
        allowedMentions: __tc.Optional[__dc.AllowedMentions] = None,
        suppressEmbeds: bool = False,
        silent: bool = False,
        deleteAfter: __tc.Optional[float] = None,
        poll: __tc.Optional[__dc.Poll] = None
    ):
        """
        \\@since 0.3.27a1 (renamed on 0.3.27a4 from `send()`)
        ```
        "method" in class Fencord
        ```
        Send a message via current client
        """
        from ._types import MISSING
        if isinstance(embeds, self.__dc.Embed):
            _embeds = tuple([embeds])
        elif isinstance(embeds, self.__tc.Sequence):
            _embeds = tuple(embeds)
        else:
            _embeds = None
        if isinstance(files, self.__dc.File):
            _files = tuple([files])
        elif isinstance(files, self.__tc.Sequence):
            _files = tuple(files)
        else:
            _files = None
        return interaction.response.send_message(
            content = content,
            embed = _embeds[0] if _embeds is not None and reckon(_embeds) == 1 else MISSING,
            embeds = _embeds if _embeds is not None and reckon(_embeds) > 1 else MISSING,
            file = _files[0] if _files is not None and reckon(_files) == 1 else MISSING,
            files = _files if _files is not None and reckon(_files) > 1 else MISSING,
            view = view if view is not None else MISSING,
            tts = textToSpeech,
            ephemeral = restricted,
            allowed_mentions = allowedMentions if allowedMentions is not None else MISSING,
            suppress_embeds = suppressEmbeds,
            silent = silent,
            delete_after = deleteAfter if deleteAfter is not None else MISSING,
            poll = poll if poll is not None else MISSING
        )

    def sync(self, server: __tc.Optional[__dc.abc.Snowflake] = None):
        """
        \\@since 0.3.25
        ```
        "method" in class Fencord
        ```
        Sync all slash/application commands, display them on Discord, and translate all strings to `locale_str`. \\
        Used for `on_ready()` event as `await fencord.sync(server?)`. If class wasn't initialized, thrown is error \\
        `tense.tcs.NotInitializedError`.

        Parameters\\:
        - `server` (Optional) - The server/guild to sync the commands to. If `None` then it syncs all global commands \\
        instead.
        """
        if self.__commandtree is None:
            err, s  = (self.__tc.NotInitializedError, f"Since 0.3.25 the '{__class__.__name__}' class must be concretized.")
            raise err(s)
        else:
            self.__synccorountine = self.__commandtree.sync(guild = server)
            return self.__synccorountine
    
    def event(self, f: __dct.T_coroutine, /):
        """
        \\@since 0.3.25
        ```
        "method" in class Fencord
        ```
        A decorator which defines an event for client to listen to.

        Function injected with this decorator must have valid name, \\
        those can be for example: `on_message()`, `on_ready()`
        """
        if self.__client is None:
            err, s = (self.__tc.NotInitializedError, f"Since 0.3.25 the '{__class__.__name__}' class must be concretized.")
            raise err(s)
        elif not ins.iscoroutinefunction(f):
            err, s = (TypeError, "Expected 'coroutine' parameter to be a coroutine.")
            raise err(s)
        else:
            return self.__client.event(f)

    if False: # removed 0.3.27
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.bold() method instead")
        def bold(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text bold
            """
            return f"**{text}**"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.italic() method instead")
        def italic(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text italic
            """
            return f"*{text}*"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.underline() method instead")
        def underline(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text underlined
            """
            return f"__{text}__"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.code() method instead")
        def code(text: str, language: __tc.Optional[str] = None, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: coded text
            """
            if language is None:
                return f"`{text}`"
            else:
                return f"```{language}\n{text}\n```"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.big() method instead")
        def big(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text big
            """
            return f"# {text}"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.medium() method instead")
        def medium(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text medium
            """
            return f"## {text}"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.small() method instead")
        def small(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text small
            """
            return f"### {text}"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.smaller() method instead")
        def smaller(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text smaller
            """
            return f"-# {text}"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.quote() method instead")
        def quote(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: transform text to quote
            """
            return f"> {text}"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.spoiler() method instead")
        def spoiler(text: str, /):
            """
            \\@since 0.3.25
            ```
            "static method" in class Fencord
            ```
            On Discord: make text spoiled
            """
            return f"||{text}||"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.textUrl() method instead")
        def textUrl(text: str, url: str, hideEmbed = True):
            """
            \\@since 0.3.26a2 \\
            ```
            "static method" in class Fencord
            ```
            On Discord: make text become hyperlink, leading to specified URL
            """
            return f"[{text}](<{url}>)" if hideEmbed else f"[{text}]({url})"
        @_sm
        @__tc.deprecated("Deprecated since 0.3.27a1, migrate to FontStyles.silent() method instead")
        def silent(text: str):
            """
            \\@since 0.3.26a3 \\
            ```
            "static method" in class Fencord
            ```
            Make a message silent. Usable for Direct Messages. \\
            As a tip, refer `@silent` as `> ` (quote), and message \\
            MUST be prefixed with `@silent`.
            """
            return f"@silent {text}"

    __all__ = [n for n in locals() if n[:1] != "_"]
    "\\@since 0.3.26rc2"
    __dir__ = lambda self: Fencord.__all__
    "\\@since 0.3.26rc2"

if __name__ == "__main__":
    err = RuntimeError
    s = "This file is not for compiling, consider importing it instead."
    raise err(s)

del wa, tc, ct, dc, dct # not for export