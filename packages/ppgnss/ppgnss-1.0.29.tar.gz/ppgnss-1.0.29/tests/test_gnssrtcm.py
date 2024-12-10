"""
   unit test of gnss rtcm module.
"""
from os import path
import unittest
from ppgnss import gnss_rtcm


class TestRTCMv3(unittest.TestCase):
    """Unit test of ``ppgnss.gnss_rtcm``.
    """

    def test_check_rtcmv3(self):
        """Unit test of ``gnss_rtcm.decode_rtcm``
        """
        RTCMv3_PREAMBLE = 0xD3
        header = chr(RTCMv3_PREAMBLE)
        flag = gnss_rtcm.check_rtcm_v3(header)
        self.assertTrue(flag)
        header = chr(RTCMv3_PREAMBLE - 1)
        flag = gnss_rtcm.check_rtcm_v3(header)
        self.assertTrue(not flag)
