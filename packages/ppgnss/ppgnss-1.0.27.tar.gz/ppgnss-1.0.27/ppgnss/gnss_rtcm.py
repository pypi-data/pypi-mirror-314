"""
   gnss_rtcm
   ------------------

   RTCM module of ppgnss. Decode RTCM data. Message Types can be decodeed.
   1. 1060
   2. 1057
   3. 1058
   4. 1019

"""
import io

RTCMv3_PREAMBLE = 0xD3


def decode_rtcm_1060(data):
    """Decoding RTCM 1060
    """


def decode_rtcm_1057(data):
    """Decoding RTCM 1057
    """


def decode_rtcm_1058(data):
    """Decoding RTCM 1058
    """


def decode_rtcm_1019(data):
    """Decoding RTCM 1019
    """


def decode_rtcm_v3(data):
    """Decode RTCM data.
    """
    if not data:
        return
    stream = io.BytesIO(data)
    while True:
        header0 = stream.read(1)
        if not check_rtcm_v3(header):
            continue
        header = stream


def check_rtcm_v3(header):
    """Decoding RTCM data block.
    """
    pre = ord(header)
    if pre != RTCMv3_PREAMBLE:
        return False
    else:
        return True
    return False
