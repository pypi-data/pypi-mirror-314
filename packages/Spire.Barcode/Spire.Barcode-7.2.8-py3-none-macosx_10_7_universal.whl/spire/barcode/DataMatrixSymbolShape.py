from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class DataMatrixSymbolShape(Enum):
    """

    """
    Auto = 0
    Square = 1
    Rectangle = 2

