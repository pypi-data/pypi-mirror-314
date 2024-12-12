from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class IChecksum (abc.ABC) :
    """

    """

    def Calculate(self ,data:str)->str:
        """

        """
        dataPtr = StrToPtr(data);
        dlllib.IChecksum_Calculate.argtypes=[c_void_p ,c_char_p]
        dlllib.IChecksum_Calculate.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.IChecksum_Calculate,self.Ptr, dataPtr))
        return ret


