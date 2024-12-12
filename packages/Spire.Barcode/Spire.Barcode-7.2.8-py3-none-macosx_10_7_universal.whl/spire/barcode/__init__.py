import sys
import os
import platform
from ctypes import *
from typing import TypeVar,Union,Generic,List,Tuple


def LoadLib(path:str):
    whlPath = os.path.abspath(__file__ + '/../lib/'+ path)
    fileExists = os.path.isfile(whlPath)
    if fileExists:
        return cdll.LoadLibrary(whlPath)
    fileExists = os.path.isfile(path)
    if fileExists:
        return cdll.LoadLibrary(path)

    return None

os_name = platform.system()
os_version = platform.release()
path = os.environ['PATH']
new_path = os.path.abspath(__file__ + '/../lib/')
os.environ['PATH'] = new_path + os.pathsep + path

if os_name == "Windows":
    lib_pathDoc = r'.\Spire.Barcode.Base.dll'
elif os_name == "Linux":
    lib_pathDoc = r'./Spire.Barcode.Base.so'
elif os_name =="Darwin":
    lib_pathDoc = r'./Spire.Barcode.Base.dylib'
else:
    lib_pathDoc = r'./Spire.Barcode.Base.dll'

dlllibDoc = None
dlllibDoc = LoadLib(lib_pathDoc)
dlllib = dlllibDoc
if dlllibDoc != None:
    dlllib = dlllibDoc



def GetDllLibDoc():
    #if dlllibDoc == None:
    #    dlllibDoc = LoadLib(lib_pathDoc)
    #if dlllibDoc != None:
    dlllib = dlllibDoc
    return dlllibDoc;


def ChangeHandleToDoc():
    GetDllLibDoc()

class SpireException(Exception):
    """Custom Exception"""
    def __init__(self, message="custom exception"):
        self.message = message
        super().__init__(self.message)

def CallCFunction(func, *args, **kwargs):
    data = create_string_buffer(sizeof(c_uint64))
    old_value  = 0
    # Write the initial values to the allocated memory
    memmove(data, byref(c_uint64(0)), sizeof(c_uint64))
    args = list(args) +[data]

    result = func(*args, **kwargs)
    modified_value = cast(data, POINTER(c_uint64)).contents.value
    if old_value != modified_value:
        info = PtrToStr(modified_value)
        raise SpireException(info)
    return result

from spire.barcode.SpireObject import SpireObject

from spire.barcode.Common import IntPtrArray
from spire.barcode.Common import GetObjVectorFromArray
from spire.barcode.Common import GetVectorFromArray
from spire.barcode.Common import GetStrVectorFromArray
from spire.barcode.Common import GetIntPtrArray
from spire.barcode.Common import GetByteArray
from spire.barcode.Common import GetIntValue
from spire.barcode.Common import GetBytesFromArray
from spire.barcode.Common import PtrToStr
from spire.barcode.Common import StrToPtr
from spire.barcode.Common import ReleasePtr

from spire.barcode.RegexOptions import RegexOptions
from spire.barcode.CultureInfo import CultureInfo
from spire.barcode.PixelFormat import PixelFormat
from spire.barcode.Size import Size
from spire.barcode.SizeF import SizeF
from spire.barcode.Point import Point
from spire.barcode.PointF import PointF
from spire.barcode.Rectangle import Rectangle
from spire.barcode.RectangleF import RectangleF
from spire.barcode.TimeSpan import TimeSpan
from spire.barcode.ImageFormat import ImageFormat
from spire.barcode.Stream import Stream
from spire.barcode.Color import Color
from spire.barcode.DateTime import DateTime
from spire.barcode.EmfType import EmfType
from spire.barcode.Encoding import Encoding
from spire.barcode.FontStyle import FontStyle
from spire.barcode.GraphicsUnit import GraphicsUnit
from spire.barcode.Regex import Regex


from spire.barcode import dlllib
from spire.barcode import dlllibDoc

from spire.barcode.BarCodeType import BarCodeType
from spire.barcode.IBarcodeSettings import IBarcodeSettings

from spire.barcode.BarCodeFormatException import BarCodeFormatException
from spire.barcode.BarCodeGenerator import BarCodeGenerator
from spire.barcode.BarcodeInfo import BarcodeInfo
from spire.barcode.BarCodeReadType import BarCodeReadType
from spire.barcode.BarcodeScanner import BarcodeScanner
from spire.barcode.BarcodeSettings import BarcodeSettings

from spire.barcode.BitArrayHelper import BitArrayHelper
from spire.barcode.CheckSumMode import CheckSumMode
from spire.barcode.CodabarChar import CodabarChar
from spire.barcode.Code128SetMode import Code128SetMode
from spire.barcode.DashStyle import DashStyle
from spire.barcode.DataMatrixSymbolShape import DataMatrixSymbolShape
from spire.barcode.DotfuscatorAttribute import DotfuscatorAttribute
from spire.barcode.EmfType import EmfType
from spire.barcode.GraphicsUnit import GraphicsUnit

from spire.barcode.IChecksum import IChecksum
from spire.barcode.ITF14BorderType import ITF14BorderType
from spire.barcode.License import License
from spire.barcode.PackageAttribute import PackageAttribute
from spire.barcode.Pdf417DataMode import Pdf417DataMode
from spire.barcode.Pdf417ECL import Pdf417ECL
from spire.barcode.QRCodeDataMode import QRCodeDataMode
from spire.barcode.QRCodeECL import QRCodeECL
from spire.barcode.ReleaseDateAttribute import ReleaseDateAttribute
from spire.barcode.ResolutionType import ResolutionType
from spire.barcode.StringAlignment import StringAlignment
from spire.barcode.SymbologyType import SymbologyType
from spire.barcode.TextRenderingHint import TextRenderingHint



