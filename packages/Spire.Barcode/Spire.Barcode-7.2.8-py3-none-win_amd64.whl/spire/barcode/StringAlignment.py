from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class StringAlignment(Enum):
    """

    """
    Near = 0
    Center = 1
    Far = 2

