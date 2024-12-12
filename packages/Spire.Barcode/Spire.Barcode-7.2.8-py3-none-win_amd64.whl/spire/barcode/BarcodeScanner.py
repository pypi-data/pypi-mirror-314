from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class BarcodeScanner (SpireObject) :
    """

    """
#    @staticmethod
#    
#
#    def ScanInfo(fileName:str)->List[BarcodeInfo]:
#        """
#
#        """
#        
#        dlllib.BarcodeScanner_ScanInfo.argtypes=[ c_wchar_p]
#        dlllib.BarcodeScanner_ScanInfo.restype=IntPtrArray
#        intPtrArray = dlllib.BarcodeScanner_ScanInfo( fileName)
#        ret = GetObjVectorFromArray(intPtrArray, BarcodeInfo)
#        return ret


#    @staticmethod
#    
#
#    def ScanInfo(fileName:str,barcodeType:BarCodeType)->List[BarcodeInfo]:
#        """
#
#        """
#        enumbarcodeType:c_int = barcodeType.value
#
#        dlllib.BarcodeScanner_ScanInfoFB.argtypes=[ c_wchar_p,c_int]
#        dlllib.BarcodeScanner_ScanInfoFB.restype=IntPtrArray
#        intPtrArray = dlllib.BarcodeScanner_ScanInfoFB( fileName,enumbarcodeType)
#        ret = GetObjVectorFromArray(intPtrArray, BarcodeInfo)
#        return ret


    @staticmethod
    

    def ScanFileWithBarCodeType(fileName:str,barcodeType:BarCodeType)->List[str]:
        """

        """
        enumbarcodeType:c_int = barcodeType.value
        intPtrFileName = StrToPtr(fileName)

        dlllib.BarcodeScanner_Scan.argtypes=[c_char_p,c_int]
        dlllib.BarcodeScanner_Scan.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_Scan,intPtrFileName,enumbarcodeType)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanFile(fileName:str)->List[str]:
        """

        """
        fileNamePtr = StrToPtr(fileName);

        dlllib.BarcodeScanner_ScanF.argtypes=[c_char_p]
        dlllib.BarcodeScanner_ScanF.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_ScanF,fileNamePtr)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanFileWithIncludeCheckSum(fileName:str,IncludeCheckSum:bool)->List[str]:
        """

        """
        fileNamePtr = StrToPtr(fileName)
        dlllib.BarcodeScanner_ScanFI.argtypes=[c_char_p,c_bool]
        dlllib.BarcodeScanner_ScanFI.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_ScanFI,fileNamePtr,IncludeCheckSum)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanFileBarCodeTypeIncludeCheckSum(fileName:str,barcodeType:BarCodeType,IncludeCheckSum:bool)->List[str]:
        """

        """
        enumbarcodeType:c_int = barcodeType.value
        fileNamePtr = StrToPtr(fileName)

        dlllib.BarcodeScanner_ScanFBI.argtypes=[ c_char_p,c_int,c_bool]
        dlllib.BarcodeScanner_ScanFBI.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_ScanFBI,fileNamePtr,enumbarcodeType,IncludeCheckSum)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanOneFile(fileName:str)->str:
        """

        """
        fileNamePtr = StrToPtr(fileName);

        dlllib.BarcodeScanner_ScanOne.argtypes=[c_char_p]
        dlllib.BarcodeScanner_ScanOne.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeScanner_ScanOne,fileNamePtr))
        return ret


    @staticmethod
    

    def ScanOneFileWithIncludeCheckSum(fileName:str,IncludeCheckSum:bool)->str:
        """

        """
        fileNamePtr = StrToPtr(fileName)

        dlllib.BarcodeScanner_ScanOneFI.argtypes=[ c_char_p,c_bool]
        dlllib.BarcodeScanner_ScanOneFI.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeScanner_ScanOneFI,fileNamePtr,IncludeCheckSum))
        return ret


    @staticmethod
    

    def ScanOneFileBarCodeTypeIncludeCheckSum(fileName:str,barcodeType:BarCodeType,IncludeCheckSum:bool)->str:
        """

        """
        enumbarcodeType:c_int = barcodeType.value
        fileNamePtr = StrToPtr(fileName)

        dlllib.BarcodeScanner_ScanOneFBI.argtypes=[ c_char_p,c_int,c_bool]
        dlllib.BarcodeScanner_ScanOneFBI.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeScanner_ScanOneFBI, fileNamePtr,enumbarcodeType,IncludeCheckSum))
        return ret


    @staticmethod
    

    def ScanStream(stream:Stream)->List[str]:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        dlllib.BarcodeScanner_ScanS.argtypes=[ c_void_p]
        dlllib.BarcodeScanner_ScanS.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_ScanS, intPtrstream)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanStreamWithIncludeCheckSum(stream:Stream,IncludeCheckSum:bool)->List[str]:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        dlllib.BarcodeScanner_ScanSI.argtypes=[ c_void_p,c_bool]
        dlllib.BarcodeScanner_ScanSI.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_ScanSI, intPtrstream,IncludeCheckSum)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanStreamBarCodeTypeIncludeCheckSum(stream:Stream,barcodeType:BarCodeType,IncludeCheckSum:bool)->List[str]:
        """

        """
        intPtrstream:c_void_p = stream.Ptr
        enumbarcodeType:c_int = barcodeType.value

        dlllib.BarcodeScanner_ScanSBI.argtypes=[ c_void_p,c_int,c_bool]
        dlllib.BarcodeScanner_ScanSBI.restype=IntPtrArray
        intPtrArray = CallCFunction(dlllib.BarcodeScanner_ScanSBI, intPtrstream,enumbarcodeType,IncludeCheckSum)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @staticmethod
    

    def ScanOneStream(stream:Stream)->str:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        dlllib.BarcodeScanner_ScanOneS.argtypes=[ c_void_p]
        dlllib.BarcodeScanner_ScanOneS.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeScanner_ScanOneS, intPtrstream))
        return ret


    @staticmethod
    

    def ScanOneStreamWithIncludeCheckSum(stream:Stream,IncludeCheckSum:bool)->str:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        dlllib.BarcodeScanner_ScanOneSI.argtypes=[ c_void_p,c_bool]
        dlllib.BarcodeScanner_ScanOneSI.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeScanner_ScanOneSI, intPtrstream,IncludeCheckSum))
        return ret


    @staticmethod
    

    def ScanOneStreamBarCodeTypeIncludeCheckSum(stream:Stream,barcodeType:BarCodeType,IncludeCheckSum:bool)->str:
        """

        """
        intPtrstream:c_void_p = stream.Ptr
        enumbarcodeType:c_int = barcodeType.value

        dlllib.BarcodeScanner_ScanOneSBI.argtypes=[ c_void_p,c_int,c_bool]
        dlllib.BarcodeScanner_ScanOneSBI.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeScanner_ScanOneSBI, intPtrstream,enumbarcodeType,IncludeCheckSum))
        return ret


