from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class BarcodeSettings (SpireObject,IBarcodeSettings) :
    """

    """
    @dispatch
    def __init__(self):
        """
        
        """
        dlllib.BarcodeSettings_CreateBarcodeSettings.argtypes=[]
        dlllib.BarcodeSettings_CreateBarcodeSettings.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_CreateBarcodeSettings,)
        super(BarcodeSettings, self).__init__(intPtr)
    @property

    def Type(self)->'BarCodeType':
        """

        """
        dlllib.BarcodeSettings_get_Type.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Type.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_Type,self.Ptr)
        objwraped = BarCodeType(ret)
        return objwraped

    @Type.setter
    def Type(self, value:'BarCodeType'):
        dlllib.BarcodeSettings_set_Type.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_Type,self.Ptr, value.value)

    @property

    def Data(self)->str:
        """

        """
        dlllib.BarcodeSettings_get_Data.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Data.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeSettings_get_Data,self.Ptr))
        return ret


    @Data.setter
    def Data(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.BarcodeSettings_set_Data.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.BarcodeSettings_set_Data,self.Ptr, valuePtr)

    @property

    def BackColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_BackColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BackColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_BackColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @BackColor.setter
    def BackColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_BackColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_BackColor,self.Ptr, value.Ptr)

    @property

    def TextColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_TextColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TextColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_TextColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @TextColor.setter
    def TextColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_TextColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_TextColor,self.Ptr, value.Ptr)

    @property
    def BarHeight(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_BarHeight.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BarHeight.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_BarHeight,self.Ptr)
        return ret

    @BarHeight.setter
    def BarHeight(self, value:float):
        dlllib.BarcodeSettings_set_BarHeight.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_BarHeight,self.Ptr, value)

    @property

    def FontColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_FontColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_FontColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_FontColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @FontColor.setter
    def FontColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_FontColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_FontColor,self.Ptr, value.Ptr)

    @property
    def TopMargin(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_TopMargin.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TopMargin.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_TopMargin,self.Ptr)
        return ret

    @TopMargin.setter
    def TopMargin(self, value:float):
        dlllib.BarcodeSettings_set_TopMargin.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_TopMargin,self.Ptr, value)

    @property
    def LeftMargin(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_LeftMargin.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_LeftMargin.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_LeftMargin,self.Ptr)
        return ret

    @LeftMargin.setter
    def LeftMargin(self, value:float):
        dlllib.BarcodeSettings_set_LeftMargin.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_LeftMargin,self.Ptr, value)

    @property
    def TopTextMargin(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_TopTextMargin.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TopTextMargin.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_TopTextMargin,self.Ptr)
        return ret

    @TopTextMargin.setter
    def TopTextMargin(self, value:float):
        dlllib.BarcodeSettings_set_TopTextMargin.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_TopTextMargin,self.Ptr, value)


    def SetTextFont(self ,name:str,size:float,fontStyle:'FontStyle'):
        """

        """
        enumfontStyle:c_int = fontStyle.value
        namePtr = StrToPtr(name)

        dlllib.BarcodeSettings_SetTextFont.argtypes=[c_void_p ,c_char_p,c_float,c_int]
        CallCFunction(dlllib.BarcodeSettings_SetTextFont,self.Ptr, namePtr,size,enumfontStyle)

    @property

    def UseChecksum(self)->'CheckSumMode':
        """

        """
        dlllib.BarcodeSettings_get_UseChecksum.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_UseChecksum.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_UseChecksum,self.Ptr)
        objwraped = CheckSumMode(ret)
        return objwraped

    @UseChecksum.setter
    def UseChecksum(self, value:'CheckSumMode'):
        dlllib.BarcodeSettings_set_UseChecksum.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_UseChecksum,self.Ptr, value.value)

    @property
    def AutoResize(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_AutoResize.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_AutoResize.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_AutoResize,self.Ptr)
        return ret

    @AutoResize.setter
    def AutoResize(self, value:bool):
        dlllib.BarcodeSettings_set_AutoResize.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_AutoResize,self.Ptr, value)

    @property

    def Data2D(self)->str:
        """

        """
        dlllib.BarcodeSettings_get_Data2D.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Data2D.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeSettings_get_Data2D,self.Ptr))
        return ret


    @Data2D.setter
    def Data2D(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.BarcodeSettings_set_Data2D.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.BarcodeSettings_set_Data2D,self.Ptr, valuePtr)

    @property

    def TopText(self)->str:
        """

        """
        dlllib.BarcodeSettings_get_TopText.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TopText.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeSettings_get_TopText,self.Ptr))
        return ret


    @TopText.setter
    def TopText(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.BarcodeSettings_set_TopText.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.BarcodeSettings_set_TopText,self.Ptr, valuePtr)

    @property

    def TopTextColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_TopTextColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TopTextColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_TopTextColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @TopTextColor.setter
    def TopTextColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_TopTextColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_TopTextColor,self.Ptr, value.Ptr)

    @property

    def ITF14BearerBars(self)->'ITF14BorderType':
        """

        """
        dlllib.BarcodeSettings_get_ITF14BearerBars.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ITF14BearerBars.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_ITF14BearerBars,self.Ptr)
        objwraped = ITF14BorderType(ret)
        return objwraped

    @ITF14BearerBars.setter
    def ITF14BearerBars(self, value:'ITF14BorderType'):
        dlllib.BarcodeSettings_set_ITF14BearerBars.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_ITF14BearerBars,self.Ptr, value.value)


    def SetTopTextFont(self ,name:str,size:float,fontStyle:'FontStyle'):
        """

        """
        enumfontStyle:c_int = fontStyle.value
        namePtr = StrToPtr(name)

        dlllib.BarcodeSettings_SetTopTextFont.argtypes=[c_void_p ,c_char_p,c_float,c_int]
        CallCFunction(dlllib.BarcodeSettings_SetTopTextFont,self.Ptr, namePtr,size,enumfontStyle)

    @property
    def ShowTopText(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_ShowTopText.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ShowTopText.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_ShowTopText,self.Ptr)
        return ret

    @ShowTopText.setter
    def ShowTopText(self, value:bool):
        dlllib.BarcodeSettings_set_ShowTopText.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_ShowTopText,self.Ptr, value)

    @property
    def Unit(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_Unit.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Unit.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_Unit,self.Ptr)
        return ret

    @Unit.setter
    def Unit(self, value:int):
        dlllib.BarcodeSettings_set_Unit.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_Unit,self.Ptr, value)

    @property
    def TextRenderingHint(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_TextRenderingHint.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TextRenderingHint.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_TextRenderingHint,self.Ptr)
        return ret

    @TextRenderingHint.setter
    def TextRenderingHint(self, value:int):
        dlllib.BarcodeSettings_set_TextRenderingHint.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_TextRenderingHint,self.Ptr, value)

    @property
    def Rotate(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_Rotate.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Rotate.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_Rotate,self.Ptr)
        return ret

    @Rotate.setter
    def Rotate(self, value:float):
        dlllib.BarcodeSettings_set_Rotate.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_Rotate,self.Ptr, value)

    @property

    def ForeColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_ForeColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ForeColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_ForeColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @ForeColor.setter
    def ForeColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_ForeColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_ForeColor,self.Ptr, value.Ptr)

    @property
    def ShowText(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_ShowText.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ShowText.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_ShowText,self.Ptr)
        return ret

    @ShowText.setter
    def ShowText(self, value:bool):
        dlllib.BarcodeSettings_set_ShowText.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_ShowText,self.Ptr, value)

    @property
    def ShowTextOnBottom(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_ShowTextOnBottom.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ShowTextOnBottom.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_ShowTextOnBottom,self.Ptr)
        return ret

    @ShowTextOnBottom.setter
    def ShowTextOnBottom(self, value:bool):
        dlllib.BarcodeSettings_set_ShowTextOnBottom.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_ShowTextOnBottom,self.Ptr, value)

    @property
    def BottomMargin(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_BottomMargin.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BottomMargin.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_BottomMargin,self.Ptr)
        return ret

    @BottomMargin.setter
    def BottomMargin(self, value:float):
        dlllib.BarcodeSettings_set_BottomMargin.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_BottomMargin,self.Ptr, value)

    @property
    def TextMargin(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_TextMargin.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TextMargin.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_TextMargin,self.Ptr)
        return ret

    @TextMargin.setter
    def TextMargin(self, value:float):
        dlllib.BarcodeSettings_set_TextMargin.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_TextMargin,self.Ptr, value)

    @property
    def RightMargin(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_RightMargin.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_RightMargin.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_RightMargin,self.Ptr)
        return ret

    @RightMargin.setter
    def RightMargin(self, value:float):
        dlllib.BarcodeSettings_set_RightMargin.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_RightMargin,self.Ptr, value)

    @property
    def TextAlignment(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_TextAlignment.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TextAlignment.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_TextAlignment,self.Ptr)
        return ret

    @TextAlignment.setter
    def TextAlignment(self, value:int):
        dlllib.BarcodeSettings_set_TextAlignment.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_TextAlignment,self.Ptr, value)

    @property
    def UseAntiAlias(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_UseAntiAlias.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_UseAntiAlias.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_UseAntiAlias,self.Ptr)
        return ret

    @UseAntiAlias.setter
    def UseAntiAlias(self, value:bool):
        dlllib.BarcodeSettings_set_UseAntiAlias.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_UseAntiAlias,self.Ptr, value)

    @property
    def ImageHeight(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_ImageHeight.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ImageHeight.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_ImageHeight,self.Ptr)
        return ret

    @ImageHeight.setter
    def ImageHeight(self, value:float):
        dlllib.BarcodeSettings_set_ImageHeight.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_ImageHeight,self.Ptr, value)

    @property
    def ImageWidth(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_ImageWidth.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ImageWidth.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_ImageWidth,self.Ptr)
        return ret

    @ImageWidth.setter
    def ImageWidth(self, value:float):
        dlllib.BarcodeSettings_set_ImageWidth.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_ImageWidth,self.Ptr, value)

    @property
    def ColumnCount(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_ColumnCount.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ColumnCount.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_ColumnCount,self.Ptr)
        return ret

    @ColumnCount.setter
    def ColumnCount(self, value:int):
        dlllib.BarcodeSettings_set_ColumnCount.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_ColumnCount,self.Ptr, value)

    @property
    def RowCount(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_RowCount.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_RowCount.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_RowCount,self.Ptr)
        return ret

    @RowCount.setter
    def RowCount(self, value:int):
        dlllib.BarcodeSettings_set_RowCount.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_RowCount,self.Ptr, value)

    @property
    def DpiX(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_DpiX.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_DpiX.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_DpiX,self.Ptr)
        return ret

    @DpiX.setter
    def DpiX(self, value:float):
        dlllib.BarcodeSettings_set_DpiX.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_DpiX,self.Ptr, value)

    @property
    def DpiY(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_DpiY.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_DpiY.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_DpiY,self.Ptr)
        return ret

    @DpiY.setter
    def DpiY(self, value:float):
        dlllib.BarcodeSettings_set_DpiY.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_DpiY,self.Ptr, value)

    @property

    def ResolutionType(self)->'ResolutionType':
        """

        """
        dlllib.BarcodeSettings_get_ResolutionType.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ResolutionType.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_ResolutionType,self.Ptr)
        objwraped = ResolutionType(ret)
        return objwraped

    @ResolutionType.setter
    def ResolutionType(self, value:'ResolutionType'):
        dlllib.BarcodeSettings_set_ResolutionType.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_ResolutionType,self.Ptr, value.value)

    @property
    def ShowCheckSumChar(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_ShowCheckSumChar.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ShowCheckSumChar.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_ShowCheckSumChar,self.Ptr)
        return ret

    @ShowCheckSumChar.setter
    def ShowCheckSumChar(self, value:bool):
        dlllib.BarcodeSettings_set_ShowCheckSumChar.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_ShowCheckSumChar,self.Ptr, value)

    @property

    def CodabarStartChar(self)->'CodabarChar':
        """

        """
        dlllib.BarcodeSettings_get_CodabarStartChar.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_CodabarStartChar.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_CodabarStartChar,self.Ptr)
        objwraped = CodabarChar(ret)
        return objwraped

    @CodabarStartChar.setter
    def CodabarStartChar(self, value:'CodabarChar'):
        dlllib.BarcodeSettings_set_CodabarStartChar.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_CodabarStartChar,self.Ptr, value.value)

    @property

    def CodabarStopChar(self)->'CodabarChar':
        """

        """
        dlllib.BarcodeSettings_get_CodabarStopChar.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_CodabarStopChar.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_CodabarStopChar,self.Ptr)
        objwraped = CodabarChar(ret)
        return objwraped

    @CodabarStopChar.setter
    def CodabarStopChar(self, value:'CodabarChar'):
        dlllib.BarcodeSettings_set_CodabarStopChar.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_CodabarStopChar,self.Ptr, value.value)

    @property
    def ShowStartCharAndStopChar(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_ShowStartCharAndStopChar.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ShowStartCharAndStopChar.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_ShowStartCharAndStopChar,self.Ptr)
        return ret

    @ShowStartCharAndStopChar.setter
    def ShowStartCharAndStopChar(self, value:bool):
        dlllib.BarcodeSettings_set_ShowStartCharAndStopChar.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_ShowStartCharAndStopChar,self.Ptr, value)

    @property

    def SupData(self)->str:
        """

        """
        dlllib.BarcodeSettings_get_SupData.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_SupData.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeSettings_get_SupData,self.Ptr))
        return ret


    @SupData.setter
    def SupData(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.BarcodeSettings_set_SupData.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.BarcodeSettings_set_SupData,self.Ptr, valuePtr)

    @property
    def SupSpace(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_SupSpace.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_SupSpace.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_SupSpace,self.Ptr)
        return ret

    @SupSpace.setter
    def SupSpace(self, value:float):
        dlllib.BarcodeSettings_set_SupSpace.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_SupSpace,self.Ptr, value)

    @property
    def WideNarrowRatio(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_WideNarrowRatio.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_WideNarrowRatio.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_WideNarrowRatio,self.Ptr)
        return ret

    @WideNarrowRatio.setter
    def WideNarrowRatio(self, value:float):
        dlllib.BarcodeSettings_set_WideNarrowRatio.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_WideNarrowRatio,self.Ptr, value)

    @property
    def HasBorder(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_HasBorder.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_HasBorder.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_HasBorder,self.Ptr)
        return ret

    @HasBorder.setter
    def HasBorder(self, value:bool):
        dlllib.BarcodeSettings_set_HasBorder.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_HasBorder,self.Ptr, value)

    @property
    def BorderWidth(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_BorderWidth.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BorderWidth.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_BorderWidth,self.Ptr)
        return ret

    @BorderWidth.setter
    def BorderWidth(self, value:float):
        dlllib.BarcodeSettings_set_BorderWidth.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_BorderWidth,self.Ptr, value)

    @property

    def BorderColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_BorderColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BorderColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_BorderColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @BorderColor.setter
    def BorderColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_BorderColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_BorderColor,self.Ptr, value.Ptr)

    @property
    def BorderDashStyle(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_BorderDashStyle.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BorderDashStyle.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_BorderDashStyle,self.Ptr)
        return ret

    @BorderDashStyle.setter
    def BorderDashStyle(self, value:int):
        dlllib.BarcodeSettings_set_BorderDashStyle.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_BorderDashStyle,self.Ptr, value)

    @property
    def X(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_X.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_X.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_X,self.Ptr)
        return ret

    @X.setter
    def X(self, value:float):
        dlllib.BarcodeSettings_set_X.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_X,self.Ptr, value)

    @property
    def Y(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_Y.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Y.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_Y,self.Ptr)
        return ret

    @Y.setter
    def Y(self, value:float):
        dlllib.BarcodeSettings_set_Y.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_Y,self.Ptr, value)

    @property
    def XYRatio(self)->float:
        """

        """
        dlllib.BarcodeSettings_get_XYRatio.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_XYRatio.restype=c_float
        ret = CallCFunction(dlllib.BarcodeSettings_get_XYRatio,self.Ptr)
        return ret

    @XYRatio.setter
    def XYRatio(self, value:float):
        dlllib.BarcodeSettings_set_XYRatio.argtypes=[c_void_p, c_float]
        CallCFunction(dlllib.BarcodeSettings_set_XYRatio,self.Ptr, value)

    @property

    def Code128SetMode(self)->'Code128SetMode':
        """

        """
        dlllib.BarcodeSettings_get_Code128SetMode.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Code128SetMode.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_Code128SetMode,self.Ptr)
        objwraped = Code128SetMode(ret)
        return objwraped

    @Code128SetMode.setter
    def Code128SetMode(self, value:'Code128SetMode'):
        dlllib.BarcodeSettings_set_Code128SetMode.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_Code128SetMode,self.Ptr, value.value)

    @property

    def Pdf417DataMode(self)->'Pdf417DataMode':
        """

        """
        dlllib.BarcodeSettings_get_Pdf417DataMode.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Pdf417DataMode.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_Pdf417DataMode,self.Ptr)
        objwraped = Pdf417DataMode(ret)
        return objwraped

    @Pdf417DataMode.setter
    def Pdf417DataMode(self, value:'Pdf417DataMode'):
        dlllib.BarcodeSettings_set_Pdf417DataMode.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_Pdf417DataMode,self.Ptr, value.value)

    @property

    def Pdf417ECL(self)->'Pdf417ECL':
        """

        """
        dlllib.BarcodeSettings_get_Pdf417ECL.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Pdf417ECL.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_Pdf417ECL,self.Ptr)
        objwraped = Pdf417ECL(ret)
        return objwraped

    @Pdf417ECL.setter
    def Pdf417ECL(self, value:'Pdf417ECL'):
        dlllib.BarcodeSettings_set_Pdf417ECL.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_Pdf417ECL,self.Ptr, value.value)

    @property
    def Pdf417Truncated(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_Pdf417Truncated.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_Pdf417Truncated.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_Pdf417Truncated,self.Ptr)
        return ret

    @Pdf417Truncated.setter
    def Pdf417Truncated(self, value:bool):
        dlllib.BarcodeSettings_set_Pdf417Truncated.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_Pdf417Truncated,self.Ptr, value)

    @property
    def AztecLayers(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_AztecLayers.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_AztecLayers.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_AztecLayers,self.Ptr)
        return ret

    @AztecLayers.setter
    def AztecLayers(self, value:int):
        dlllib.BarcodeSettings_set_AztecLayers.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_AztecLayers,self.Ptr, value)

    @property
    def AztecErrorCorrection(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_AztecErrorCorrection.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_AztecErrorCorrection.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_AztecErrorCorrection,self.Ptr)
        return ret

    @AztecErrorCorrection.setter
    def AztecErrorCorrection(self, value:int):
        dlllib.BarcodeSettings_set_AztecErrorCorrection.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_AztecErrorCorrection,self.Ptr, value)

    @property

    def DataMatrixSymbolShape(self)->'DataMatrixSymbolShape':
        """

        """
        dlllib.BarcodeSettings_get_DataMatrixSymbolShape.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_DataMatrixSymbolShape.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_DataMatrixSymbolShape,self.Ptr)
        objwraped = DataMatrixSymbolShape(ret)
        return objwraped

    @DataMatrixSymbolShape.setter
    def DataMatrixSymbolShape(self, value:'DataMatrixSymbolShape'):
        dlllib.BarcodeSettings_set_DataMatrixSymbolShape.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_DataMatrixSymbolShape,self.Ptr, value.value)

    @property
    def MacroFileIndex(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_MacroFileIndex.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_MacroFileIndex.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_MacroFileIndex,self.Ptr)
        return ret

    @MacroFileIndex.setter
    def MacroFileIndex(self, value:int):
        dlllib.BarcodeSettings_set_MacroFileIndex.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_MacroFileIndex,self.Ptr, value)

    @property
    def MacroSegmentIndex(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_MacroSegmentIndex.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_MacroSegmentIndex.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_MacroSegmentIndex,self.Ptr)
        return ret

    @MacroSegmentIndex.setter
    def MacroSegmentIndex(self, value:int):
        dlllib.BarcodeSettings_set_MacroSegmentIndex.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_MacroSegmentIndex,self.Ptr, value)

    @property

    def QRCodeDataMode(self)->'QRCodeDataMode':
        """

        """
        dlllib.BarcodeSettings_get_QRCodeDataMode.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_QRCodeDataMode.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_QRCodeDataMode,self.Ptr)
        objwraped = QRCodeDataMode(ret)
        return objwraped

    @QRCodeDataMode.setter
    def QRCodeDataMode(self, value:'QRCodeDataMode'):
        dlllib.BarcodeSettings_set_QRCodeDataMode.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_QRCodeDataMode,self.Ptr, value.value)

    @property

    def QRCodeECL(self)->'QRCodeECL':
        """

        """
        dlllib.BarcodeSettings_get_QRCodeECL.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_QRCodeECL.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_QRCodeECL,self.Ptr)
        objwraped = QRCodeECL(ret)
        return objwraped

    @QRCodeECL.setter
    def QRCodeECL(self, value:'QRCodeECL'):
        dlllib.BarcodeSettings_set_QRCodeECL.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_QRCodeECL,self.Ptr, value.value)

    @dispatch

    def SetQRCodeLogoImage(self ,imgFile:str):
        """

        """
        imgFilePtr = StrToPtr(imgFile);
        dlllib.BarcodeSettings_SetQRCodeLogoImage.argtypes=[c_void_p ,c_char_p]
        CallCFunction(dlllib.BarcodeSettings_SetQRCodeLogoImage,self.Ptr, imgFilePtr)

    @dispatch

    def SetQRCodeLogoImage(self ,imgStream:Stream):
        """

        """
        intPtrimgStream:c_void_p = imgStream.Ptr

        dlllib.BarcodeSettings_SetQRCodeLogoImageI.argtypes=[c_void_p ,c_void_p]
        CallCFunction(dlllib.BarcodeSettings_SetQRCodeLogoImageI,self.Ptr, intPtrimgStream)

    @property
    def TopTextAligment(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_TopTextAligment.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_TopTextAligment.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_TopTextAligment,self.Ptr)
        return ret

    @TopTextAligment.setter
    def TopTextAligment(self, value:int):
        dlllib.BarcodeSettings_set_TopTextAligment.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_TopTextAligment,self.Ptr, value)

    @property

    def BottomText(self)->str:
        """

        """
        dlllib.BarcodeSettings_get_BottomText.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BottomText.restype=c_void_p
        ret = PtrToStr(CallCFunction(dlllib.BarcodeSettings_get_BottomText,self.Ptr))
        return ret


    @BottomText.setter
    def BottomText(self, value:str):
        valuePtr = StrToPtr(value);
        dlllib.BarcodeSettings_set_BottomText.argtypes=[c_void_p, c_char_p]
        CallCFunction(dlllib.BarcodeSettings_set_BottomText,self.Ptr, valuePtr)

    @property

    def BottomTextColor(self)->'Color':
        """

        """
        dlllib.BarcodeSettings_get_BottomTextColor.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BottomTextColor.restype=c_void_p
        intPtr = CallCFunction(dlllib.BarcodeSettings_get_BottomTextColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @BottomTextColor.setter
    def BottomTextColor(self, value:'Color'):
        dlllib.BarcodeSettings_set_BottomTextColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(dlllib.BarcodeSettings_set_BottomTextColor,self.Ptr, value.Ptr)


    def SetBottomTextFont(self ,name:str,size:float,fontStyle:'FontStyle'):
        """

        """
        enumfontStyle:c_int = fontStyle.value
        namePtr = StrToPtr(name);

        dlllib.BarcodeSettings_SetBottomTextFont.argtypes=[c_void_p ,c_char_p,c_float,c_int]
        CallCFunction(dlllib.BarcodeSettings_SetBottomTextFont,self.Ptr, namePtr,size,enumfontStyle)

    @property
    def ShowBottomText(self)->bool:
        """

        """
        dlllib.BarcodeSettings_get_ShowBottomText.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_ShowBottomText.restype=c_bool
        ret = CallCFunction(dlllib.BarcodeSettings_get_ShowBottomText,self.Ptr)
        return ret

    @ShowBottomText.setter
    def ShowBottomText(self, value:bool):
        dlllib.BarcodeSettings_set_ShowBottomText.argtypes=[c_void_p, c_bool]
        CallCFunction(dlllib.BarcodeSettings_set_ShowBottomText,self.Ptr, value)

    @property
    def BottomTextAligment(self)->int:
        """

        """
        dlllib.BarcodeSettings_get_BottomTextAligment.argtypes=[c_void_p]
        dlllib.BarcodeSettings_get_BottomTextAligment.restype=c_int
        ret = CallCFunction(dlllib.BarcodeSettings_get_BottomTextAligment,self.Ptr)
        return ret

    @BottomTextAligment.setter
    def BottomTextAligment(self, value:int):
        dlllib.BarcodeSettings_set_BottomTextAligment.argtypes=[c_void_p, c_int]
        CallCFunction(dlllib.BarcodeSettings_set_BottomTextAligment,self.Ptr, value)

