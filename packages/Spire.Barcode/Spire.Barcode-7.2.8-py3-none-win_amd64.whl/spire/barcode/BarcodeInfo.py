from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class BarcodeInfo (SpireObject) :
    """

    """
    @property

    def BarCodeReadType(self)->'BarCodeReadType':
        """

        """
        dlllib.BarcodeInfo_get_BarCodeReadType.argtypes=[c_void_p]
        dlllib.BarcodeInfo_get_BarCodeReadType.restype=c_int
        ret = CallCFunction(dlllib.BarcodeInfo_get_BarCodeReadType,self.Ptr)
        objwraped = BarCodeReadType(ret)
        return objwraped

    @BarCodeReadType.setter
    def BarCodeReadType(self, value:'BarCodeReadType'):
        dlllib.BarcodeInfo_set_BarCodeReadType.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeInfo_set_BarCodeReadType,self.Ptr, value.value)

#    @property
#
#    def Vertexes(self)->List['Point']:
#        """
#
#        """
#        dlllib.BarcodeInfo_get_Vertexes.argtypes=[c_void_p]
#        dlllib.BarcodeInfo_get_Vertexes.restype=IntPtrArray
#        intPtrArray = dlllib.BarcodeInfo_get_Vertexes(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Point)
#        return ret


    @property

    def DataString(self)->str:
        """

        """
        dlllib.BarcodeInfo_get_DataString.argtypes=[c_void_p]
        dlllib.BarcodeInfo_get_DataString.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeInfo_get_DataString,self.Ptr))
        return ret


    @DataString.setter
    def DataString(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.BarcodeInfo_set_DataString.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.BarcodeInfo_set_DataString,self.Ptr, valuePtr)


    def ToString(self)->str:
        """

        """
        dlllib.BarcodeInfo_ToString.argtypes=[c_void_p]
        dlllib.BarcodeInfo_ToString.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeInfo_ToString,self.Ptr))
        return ret



    def checkSum(self)->str:
        """

        """
        dlllib.BarcodeInfo_checkSum.argtypes=[c_void_p]
        dlllib.BarcodeInfo_checkSum.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeInfo_checkSum,self.Ptr))
        return ret


