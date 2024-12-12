from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class Blacklist (SpireObject) :
    """
<summary> 
            Authorization Blacklist
    </summary>
    """
    @staticmethod

    def BlacklistData()->List[str]:
        """
<summary> 
            The serial number or the MD5 code of the key that is entered into the authorization blacklist. 
    </summary>
        """
        #dlllib.Blacklist_BlacklistData.argtypes=[]
        dlllib.Blacklist_BlacklistData.restype=IntPtrArray
        intPtrArray = dlllib.Blacklist_BlacklistData()
        ret = GetVectorFromArray(intPtrArray, c_wchar_p)
        return ret

