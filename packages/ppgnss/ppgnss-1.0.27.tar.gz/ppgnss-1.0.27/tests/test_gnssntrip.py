"""
   unit test of gnss ntrip module.
"""
import socket
import datetime
import unittest
from collections import defaultdict
from ppgnss import gnss_ntrip


class TestNTRIP(unittest.TestCase):
    """Unit test of ``ppgnss.gnss_ntrip``.
    """
    ntripArgs = {
        "buffer": 50,
        "caster": "rt.igs.org",
        "port": 2101,
        "user": "cavin:cavin",
        "mountpoint": "IGS01",
        "lat": 35.5,
        "lon": 120.0,
        "ssl": True,
        "verbose": False,
        "UDP_Port": 1,
        "V2": True,
        "headerFile": "headerfile",
        "headerOutput": True,
    }
    ntripClient = gnss_ntrip.NtripClient(**ntripArgs)

    def test_init(self):
        self.assertEqual(self.ntripClient.buffer, 50)
        self.assertEqual(self.ntripClient.user, "cavin:cavin")
        self.assertEqual(self.ntripClient.port, 2101)

        # test NtripClient.setPosition()
        self.ntripClient.setPosition(20 + 30 / 60., 111 + 20 / 60.)
        self.assertEqual(self.ntripClient.lonDeg, 111)
        self.assertEqual(self.ntripClient.latDeg, 20)
        self.assertAlmostEqual(self.ntripClient.lonMin, 20, 12)
        self.assertAlmostEqual(self.ntripClient.latMin, 30, 10)

    def test_getMountPointString(self):
        MountPointStr = self.ntripClient.getMountPointString()
        strconst = ("GET IGS01 HTTP/1.1\r\n"
                    "User-Agent: NTRIP JCMBsoftPythonClient/0.2\r\n"
                    "Authorization: Basic cavin:cavin\r\n"
                    "Host: rt.igs.org:2101\r\n"
                    "Ntrip-Version: Ntrip/2.0\r\n"
                    "\r\n")
        self.assertEqual(MountPointStr, strconst)

    def test_getGGAString(self):
        # 2018-05-02 10:34:05.157928
        now = datetime.datetime(2018, 5, 2, 10, 34, 5, 157)
        print(now)
        ggaString = ("GPGGA,10345.00,3530.00000000,N,12000.00000000,E,"
                     "1,05,0.19,+00400,M,1212.000,M,,")
        checksum = self.ntripClient.calcultateCheckSum(ggaString)
        strconst = "$%s*%s\r\n" % (ggaString, checksum)
        self.assertEqual(checksum, "55")
        self.assertEqual(self.ntripClient.getGGAString(now), strconst)

    def test_socket(self):
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        HOST = ""
        PORT = 50007
        error_indicator = mysocket.connect_ex(
            ("rt.igs.org", 2101))

        mysocket.settimeout(10)
        s4send = self.ntripClient.getMountPointString().encode()
        print((s4send))
        # conn, addr = mysocket.accept()
        # print(addr)
        mysocket.sendall(s4send)
        resp = mysocket.recv(4096)
        print("response")
        print(resp)
        mysocket.close()
