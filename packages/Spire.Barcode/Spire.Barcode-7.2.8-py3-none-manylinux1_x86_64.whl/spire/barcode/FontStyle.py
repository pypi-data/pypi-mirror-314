from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple


from ctypes import *
import abc

class FontStyle(Enum):
    """

    """
    Regular = 0
    Bold = 1
    Italic = 2
    Underline = 4
    Strikeout = 8

