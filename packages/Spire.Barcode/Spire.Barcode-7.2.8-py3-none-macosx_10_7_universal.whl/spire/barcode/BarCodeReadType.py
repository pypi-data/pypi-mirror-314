from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple

from spire.barcode import *
from ctypes import *
import abc

class BarCodeReadType(Enum):
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
    Standard2of5 = 65536
    Interleaved2of5 = 131072
    Matrix2of5 = 262144
    ItalianPost25 = 524288
    IATA2of5 = 1048576
    ITF14 = 2097152
    ITF6 = 4194304
    MSI = 8388608
    VIN = 16777216
    DeutschePostIdentcode = 33554432
    DeutschePostLeitcode = 67108864
    OPC = 134217728
    PZN = 268435456
    Pharmacode = 536870912
    DataMatrix = 1073741824
    GS1DataMatrix = 2147483648
    QR = 4294967296
    Aztec = 8589934592
    Pdf417 = 17179869184
    MacroPdf417 = 34359738368
    MicroPdf417 = 68719476736
    AustraliaPost = 137438953472
    Postnet = 274877906944
    Planet = 549755813888
    OneCode = 1099511627776
    RM4SCC = 2199023255552
    DatabarOmniDirectional = 4398046511104
    DatabarTruncated = 8796093022208
    DatabarLimited = 17592186044416
    DatabarExpanded = 35184372088832
    PatchCode = 70368744177664
    ISSN = 140737488355328
    ISMN = 281474976710656
    Supplement = 562949953421312
    AustralianPosteParcel = 1125899906842624
    SwissPostParcel = 2251799813685248
    Code16K = 4503599627370496
    AllSupportedTypes = 9007199254740992
    MicroQR = 18014398509481984

