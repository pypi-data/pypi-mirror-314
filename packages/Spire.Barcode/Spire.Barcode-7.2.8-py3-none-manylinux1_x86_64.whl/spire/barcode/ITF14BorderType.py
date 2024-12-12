from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class ITF14BorderType(Enum):
    """

    """
    none = 0
    Frame = 1
    Bar = 2

