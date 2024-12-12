from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class BarCodeGenerator (SpireObject) :
    """

    """

    @dispatch
    def __init__(self,barcodeSettings:IBarcodeSettings):
        """
        
        """
        intPtrbarcodeSettings:c_void_p = barcodeSettings.Ptr;

        dlllib.BarCodeGenerator_CreateBarCodeGeneratorS.argtypes=[c_void_p]
        dlllib.BarCodeGenerator_CreateBarCodeGeneratorS.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarCodeGenerator_CreateBarCodeGeneratorS,intPtrbarcodeSettings)
        super(BarCodeGenerator, self).__init__(intPtr)

    @dispatch

    def GenerateImage(self):
        """

        """
        dlllib.BarCodeGenerator_GenerateImageBytes.argtypes=[c_void_p]
        dlllib.BarCodeGenerator_GenerateImageBytes.restype=IntPtrArray
        intPtr = CallCFunction(dlllib.BarCodeGenerator_GenerateImageBytes,self.Ptr)
        ret = None if intPtr==None else GetBytesFromArray(intPtr)
        return ret



    @dispatch

    def GenerateImage(self ,barcodeSize:Size):
        """

        """
        intPtrbarcodeSize:c_void_p = barcodeSize.Ptr

        dlllib.BarCodeGenerator_GenerateImageBytesB.argtypes=[c_void_p ,c_void_p]
        dlllib.BarCodeGenerator_GenerateImageBytesB.restype=IntPtrArray
        intPtr = CallCFunction(dlllib.BarCodeGenerator_GenerateImageBytesB,self.Ptr, intPtrbarcodeSize)
        ret = None if intPtr==None else GetBytesFromArray(intPtr)
        return ret



    @staticmethod

    def CopySettings(srcSetting:'IBarcodeSettings',settingsCopyTo:'IBarcodeSettings'):
        """

        """
        intPtrsrcSetting:c_void_p = srcSetting.Ptr
        intPtrsettingsCopyTo:c_void_p = settingsCopyTo.Ptr

        dlllib.BarCodeGenerator_CopySettings.argtypes=[ c_void_p,c_void_p]
        CallCFunction(dlllib.BarCodeGenerator_CopySettings, intPtrsrcSetting,intPtrsettingsCopyTo)

