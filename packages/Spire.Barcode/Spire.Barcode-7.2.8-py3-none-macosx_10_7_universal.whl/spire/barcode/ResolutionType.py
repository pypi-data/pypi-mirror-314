from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class ResolutionType(Enum):
    """

    """
    Graphics = 0
    UseDpi = 1
    Printer = 2

