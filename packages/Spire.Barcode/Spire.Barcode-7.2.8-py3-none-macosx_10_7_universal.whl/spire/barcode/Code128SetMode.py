from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class Code128SetMode(Enum):
    """

    """
    OnlyA = 0
    OnlyB = 1
    OnlyC = 2
    Auto = 3

