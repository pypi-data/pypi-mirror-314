from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
#
from spire.barcode import *
from ctypes import *
import abc

class ReleaseDateAttribute (SpireObject) :
    """

    """
    @property

    def ReleaseDate(self)->str:
        """

        """
        dlllib.ReleaseDateAttribute_get_ReleaseDate.argtypes=[c_void_p]
        dlllib.ReleaseDateAttribute_get_ReleaseDate.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.ReleaseDateAttribute_get_ReleaseDate,self.Ptr))
        return ret


    @ReleaseDate.setter
    def ReleaseDate(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.ReleaseDateAttribute_set_ReleaseDate.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.ReleaseDateAttribute_set_ReleaseDate,self.Ptr, valuePtr)

#    @staticmethod
#
#    def GetReleaseDate(assembly:'Assembly')->'Nullable1':
#        """
#
#        """
#        intPtrassembly:c_void_p = assembly.Ptr
#
#        dlllib.ReleaseDateAttribute_GetReleaseDate.argtypes=[ c_void_p]
#        dlllib.ReleaseDateAttribute_GetReleaseDate.restype=c_void_p
#        intPtr = dlllib.ReleaseDateAttribute_GetReleaseDate( intPtrassembly)
#        ret = None if intPtr==None else Nullable1(intPtr)
#        return ret
#


