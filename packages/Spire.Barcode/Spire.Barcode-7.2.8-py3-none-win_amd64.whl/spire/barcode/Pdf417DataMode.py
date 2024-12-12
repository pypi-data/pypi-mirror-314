from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class Pdf417DataMode(Enum):
    """

    """
    Auto = 0
    Text = 1
    Numeric = 2
    Byte = 3

