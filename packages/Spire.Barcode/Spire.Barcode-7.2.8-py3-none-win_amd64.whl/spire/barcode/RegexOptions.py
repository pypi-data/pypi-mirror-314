from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from ctypes import *
import abc

#

class RegexOptions(Enum):
    """

    """
    none = 0
    IgnoreCase = 1
    Multiline = 2
    ExplicitCapture = 4
    Compiled = 8
    Singleline = 16
    IgnorePatternWhitespace = 32
    RightToLeft = 64
    ECMAScript = 256
    CultureInvariant = 512

