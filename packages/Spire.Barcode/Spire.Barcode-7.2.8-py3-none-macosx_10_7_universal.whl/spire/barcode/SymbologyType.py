from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class SymbologyType(Enum):
    """

    """
    Codabar = 1
    Code11 = 2
    Code39Standard = 4
    Code39Extended = 8
    Code93Standard = 16
    Code93Extended = 32
    Code128 = 64
    GS1Code128 = 128
    EAN8 = 256
    EAN13 = 512
    EAN14 = 1024
    SCC14 = 2048
    SSCC18 = 4096
    UPCA = 8192
    UPCE = 16384
    ISBN = 32768
    ISSN = 65536
    ISMN = 131072
    Standard2of5 = 262144
    Interleaved2of5 = 524288
    Matrix2of5 = 1048576
    ItalianPost25 = 2097152
    IATA2of5 = 4194304
    ITF14 = 8388608
    ITF6 = 16777216
    MSI = 33554432
    VIN = 67108864
    DeutschePostIdentcode = 134217728
    DeutschePostLeitcode = 268435456
    OPC = 536870912
    PZN = 1073741824
    Code16K = 2147483648
    Pharmacode = 4294967296
    DataMatrix = 8589934592
    QR = 17179869184
    MicroQR = 0
    Aztec = 34359738368
    Pdf417 = 68719476736
    MacroPdf417 = 137438953472
    AustraliaPost = 274877906944
    Postnet = 549755813888
    Planet = 1099511627776
    OneCode = 2199023255552
    RM4SCC = 4398046511104
    DatabarOmniDirectional = 8796093022208
    DatabarTruncated = 17592186044416
    DatabarLimited = 35184372088832
    DatabarExpanded = 70368744177664
    SingaporePost = 140737488355328
    GS1DataMatrix = 281474976710656
    AustralianPosteParcel = 562949953421312
    SwissPostParcel = 1125899906842624
    EAN128 = 4503599627370496

