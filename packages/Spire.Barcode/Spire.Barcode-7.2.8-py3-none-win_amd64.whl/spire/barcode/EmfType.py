from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.barcode import *
from ctypes import *
import abc

class EmfType(Enum):
    """

    """
    EmfOnly = 3
    EmfPlusOnly = 4
    EmfPlusDual = 5

