from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from ctypes import *
import abc

class GraphicsUnit(Enum):
    """

    """
    World = 0
    Display = 1
    Pixel = 2
    Point = 3
    Inch = 4
    Document = 5
    Millimeter = 6

