from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class CheckSumMode(Enum):
    """

    """
    Auto = 1
    ForceEnable = 2
    ForceDisable = 4

