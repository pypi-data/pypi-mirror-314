from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class QRCodeECL(Enum):
    """

    """
    L = 0
    M = 1
    Q = 2
    H = 3

