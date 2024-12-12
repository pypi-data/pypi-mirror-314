from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class CodabarChar(Enum):
    """

    """
    A = 65
    B = 66
    C = 67
    D = 68

