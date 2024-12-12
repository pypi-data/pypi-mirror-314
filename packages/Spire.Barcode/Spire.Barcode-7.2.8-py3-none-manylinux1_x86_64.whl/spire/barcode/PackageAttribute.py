from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class PackageAttribute (SpireObject) :
    """

    """
    @property

    def Name(self)->str:
        """

        """
        dlllib.PackageAttribute_get_Name.argtypes=[c_void_p]
        dlllib.PackageAttribute_get_Name.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.PackageAttribute_get_Name,self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.PackageAttribute_set_Name.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.PackageAttribute_set_Name,self.Ptr, valuePtr)

    @property

    def Version(self)->str:
        """

        """
        dlllib.PackageAttribute_get_Version.argtypes=[c_void_p]
        dlllib.PackageAttribute_get_Version.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.PackageAttribute_get_Version,self.Ptr))
        return ret


    @Version.setter
    def Version(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.PackageAttribute_set_Version.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.PackageAttribute_set_Version,self.Ptr, valuePtr)

#    @staticmethod
#
#    def GetPackage(assembly:'Assembly')->List['PackageAttribute']:
#        """
#
#        """
#        intPtrassembly:c_void_p = assembly.Ptr
#
#        dlllib.PackageAttribute_GetPackage.argtypes=[ c_void_p]
#        dlllib.PackageAttribute_GetPackage.restype=IntPtrArray
#        intPtrArray = dlllib.PackageAttribute_GetPackage( intPtrassembly)
#        ret = GetObjVectorFromArray(intPtrArray, PackageAttribute)
#        return ret


