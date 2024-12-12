from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class TextRenderingHint(Enum):
    """

    """
    SystemDefault = 0
    SingleBitPerPixelGridFit = 1
    SingleBitPerPixel = 2
    AntiAliasGridFit = 3
    AntiAlias = 4
    ClearTypeGridFit = 5

