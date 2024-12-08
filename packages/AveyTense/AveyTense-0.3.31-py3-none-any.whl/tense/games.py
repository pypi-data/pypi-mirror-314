
from tense import *
from ._primal_types import (
    TypeVar as _var,
    Union as _uni,
    Optional as _opt,
    Literal as _lit
)

from .types_collection import (
    FileType as _FileType,
    EnchantedBookQuantity as _EnchantedBookQuantity
)

_cm = classmethod
_TicTacToeBoard = list[list[str]]

class Games:
    """
    \\@since 0.3.25 \\
    \\@author Aveyzan
    ```
    # created 15.07.2024
    in module tense # in tense.games module since 0.3.31
    ```
    Class being a deputy of class `Tense08Games`.
    """
    import tkinter as __tk, re as __re
    
    def __init__(self) -> None:
        pass
    
    MC_ENCHANTS = 42
    """
    \\@since 0.3.25 \\
    \\@author Aveyzan
    ```
    // created 18.07.2024
    const in class Games
    ```
    Returns amount of enchantments as for Minecraft 1.21. \\
    It does not include max enchantment level sum.
    """
    SMASH_HIT_CHECKPOINTS = 13
    """
    \\@since 0.3.26a2 \\
    \\@author Aveyzan
    ```
    // created 20.07.2024
    const in class Games
    ```
    Returns amount of checkpoints in Smash Hit. \\
    12 + endless (1) = 13 (12, because 0-11)
    """
    @_cm
    def mcEnchBook(
        self,
        target: str = "@p",
        /, # <- 0.3.26rc2
        quantity: _EnchantedBookQuantity = 1,
        name: _opt[str] = None,
        lore: _opt[str] = None,
        file: _uni[_FileType, None] = None,
        *,
        aquaAffinity: _uni[bool, _lit[1, None]] = None,
        baneOfArthropods: _lit[1, 2, 3, 4, 5, None] = None,
        blastProtection: _lit[1, 2, 3, 4, None] = None,
        breach: _lit[1, 2, 3, 4, None] = None,
        channeling: _uni[bool, _lit[1, None]] = None,
        curseOfBinding: _uni[bool, _lit[1, None]] = None,
        curseOfVanishing: _uni[bool, _lit[1, None]] = None,
        density: _lit[1, 2, 3, 4, 5, None] = None,
        depthStrider: _lit[1, 2, 3, None] = None,
        efficiency: _lit[1, 2, 3, 4, 5, None] = None,
        featherFalling: _lit[1, 2, 3, 4, None] = None,
        fireAspect: _lit[1, 2, None] = None,
        fireProtection: _lit[1, 2, 3, 4, None] = None,
        flame: _uni[bool, _lit[1, None]] = None,
        fortune: _lit[1, 2, 3, None] = None,
        frostWalker: _lit[1, 2, None] = None,
        impaling: _lit[1, 2, 3, 4, 5, None] = None,
        infinity: _uni[bool, _lit[1, None]] = None,
        knockback: _lit[1, 2, None] = None,
        looting: _lit[1, 2, 3, None] = None,
        loyalty: _lit[1, 2, 3, None] = None,
        luckOfTheSea: _lit[1, 2, 3, None] = None,
        lure: _lit[1, 2, 3, None] = None,
        mending: _uni[bool, _lit[1, None]] = None,
        multishot: _uni[bool, _lit[1, None]] = None,
        piercing: _lit[1, 2, 3, 4, None] = None,
        power: _lit[1, 2, 3, 4, 5, None] = None,
        projectileProtection: _lit[1, 2, 3, 4, None] = None,
        protection: _lit[1, 2, 3, 4, None] = None,
        punch: _lit[1, 2, None] = None,
        quickCharge: _lit[1, 2, 3, None] = None,
        respiration: _lit[1, 2, 3, None] = None,
        riptide: _lit[1, 2, 3, None] = None,
        sharpness: _lit[1, 2, 3, 4, 5, None] = None,
        silkTouch: _uni[bool, _lit[1, None]] = None,
        smite: _lit[1, 2, 3, 4, 5, None] = None,
        soulSpeed: _lit[1, 2, 3, None] = None,
        sweepingEdge: _lit[1, 2, 3, None] = None,
        swiftSneak: _lit[1, 2, 3, None] = None,
        thorns: _lit[1, 2, 3, None] = None,
        unbreaking: _lit[1, 2, 3, None] = None,
        windBurst: _lit[1, 2, 3, None] = None
    ):
        """
        \\@since 0.3.25 \\
        \\@modified 0.3.31 (cancelled `StringVar` and `BooleanVar` Tkinter types support + shortened code)
        https://aveyzan.glitch.me/tense/py/method.mcEnchBook.html
        ```
        # created 18.07.2024
        "class method" in class Games
        ```
        Minecraft `/give <target> ...` command generator for specific enchanted books.
        Basing on https://www.digminecraft.com/generators/give_enchanted_book.php.
        
        Parameters (all are optional):
        - `target` - registered player name or one of special identifiers: `@p` (closest player), \\
        `@a` (all players), `@r` (random player), `@s` (entity running command; will not work in \\
        command blocks). Defaults to `@p`
        - `quantity` - amount of enchanted books to give to the target. Due to fact that enchanted \\
        books aren't stackable, there is restriction put to 36 (total inventory slots, excluding left hand) \\
        instead of 64 maximum. Defaults to 1
        - `name` - name of the enchanted book. Does not affect enchants; it is like putting that book \\
        to anvil and simply renaming. Defaults to `None`
        - `lore` - lore of the enchanted book. Totally I don't know what it does. Defaults to `None`
        - `file` - file to write the command into. This operation will be only done, when command has \\
        been prepared and will be about to be returned. This file will be open in `wt` mode. If file \\
        does not exist, code will attempt to create it. Highly recommended to use file with `.txt` \\
        extension. Defaults to `None`

        Next parameters are enchants. For these having level 1 only, a boolean value can be passed: \\
        in this case `False` will be counterpart of default value `None` of each, `True` means 1.
        """
        from re import (
            search as _search,
            sub as _sub
        )
        
        # 'target' must be a string
        if not Tense.isString(target):
            error = TypeError("expected parameter 'target' to be of type 'str'")
            raise error
        
        # /give minecraft command begins
        _result = "/give "
        _target = target
        
        # ensure 'target' belongs to one of selectors or matches a-zA-Z0-9_ (player name possible characters)
        _selectors = ("@a", "@s", "@p", "@r")
        
        if _target.lower() in _selectors or _search(r"[^a-zA-Z0-9_]", _target) is None:
            _result += _target
        
        else:
            error = ValueError("Parameter 'target' has invalid value, either selector or player name. Possible selectors: @a, @s, @p, @r. Player name may only have chars from ranges: a-z, A-Z, 0-9 and underscores (_)")
            raise error
        
        # next is adding the 'enchanted_book' item
        _result += " enchanted_book["
        
        
        if not Tense.isInteger(quantity):
            error = TypeError("expected parameter 'quantity' to be of type 'int'")
            raise error
        
        elif quantity not in -abroad(1, 36.1):
            error = ValueError("expected parameter 'quantity' value to be in range 1-36")
            raise error
        
        if not Tense.isNone(name):
            
            if not Tense.isString(name):
                err, s = (TypeError, "expected parameter 'name' to be of type 'str' or 'None'")
                raise err(s)
            
            else:
                _result += "custom_name={}, ".format("{\"text\": \"" + name + "\"}")
        
        if not Tense.isNone(lore):
            
            if not Tense.isString(lore):
                err, s = (TypeError, "expected parameter 'lore' to be of type 'str' or 'None'")
                raise err(s)
            
            else:
                _result += "lore=[{}], ".format("{\"text\": \"" + lore + "\"}")
        
        def _fix_name(s: str, /):
            """
            @since 0.3.31
            
            Internal function used to deputize name using CamelCase naming convention \\
            to one, which Python uses in PEP 8 (as well as Minecraft; with _).
            """
    
            _s = ""
            
            for i in abroad(s):
                
                if s[i].isupper():
                    _s += "_" + s[i].lower()
                    
                else:
                    _s += s[i]
                    
            return _s
        
        _level_1_tuple = (1, True, False)
        _level_2_tuple = (1, 2)
        _level_3_tuple = (1, 2, 3)
        _level_4_tuple = (1, 2, 3, 4)
        _level_5_tuple = (1, 2, 3, 4, 5)
        
        # same can be done with invocation of eval() function in this case, but used is this
        # version to deduce united type of all enchantments
        _params = [p for p in (
            aquaAffinity, baneOfArthropods, blastProtection, breach, channeling, curseOfBinding, curseOfVanishing, density, depthStrider, efficiency, featherFalling, flame, fireAspect, fireProtection, fortune,
            frostWalker, impaling, infinity, knockback, looting, loyalty, luckOfTheSea, lure, mending, multishot, piercing, power, projectileProtection, protection, punch, quickCharge, respiration, riptide,
            sharpness, silkTouch, smite, soulSpeed, sweepingEdge, swiftSneak, thorns, unbreaking, windBurst
        )]
        
        # excluding 'None', it will be inspected later
        # these variables are there to provide changes easier,
        # if there were ones concerning the enchantments' levels
        _required_params = (
            _level_1_tuple, # aqua affinity
            _level_5_tuple, # bane of arthropods
            _level_4_tuple, # blast protection
            _level_4_tuple, # breach
            _level_1_tuple, # channeling
            _level_1_tuple, # curse of binding
            _level_1_tuple, # curse of vanishing
            _level_5_tuple, # density
            _level_3_tuple, # depth strider
            _level_5_tuple, # efficiency
            _level_4_tuple, # feather falling
            _level_2_tuple, # fire aspect
            _level_4_tuple, # fire protection
            _level_1_tuple, # flame
            _level_3_tuple, # fortune
            _level_2_tuple, # frost walker
            _level_5_tuple, # impaling
            _level_1_tuple, # infinity
            _level_2_tuple, # knockback
            _level_3_tuple, # looting
            _level_3_tuple, # loyalty
            _level_3_tuple, # luck of the sea
            _level_3_tuple, # lure
            _level_1_tuple, # mending
            _level_1_tuple, # multishot
            _level_4_tuple, # piercing
            _level_5_tuple, # power
            _level_4_tuple, # projectile protection
            _level_4_tuple, # protection
            _level_2_tuple, # punch
            _level_3_tuple, # quick charge
            _level_3_tuple, # respiration
            _level_3_tuple, # riptide
            _level_5_tuple, # sharpness
            _level_1_tuple, # silk touch
            _level_5_tuple, # smite
            _level_3_tuple, # soul speed
            _level_3_tuple, # sweeping edge
            _level_3_tuple, # swift sneak
            _level_3_tuple, # thorns
            _level_3_tuple, # unbreaking
            _level_3_tuple, # wind burst
        )
        
        _enchantslack = 0
        
        # instead of using 'inspect.signature()' function, which would include string extraction, and this extraction might take long time
        _enchantments = [k for k in self.mcEnchBook.__annotations__][5:]
        
        # this dictionary led to error once it occured in following way: {_params[i]: (_enchantments[i], _required_params[i]) for i in abroad(_params)},
        # because there were only 2 pairs and completely unintentional was overriding key values; only changed order of _params and _enchantments went
        # successful (there used assertion statement to figure it out)
        _build = {_enchantments[i]: (_params[i], _required_params[i]) for i in abroad(_params)}
        
        # first inspection before we append 'stored_enchantments' inside squared, unclosed bracket
        for k in _build:
            
            if Tense.isNone(_build[k][0]):
                _enchantslack += 1
        
        # every enchantment has value 'None', what means we can clear the squared bracket
        # ONLY if 'name' and 'lore' have value 'None'
        if _enchantslack == reckon(_enchantments):
            return _result[:-1] if reckon(Tense.any([name, lore], lambda x: Tense.isNone(x))) == 2 else _result
        
        else:
            _result += "stored_enchantments={"
        
        # further inspection and finalizing the resulted string
        for k in _build:
            
            # skip whether 'None'
            if not Tense.isNone(_build[k][0]):
                
                if _build[k][0] not in _build[k][1]:
                    
                    error = ValueError("expected parameter '{}' to have integer value".format(k) + (" in range 1-{}".format(_build[k][1][-1]) if _build[k][1] != (1, True, False) else " 1 or boolean value, either 'True' or 'False'"))
                    raise error
                
                if Tense.isBoolean(_build[k][0]):
                    
                    # skip whether 'False'
                    if _build[k][0] is True:
                        _result += "\"{}\": 1, ".format(_fix_name(k))
                        
                elif Tense.isInteger(_build[k][0]):
                    
                    _result += "\"{}\": {}, ".format(_fix_name(k), _build[k][0])
            
            else:
                _enchantslack += 1
        
        # missing closing curly and squared brackets, replace with last comma
        _result = _sub(r", $", "}] ", _result) + str(quantity)
        
        if file is not None:
            
            if not isinstance(file, _FileType):
                error = TypeError("parameter 'file' has incorrect file name or type")
                raise error
            
            try:
                f = open(file, "x")
                
            except FileExistsError:
                f = open(file, "wt")
            
            f.write(_result)
            f.close()
            
        return _result
    
    O = "o"
    X = "x"
    __ttBoard = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    __ttPlayerChar = X
    __ttPlayerId = 1
    __ttPlayerChar1 = "x"
    __ttPlayerChar2 = "o"
    @_cm
    def isBoardFilled(self):
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25
        ```
        "class method" in class Games
        ```
        (Tic-Tac-Toe) Determine whether the whole board is filled, but there is no winner
        """
        return (self.__ttBoard[0][0] != self.ttEmptyField() and self.__ttBoard[0][1] != self.ttEmptyField() and self.__ttBoard[0][2] != self.ttEmptyField() and
                self.__ttBoard[1][0] != self.ttEmptyField() and self.__ttBoard[1][1] != self.ttEmptyField() and self.__ttBoard[1][2] != self.ttEmptyField() and
                self.__ttBoard[2][0] != self.ttEmptyField() and self.__ttBoard[2][1] != self.ttEmptyField() and self.__ttBoard[2][2] != self.ttEmptyField())
    @_cm
    def isLineMatched(self):
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25
        ```
        "class method" in class Games
        ```
        (Tic-Tac-Toe) Determine whether a line is matched on the board
        """
        return ((
            # horizontal match
            self.__ttBoard[0][0] == self.__ttPlayerChar and self.__ttBoard[0][1] == self.__ttPlayerChar and self.__ttBoard[0][2] == self.__ttPlayerChar) or (
            self.__ttBoard[1][0] == self.__ttPlayerChar and self.__ttBoard[1][1] == self.__ttPlayerChar and self.__ttBoard[1][2] == self.__ttPlayerChar) or (
            self.__ttBoard[2][0] == self.__ttPlayerChar and self.__ttBoard[2][1] == self.__ttPlayerChar and self.__ttBoard[2][2] == self.__ttPlayerChar) or (
            
            # vertical match
            self.__ttBoard[0][0] == self.__ttPlayerChar and self.__ttBoard[1][0] == self.__ttPlayerChar and self.__ttBoard[2][0] == self.__ttPlayerChar) or (
            self.__ttBoard[0][1] == self.__ttPlayerChar and self.__ttBoard[1][1] == self.__ttPlayerChar and self.__ttBoard[2][1] == self.__ttPlayerChar) or (
            self.__ttBoard[0][2] == self.__ttPlayerChar and self.__ttBoard[1][2] == self.__ttPlayerChar and self.__ttBoard[2][2] == self.__ttPlayerChar) or (
            
            # cursive match
            self.__ttBoard[0][0] == self.__ttPlayerChar and self.__ttBoard[1][1] == self.__ttPlayerChar and self.__ttBoard[2][2] == self.__ttPlayerChar) or (
            self.__ttBoard[2][0] == self.__ttPlayerChar and self.__ttBoard[1][1] == self.__ttPlayerChar and self.__ttBoard[0][2] == self.__ttPlayerChar
        ))
    @_cm
    def ttEmptyField(self):
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25
        ```
        "class method" in class Games
        ```
        Returns empty field for tic-tac-toe game.
        """
        return " "
    @_cm
    def ttBoardGenerate(self) -> _TicTacToeBoard:
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        Generates a new tic-tac-toe board.
        Content: `list->list(3)->str(3)` (brackets: amount of strings `" "`)
        """
        return Tense.repeat(Tense.repeat(" ", 3), 3)
    @_cm
    def ttIndexCheck(self, input: int, /):
        """
        \\@since 0.3.6 \\
        \\@lifetime ≥ 0.3.6; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        . : Tic-Tac-Toe (Tense 0.3.6) : . \n
        To return `True`, number must be in in range 1-9. There \\
        is template below. Number 0 exits program.

        `1 | 2 | 3` \\
        `4 | 5 | 6` \\
        `7 | 8 | 9` \n
        """
        if input == 0:
            Tense.print("Exitting...")
            exit()
        elif input >= 1 and input <= 9:
            check = " "
            if input == 1: check = self.__ttBoard[0][0]
            elif input == 2: check = self.__ttBoard[0][1]
            elif input == 3: check = self.__ttBoard[0][2]
            elif input == 4: check = self.__ttBoard[1][0]
            elif input == 5: check = self.__ttBoard[1][1]
            elif input == 6: check = self.__ttBoard[1][2]
            elif input == 7: check = self.__ttBoard[2][0]
            elif input == 8: check = self.__ttBoard[2][1]
            else: check = self.__ttBoard[2][2]

            if check != self.__ttPlayerChar1 and check != self.__ttPlayerChar2: return True
        return False
    
    @_cm
    def ttFirstPlayer(self):
        """
        \\@since 0.3.6 \\
        \\@lifetime ≥ 0.3.6; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        . : Tic-Tac-Toe (Tense 0.3.6) : . \n
        Selects first player to start the tic-tac-toe game. \n
        First parameter will take either number 1 or 2, meanwhile second -
        \"x\" or \"o\" (by default). This setting can be changed via `ttChangeChars()` method \n
        **Warning:** do not use `ttChangeChars()` method during the game, do it before, as since you can mistaken other player \n
        Same case goes to this method. Preferably, encase whole game in `while self.ttLineMatch() == 2:` loop
        """
        self.__ttPlayerId = Tense.pick((1, 2))
        self.__ttPlayerChar = ""
        if self.__ttPlayerId == 1: self.__ttPlayerChar = self.__ttPlayerChar1
        else: self.__ttPlayerChar = self.__ttPlayerChar2
        return self
    @_cm
    def ttNextPlayer(self):
        """
        \\@since 0.3.6 \\
        \\@lifetime ≥ 0.3.6; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        . : Tic-Tac-Toe (Tense 0.3.6) : . \n
        Swaps the player turn to its concurrent (aka other player) \n
        """
        if self.__ttPlayerId == 1:
            self.__ttPlayerId = 2
            self.__ttPlayerChar = self.__ttPlayerChar2
        else:
            self.__ttPlayerId = 1
            self.__ttPlayerChar = self.__ttPlayerChar1
        return self
    @_cm
    def ttBoardDisplay(self):
        """
        \\@since 0.3.6 \\
        \\@lifetime ≥ 0.3.6; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        . : Tic-Tac-Toe (Tense 0.3.6) : . \\
        Allows to display the board after modifications, either clearing or placing another char \n
        """
        print(self.__ttBoard[0][0] + " | " + self.__ttBoard[0][1] + " | " + self.__ttBoard[0][2])
        print(self.__ttBoard[1][0] + " | " + self.__ttBoard[1][1] + " | " + self.__ttBoard[1][2])
        print(self.__ttBoard[2][0] + " | " + self.__ttBoard[2][1] + " | " + self.__ttBoard[2][2])
        return self
    @_cm
    def ttBoardLocationSet(self, _input: int):
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        This method places a char on the specified index on the board
        """
        while not self.ttIndexCheck(_input):
            _input = int(input())
        print("Location set! Modifying the board: \n\n")
        if _input == 1: self.__ttBoard[0][0] = self.__ttPlayerChar
        elif _input == 2: self.__ttBoard[0][1] = self.__ttPlayerChar
        elif _input == 3: self.__ttBoard[0][2] = self.__ttPlayerChar
        elif _input == 4: self.__ttBoard[1][0] = self.__ttPlayerChar
        elif _input == 5: self.__ttBoard[1][1] = self.__ttPlayerChar
        elif _input == 6: self.__ttBoard[1][2] = self.__ttPlayerChar
        elif _input == 7: self.__ttBoard[2][0] = self.__ttPlayerChar
        elif _input == 8: self.__ttBoard[2][1] = self.__ttPlayerChar
        else: self.__ttBoard[2][2] = self.__ttPlayerChar
        self.ttBoardDisplay()
        return self
    @_cm
    def ttBoardClear(self):
        """
        \\@since 0.3.6 \\
        \\@lifetime ≥ 0.3.6; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        Clears the tic-tac-toe board. It is ready for another game
        """
        self.__ttBoard = self.ttBoardGenerate()
        return self
    @_cm
    def ttBoardSyntax(self):
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        Displays tic-tac-toe board syntax
        """
        print("""
        1 | 2 | 3
        4 | 5 | 6
        7 | 8 | 9
        """)
        return self
    @_cm
    def ttLineMatch(self, messageIfLineDetected: str = "Line detected! Player " + str(__ttPlayerId) + " wins!", messageIfBoardFilled: str = "Looks like we have a draw! Nice gameplay!"):
        """
        \\@since 0.3.6 \\
        \\@lifetime ≥ 0.3.6; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        Matches a line found in the board. Please ensure that the game has started. \\
        Returned values:
        - `0`, when a player matched a line in the board with his character. Game ends after.
        - `1`, when there is a draw - board got utterly filled. Game ends with no winner.
        - `2`, game didn't end, it's still going (message for this case isnt sent, because it can disturb during the game).

        """
        if self.isLineMatched():
            Tense.print(messageIfLineDetected)
            return 0
        elif self.isBoardFilled():
            Tense.print(messageIfBoardFilled)
            return 1
        else: return 2

    @_cm
    def ttChangeChars(self, char1: str = "x", char2: str = "o", /):
        """
        \\@since 0.3.7 \\
        \\@lifetime ≥ 0.3.7; < 0.3.24; ≥ 0.3.25 \\
        \\@modified 0.3.25
        ```
        "class method" in class Games
        ```
        Allows to replace x and o chars with different char. \\
        If string is longer than one char, first char of that string is selected \\
        Do it BEFORE starting a tic-tac-toe game
        """
        if reckon(char1) == 1: self.__ttPlayerChar1 = char1
        else: self.__ttPlayerChar1 = char1[0]
        if reckon(char2) == 1: self.__ttPlayerChar2 = char2
        else: self.__ttPlayerChar2 = char2[0]
        return self