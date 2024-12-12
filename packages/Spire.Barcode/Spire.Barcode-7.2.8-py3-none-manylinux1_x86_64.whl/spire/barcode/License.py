from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class License (SpireObject) :
    """

    """
    @staticmethod
    def SetLicenseFileFullPath(licenseFileFullPath:str):
        """

        """
        licenseFileFullPathPtr = StrToPtr(licenseFileFullPath);
        dlllib.LISetLicenseFileFullPath.argtypes=[ c_char_p]
        CallCFunction(dlllib.LISetLicenseFileFullPath,licenseFileFullPathPtr)

    @staticmethod
    def SetLicenseFileName(licenseFileName:str):
        """

        """
        licenseFileNamePtr = StrToPtr(licenseFileName);
        dlllib.LISetLicenseFileName.argtypes=[c_char_p]
        CallCFunction(dlllib.LISetLicenseFileName,licenseFileNamePtr)

    @staticmethod
    def SetLicenseFileStream(licenseFileStream:Stream):
        """

        """
        intPtrlicenseFileStream:c_void_p = licenseFileStream.Ptr

        dlllib.LISetLicenseFileStream.argtypes=[ c_void_p]
        CallCFunction(dlllib.LISetLicenseFileStream, intPtrlicenseFileStream)

    @staticmethod
    def SetLicenseKey(key:str):
        """

        """
        keyPtr = StrToPtr(key);
        dlllib.LISetLicenseKey.argtypes=[c_char_p]
        CallCFunction(dlllib.LISetLicenseKey,keyPtr)


    @staticmethod
    def ClearLicense():
        """

        """
        CallCFunction(dlllib.LIClearLicense)

