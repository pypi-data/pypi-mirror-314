from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class BitArrayHelper (SpireObject) :
    """

    """
#    @staticmethod
#
#    def PopFront(bits:'BitArray[]&')->'BitArray':
#        """
#
#        """
#        intPtrbits:c_void_p = bits.Ptr
#
#        dlllib.BitArrayHelper_PopFront.argtypes=[ c_void_p]
#        dlllib.BitArrayHelper_PopFront.restype=c_void_p
#        intPtr = dlllib.BitArrayHelper_PopFront( intPtrbits)
#        ret = None if intPtr==None else BitArray(intPtr)
#        return ret
#


#    @staticmethod
#
#    def PopBack(bits:'BitArray[]&')->'BitArray':
#        """
#
#        """
#        intPtrbits:c_void_p = bits.Ptr
#
#        dlllib.BitArrayHelper_PopBack.argtypes=[ c_void_p]
#        dlllib.BitArrayHelper_PopBack.restype=c_void_p
#        intPtr = dlllib.BitArrayHelper_PopBack( intPtrbits)
#        ret = None if intPtr==None else BitArray(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ToBitArray(data:str)->'BitArray':
#        """
#
#        """
#        
#        dlllib.BitArrayHelper_ToBitArray.argtypes=[ c_wchar_p]
#        dlllib.BitArrayHelper_ToBitArray.restype=c_void_p
#        intPtr = dlllib.BitArrayHelper_ToBitArray( data)
#        ret = None if intPtr==None else BitArray(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ToBitMatrix(data:List[str])->List['BitArray']:
#        """
#
#        """
#        #arraydata:ArrayTypedata = ""
#        countdata = len(data)
#        ArrayTypedata = c_wchar_p * countdata
#        arraydata = ArrayTypedata()
#        for i in range(0, countdata):
#            arraydata[i] = data[i]
#
#
#        dlllib.BitArrayHelper_ToBitMatrix.argtypes=[ ArrayTypedata]
#        dlllib.BitArrayHelper_ToBitMatrix.restype=IntPtrArray
#        intPtrArray = dlllib.BitArrayHelper_ToBitMatrix( arraydata)
#        ret = GetObjVectorFromArray(intPtrArray, BitArray)
#        return ret


