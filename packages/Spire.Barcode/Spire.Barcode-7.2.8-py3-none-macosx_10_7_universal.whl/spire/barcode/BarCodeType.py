from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.barcode import *
from ctypes import *
import abc

class BarCodeType(Enum):
    """

    """
    Codabar = 1
    Code11 = 2
    Code25 = 3
    Interleaved25 = 4
    Code39 = 5
    Code39Extended = 6
    Code93 = 7
    Code93Extended = 8
    Code128 = 9
    EAN8 = 10
    EAN13 = 11
    EAN128 = 12
    EAN14 = 13
    SCC14 = 14
    SSCC18 = 15
    ITF14 = 16
    ITF6 = 17
    UPCA = 18
    UPCE = 19
    PostNet = 20
    Planet = 21
    MSI = 22
    QRCode = 24
    DataMatrix = 23
    Pdf417 = 25
    Pdf417Macro = 26
    RSS14 = 27
    RSS14Truncated = 28
    RSSLimited = 29
    RSSExpanded = 30
    USPS = 31
    SwissPostParcel = 32
    PZN = 33
    OPC = 34
    DeutschePostIdentcode = 35
    DeutschePostLeitcode = 36
    RoyalMail4State = 37
    SingaporePost4State = 38
    Aztec = 39
    MicroQR = 40

