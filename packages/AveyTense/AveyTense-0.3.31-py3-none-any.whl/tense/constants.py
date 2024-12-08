"""
**Tense Constants** \n
\\@since 0.3.26rc3 \\
© 2023-Present Aveyzan // License: MIT
```ts
module tense.constants
```
Constants wrapper for Tense. Extracted from former `tense.tcs` module
"""

import math
from ._versioning import version_current, version, version_type

#################################### VERSION COMPONENTS (0.3.26b3) ####################################
# Consider NOT changing the version values, as it may be
# mistaken, and possibly you may not be up-to-date.

_a = version_type[0]
"""Aalpha release"""
_b = version_type[1]
"""beta release"""
_c = version_type[2]
"""release canditate"""
_f = version_type[3]
"""final release"""

VERSION = version[0]
"""
Returns currently used version of Tense. \\
Can be also retrieved with `tense.constants.VERSION_LIST[-1]`
"""
VERSION_TUPLE = version_current
"""Returns currently used version of Tense as a tuple"""

VERSION_LIST = (
    # these comments have to faciliate computing for VERSION_ID
    "0.2.1", # 0
    "0.2.2", # 1
    "0.2.3", # 2
    "0.2.4", # 3
    "0.2.5", # 4
    "0.2.6", # 5
    "0.2.7", # 6
    "0.2.8", # 7
    "0.2.9", # 8
    "0.2.10", # 9
    "0.2.11", # 10
    "0.2.12", # 11
    "0.2.13", # 12
    "0.2.14", # 13
    "0.2.15", # 14
    "0.2.16", # 15
    "0.3.0", # 16
    "0.3.1", # 17
    "0.3.2", # 18
    "0.3.3", # 19
    "0.3.4", # 20
    "0.3.5", # 21
    "0.3.6", # 22
    "0.3.7", # 23
    "0.3.8", # 24
    "0.3.9", # 25
    "0.3.10", # 26
    "0.3.11", # 27
    "0.3.12", # 28
    "0.3.13", # 29
    "0.3.14", # 30
    "0.3.15", # 31
    "0.3.16", # 32
    "0.3.17", # 33
    "0.3.18", # 34
    "0.3.19", # 35
    "0.3.20", # 36
    "0.3.21", # 37
    "0.3.22", # 38
    "0.3.23", # 39
    "0.3.24", # 40
    "0.3.25", # 41
    "0.3.26a1", # 42
    "0.3.26a2", # 43
    "0.3.26a3", # 44
    "0.3.26b1", # 45
    "0.3.26a4", # 46
    "0.3.26b2", # 47
    "0.3.26b3", # 48
    "0.3.26rc1", # 49
    "0.3.26rc2", # 50
    "0.3.26rc3", # 51
    "0.3.26", # 52
    "0.3.27a1", # 53
    "0.3.27a2", # 54
    "0.3.27a3", # 55
    "0.3.27a4", # 56
    "0.3.27a5", # 57
    "0.3.27b1", # 58
    "0.3.27b2", # 59
    "0.3.27b3", # 60
    "0.3.27rc1", # 61
    "0.3.27rc2", # 62
    "0.3.27", # 63
    "0.3.28", # 64
    "0.3.29", # 65
    "0.3.30", # 66
    VERSION, # 67
)
"""
Returns list (not `list`) of Tense versions in ascending order

Note that even version 0.1 of Tense existed, it isn't considered \\
official since it doesn't appear on downloads page.
"""

VERSION_ID = 67
"""Size of constant `VERSION_LIST` minus one (0.2.1 equals 0)"""

#################################### MATH CONSTANTS (0.3.26b3) ####################################

