from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class DotfuscatorAttribute (SpireObject) :
    """

    """

    def a(self)->str:
        """

        """
        dlllib.DotfuscatorAttribute_a.argtypes=[c_void_p]
        dlllib.DotfuscatorAttribute_a.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.DotfuscatorAttribute_a,self.Ptr))
        return ret


    def c(self)->int:
        """

        """
        dlllib.DotfuscatorAttribute_c.argtypes=[c_void_p]
        dlllib.DotfuscatorAttribute_c.restype=c_int
        ret = CallCFunction(dlllib.DotfuscatorAttribute_c,self.Ptr)
        return ret

