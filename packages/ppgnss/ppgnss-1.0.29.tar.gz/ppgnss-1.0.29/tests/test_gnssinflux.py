# -*- coding: utf-8 -*-
"""
   unit test of gnss influx module.
"""
import os
from os import path
import shutil
import unittest

from influxdb import InfluxDBClient

from ppgnss import gnss_influx


class TestInflux(unittest.TestCase):
    """
    Unit test of ppgnss.gnss_influx
    """
    host = "localhost"
    port = 8086
    user = "lzhang"
    passwd = "lzhang"
    dbname = "test1"
    ssr_91_filename = path.join(path.dirname(
        __file__), "data", "CLK912620.17C")
    client = InfluxDBClient(host, 8086, user, passwd, dbname)

    def test_handle_SSR(self):
        """Test insert, query, remove record from Influx
        """
        fields = {"C0": 0.1,
                  "C1": 0.2,
                  "C2": 0.3}
        IODE = 99
        timestamp = "2017-06-21T00:00:00.0"
        measurement = "RTS_CLOCK_SSR"
        mount = "CLK00"
        prn = "G00"
        gnss_influx.insertSSR(self.client, fields, measurement,
                              mount, timestamp, prn, IODE)
        records = list(gnss_influx.querySSR(
            self.client, measurement=measurement, tags={"MOUNT": mount}))
        self.assertTrue(len(records), 1)
        self.assertEqual(records[0]["PRN"], prn)
        self.assertEqual(records[0]["IODE"], "%d" % IODE)
        self.assertEqual(records[0]["time"], "2017-06-21T00:00:00Z")
        self.assertEqual(records[0]["C0"], fields["C0"])
        self.assertEqual(records[0]["C1"], fields["C1"])
        self.assertEqual(records[0]["C2"], fields["C2"])
        self.assertEqual(records[0]["MOUNT"], mount)
        gnss_influx.deleteSSR(self.client, measurement, tags={"MOUNT": mount})
        records = list(gnss_influx.querySSR(
            self.client, mount, measurement=measurement))
        self.assertEqual(len(records), 0)
