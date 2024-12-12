from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class QRCodeDataMode(Enum):
    """

    """
    Auto = 0
    Numeric = 1
    AlphaNumber = 2
    Byte = 4