NAN = math.nan
INF = math.inf
E = 2.718281828459045235360287471352
PI = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461
TAU = 6.283185307179586476925287
SQRT2 = 1.4142135623730950488016887242097
THOUSAND           = 1000 # 1e+3
MILLION            = 1000000 # 1e+6
BILLION            = 1000000000 # 1e+9
TRILLION           = 1000000000000 # 1e+12
QUADRILLION        = 1000000000000000 # 1e+15
QUINTILLION        = 1000000000000000000 # 1e+18
SEXTILLION         = 1000000000000000000000 # 1e+21
SEPTILLION         = 1000000000000000000000000 # 1e+24
OCTILLION          = 1000000000000000000000000000 # 1e+27
NONILLION          = 1000000000000000000000000000000 # 1e+30
DECILLION          = 1000000000000000000000000000000000 # 1e+33
UNDECILLION        = 1000000000000000000000000000000000000 # 1e+36
DUODECILLION       = 1000000000000000000000000000000000000000 # 1e+39
TREDECILLION       = 1000000000000000000000000000000000000000000 # 1e+42
QUATTUOR_DECILLION = 1000000000000000000000000000000000000000000000 # 1e+45
QUINDECILLION      = 1000000000000000000000000000000000000000000000000 # 1e+48
SEXDECILLION       = 1000000000000000000000000000000000000000000000000000 # 1e+51
SEPTEN_DECILLION   = 1000000000000000000000000000000000000000000000000000000 # 1e+54
OCTODECILLION      = 1000000000000000000000000000000000000000000000000000000000 # 1e+57
NOVEMDECILLION     = 1000000000000000000000000000000000000000000000000000000000000 # 1e+60
VIGINTILLION       = 1000000000000000000000000000000000000000000000000000000000000000 # 1e+63
GOOGOL             = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 # 1e+100
CENTILLION         = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 # 1e+303


#################################### OTHER CONSTANTS ####################################

JS_MIN_SAFE_INTEGER = -9007199254740991
"""
\\@since 0.3.26b3

`-(2^53 - 1)` - the smallest safe integer in JavaScript
"""
JS_MAX_SAFE_INTEGER = 9007199254740991
"""
\\@since 0.3.26b3

`2^53 - 1` - the biggest safe integer in JavaScript
"""
JS_MIN_VALUE = 4.940656458412465441765687928682213723650598026143247644255856825006755072702087518652998363616359923797965646954457177309266567103559397963987747960107818781263007131903114045278458171678489821036887186360569987307230500063874091535649843873124733972731696151400317153853980741262385655911710266585566867681870395603106249319452715914924553293054565444011274801297099995419319894090804165633245247571478690147267801593552386115501348035264934720193790268107107491703332226844753335720832431936092382893458368060106011506169809753078342277318329247904982524730776375927247874656084778203734469699533647017972677717585125660551199131504891101451037862738167250955837389733598993664809941164205702637090279242767544565229087538682506419718265533447265625e-324
"""
\\@since 0.3.26b3

`2^-1074` - the smallest possible number in JavaScript \\
Precision per digit
"""
JS_MAX_VALUE = 17976931348623139118889956560692130772452639421037405052830403761197852555077671941151929042600095771540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368
"""
\\@since 0.3.26b3

`2^1024 - 2^971` - the biggest possible number in JavaScript \\
Precision per digit
"""

SMASH_HIT_CHECKPOINTS = 13
"""
\\@since 0.3.26b3

Amount of checkpoints in Smash Hit (12 normal, 0-11 + 1 endless)
"""
MC_ENCHANTS = 42
"""
\\@since 0.3.26b3

Amount of enchantments in Minecraft
"""
MC_DURABILITY = {
    "helmet_turtleShell": 275,
    "helmet_leather": 55,
    "helmet_golden": 77,
    "helmet_chainmail": 165,
    "helmet_iron": 165,
    "helmet_diamond": 363,
    "helmet_netherite": 407,
    "chestplate_leather": 80,
    "chestplate_golden": 112,
    "chestplate_chainmail": 240,
    "chestplate_iron": 240,
    "chestplate_diamond": 528,
    "chestplate_netherite": 592,
    "leggings_leather": 75,
    "leggings_golden": 105,
    "leggings_chainmail": 225,
    "leggings_iron": 225,
    "leggings_diamond": 495,
    "leggings_netherite": 555,
    "boots_leather": 65,
    "boots_golden": 91,
    "boots_chainmail": 195,
    "boots_iron": 195,
    "boots_diamond": 429,
    "boots_netherite": 481,
    "bow": 384,
    "shield": 336,
    "trident": 250,
    "elytra": 432,
    "crossbow_java": 465,
    "crossbow_bedrock": 464,
    "brush": 64,
    "fishingRod_java": 64,
    "fishingRod_bedrock": 384,
    "flintAndSteel": 64,
    "carrotOnStick": 25,
    "warpedFungusOnStick": 100,
    "sparkler_bedrock": 100,
    "glowStick_bedrock": 100,
    "tool_gold": 32,
    "tool_wood": 65,
    "tool_stone": 131,
    "tool_iron": 250,
    "tool_diamond": 1561,
    "tool_netherite": 2031
}

__version__ = VERSION
"""
\\@since 0.3.27a3

Returns currently used version of Tense. \\
Can be also retrieved with `tense.constants.VERSION_LIST[-1]`
"""

del version_current, version, version_type