# -*- coding: utf-8 -*-
"""
   unit test of gnss i/o module.
"""
import operator
import datetime
import unittest
from os import path
from collections import defaultdict
import numpy as np

import matplotlib.pyplot as plt

# from ppgnss import cython_extend
from ppgnss import gnss_io


import xarray as xr
import pandas as pd
from ppgnss import gnss_geodesy


class TestIO(unittest.TestCase):
    '''
    Unit test of ppgnss.gnss_time
    '''
    clock_filename = path.join(path.dirname(__file__), "data",
                               "igs19544.clk_30s")

    clock_file2 = path.join(path.dirname(__file__), "data",
                            "IGS0119530.clk")

    brdc_filename = path.join(path.dirname(__file__), "data",
                              "brdc1070.17n")
    brdc_block_filename = path.join(path.dirname(__file__), "data",
                                    "brdc_block.dat")
    derive_block_fn = path.join(path.dirname(__file__), "data",
                                "derive_block.dat")
    soltab_fn = path.join(path.dirname(__file__), "data",
                          "soltab.2017.J2000")

    ssr_91_filename = path.join(path.dirname(__file__), "data",
                                "CLK912620.17C")
    ssr_71_filename = path.join(path.dirname(__file__), "data",
                                "CLK712720.17C")
    ssr_81_filename = path.join(path.dirname(__file__), "data",
                                "CLK812750.17C")
    ssr_orbit_clock_file = path.join(path.dirname(__file__), "data",
                                     "IGS0119543.ssrC")


    def test_read_orbit_clock_file(self):
        xr_clk_ssr, xr_orb_ssr = gnss_io.read_ssr_file(
            self.ssr_orbit_clock_file)

        self.assertEqual(xr_clk_ssr.loc["2017-06-21 00:00:0.000",
                                        "G01", "C0"],
                         2.839)

        self.assertEqual(xr_orb_ssr.loc["2017-06-21 00:00:0.000",
                                        "G01", "vel_radial"],
                         0.00001)
        self.assertEqual(xr_clk_ssr.loc["2017-06-21 23:59:55.000",
                                        "G32", "C0"],
                         -0.058)
        self.assertEqual(xr_clk_ssr.loc["2017-06-21 23:59:55.000",
                                        "G32", "IODE"],
                         104)
        self.assertEqual(xr_orb_ssr.loc["2017-06-21 23:59:55.000",
                                        "G32", "vel_radial"],
                         -0.00001)

    def test_read_ssr91_file(self):
        time1 = datetime.datetime.now()
        clk_xr, orb_xr = gnss_io.read_ssr_file(self.ssr_91_filename)
        time2 = datetime.datetime.now()
        print("Reading ssr91 costs %s seconds" % str(time2 - time1))
        # check if data in xr_data is correct
        # print  clk_xr.loc["2017-09-19 20:04:45.00", 'R01']
        self.assertEqual(clk_xr.loc["2017-09-19 20:04:45.000", 'R01', 'C0'],
                         1.3211)
        self.assertEqual(orb_xr.loc["2017-09-19 20:04:45.000", 'R24',
                                    'vel_along'], 0.0005)
        self.assertEqual(clk_xr.loc["2017-09-19 23:59:45.000", 'G01', 'C0'],
                         0.1664)
        self.assertEqual(orb_xr.loc["2017-09-19 23:59:45.000", 'G08',
                                    'vel_along'], -0.0001)

    def test_read_ssr71_file(self):
        time1 = datetime.datetime.now()
        clk_xr, orb_xr = gnss_io.read_ssr_file(self.ssr_71_filename)
        time2 = datetime.datetime.now()
        print("Reading ssr71 costs", time2 - time1, " seconds")
        # check if data in xr_data is correct
        # print  clk_xr.loc["2017-09-19 20:04:45.00", 'R01']
        self.assertEqual(
            clk_xr.loc["2017-09-28 23:59:40.000", 'R01', 'C0'],
            -32.4760)
        self.assertEqual(orb_xr.loc["2017-09-28 23:59:40.000", 'R24',
                                    'vel_along'], -0.0006)
        self.assertEqual(
            clk_xr.loc["2017-09-29 00:12:45.000", 'G01', 'C0'],
            1.2264)
        self.assertEqual(orb_xr.loc["2017-09-29 00:12:50.000", 'G08',
                                    'vel_out'], -0.0001)

    def test_read_ssr81_file(self):
        time1 = datetime.datetime.now()
        clk_xr, orb_xr = gnss_io.read_ssr_file(self.ssr_81_filename)
        time2 = datetime.datetime.now()
        print("Reading ssr81 costs", time2 - time1, " seconds")
        # check if data in xr_data is correct
        # print  clk_xr.loc["2017-09-19 20:04:45.00", 'R01']
        self.assertEqual(clk_xr.loc["2017-10-01 23:59:50.000", 'G07', 'C0'],
                         0.0193)
        self.assertEqual(orb_xr.loc["2017-10-01 23:59:50.000", 'R24',
                                    'vel_along'], 0.0002)
        self.assertEqual(clk_xr.loc["2017-10-02 00:10:00.000", 'G01', 'C0'],
                         0.0316)
        self.assertEqual(orb_xr.loc["2017-10-02 00:10:00.000", 'G08',
                                    'vel_along'], 0.0001)

    def test_read_clock_file(self):
        """
        Unit test of :func:`gnss_io.read_clock_file`.
        """
        xr_data = gnss_io.read_clock_file(path.join(
            path.dirname(__file__), "data", "test4read.clk"))
        self.assertEqual(xr_data.loc['2017-06-22 00:00:00.000000', 'G01'],
                         5.612685720553e-05)
        time1 = datetime.datetime.now()
        xr_data = gnss_io.read_clock_file(self.clock_filename)
        time2 = datetime.datetime.now()
        print("Reading clock final clock (30s) cost %s seconds"
              % (time2 - time1))
        self.assertEqual(xr_data.loc['2017-06-22 00:00:00.000000', 'GPST'],
                         -6.565609270118e-09)

        self.assertEqual(xr_data.loc['2017-06-22 23:59:30.000000', 'G32'],
                         -4.466444400739e-04)

        time1 = datetime.datetime.now()
        xr_data = gnss_io.read_clock_file(self.clock_file2)
        self.assertEqual(xr_data.loc['2017-06-11 00:00:00.00000', 'G01'],
                         5.575280500000e-05)
        self.assertEqual(xr_data.loc['2017-06-11 23:59:55.000000', 'G32'],
                         -4.378776690000e-04)
        time2 = datetime.datetime.now()
        print("Reading clock IGS01 costs %s seconds" % str(time2 - time1))

    def test_parse_clock_block(self):
        """Unit test of :func:`gnss_io.parse_clock_block()`.
        """
        clock_block_filename = path.join(path.dirname(__file__), "data",
                                         "clock_block.dat")
        with open(clock_block_filename, 'r') as fread:
            xr_data = gnss_io.parse_clock_block(fread)

        self.assertEqual(xr_data.loc["2017-06-22 00:13:30.000000", 'GPST'],
                         -6.564880538813e-09)
        self.assertEqual(xr_data.loc["2017-06-22 00:13:30.000000", 'G32'],
                         -4.458731478409e-04)

    def test_read_brdc(self):
        """Unit test of :func:`gnss_io.read_brdc_file`.
        """
        brdc_file_2 = path.join(path.dirname(__file__), "data", "brdc3150.17n")
        xr_brdc = gnss_io.read_brdc_file(brdc_file_2)

        xr_brdc = gnss_io.read_brdc_file(self.brdc_filename)
        self.assertEqual(xr_brdc.loc['2017-04-17 23:59:44.0', 'G26', 'IODC'],
                         18)
        self.assertEqual(xr_brdc.loc['2017-04-17 00:00:00.0',
                                     'G01',
                                     'FitIntvl'],
                         0.400000000000E+01)

    def test_parse_brdc_block(self):
        """Unit test of :func:`gnss_io.parse_brdc_block`.
        """

        with open(self.brdc_block_filename, 'rb') as fstream:
            xr_brdc = gnss_io.parse_brdc_block(fstream)
            self.assertEqual(xr_brdc.loc['2017-04-17 00:00:00.0',
                                         'G01',
                                         'Crc'],
                             0.217125000000E+03)
            self.assertEqual(xr_brdc.loc['2017-04-17 00:00:00.0',
                                         'G32',
                                         'IODC'],
                             8)

    def test_derive_lines_nline(self):
        """Unit test of :func:`gnss_io.derive_lines`.
        """
        block_flag = {'nlines': 3}
        with open(self.brdc_block_filename, 'rb') as fstream:
            lines = gnss_io.derive_lines(fstream, block_flag)
            line1 = " 1 17  4 17  0  0  0.0 0.533713027835D-04 " \
                + "0.568434188608D-12 0.000000000000D+00\n"
            line2 = "    0.980000000000D+02-0.193125000000D+02 " \
                + "0.447947230229D-08 0.994765621215D+00\n"
            line3 = "   -0.767409801483D-06 0.646551663522D-02 "  \
                + "0.853277742863D-05 0.515368868446D+04\n"
            self.assertIn(line1, lines)
            self.assertIn(line2, lines)
            self.assertIn(line3, lines)

    def test_derive_lines_start(self):
        """Unit test of :func:`gnss_io.derive_lines`.
        """
        with open(self.derive_block_fn, 'rb') as fstream:
            block_flag = {
                'start_cond': [
                    (operator.__contains__,
                     'START OF BLOCK'),
                ],
                'stop_cond': [],
                'nlines': None
            }
            outlines = gnss_io.derive_lines(fstream, block_flag)
            valid_lines = ['START OF BLOCK\n',
                           '1 first\n',
                           '2 second\n',
                           '3 third\n',
                           '4 forth\n',
                           'BLOCK END\n',
                           '*  2011  3 11 23 45  0.00000000\n']

            self.assertEqual(valid_lines, outlines)

    def test_derive_lines_start_stop(self):
        """Test starting and stopping conditions of gnss_io.derive_lines
        """
        with open(self.derive_block_fn, 'rb') as fstream:
            block_flag = {
                'start_cond': [
                    (operator.__contains__,
                     'START OF BLOCK'),
                ],
                'stop_cond': [
                    (str.startswith, '*'),
                ],
                'nlines': None
            }
            outlines = gnss_io.derive_lines(fstream, block_flag)
            # print outlines
            valid_lines = ['START OF BLOCK\n',
                           '1 first\n',
                           '2 second\n',
                           '3 third\n',
                           '4 forth\n',
                           'BLOCK END\n',
                           '*  2011  3 11 23 45  0.00000000\n', ]

            self.assertEqual(valid_lines, outlines)

    def test_derive_lines_stop(self):
        """Test stop condition of gnss_io.derive_lines.
        """
        with open(self.derive_block_fn, 'rb') as fstream:
            block_flag = {
                'start_cond': [],
                'stop_cond': [
                    (operator.__contains__, 'BLOCK END'),
                ],
                'nlines': None}
            outlines = gnss_io.derive_lines(fstream, block_flag)
            valid_lines = ['this line CONTAINS a key word\n',
                           '*  2011  3 11 23 30  0.00000000\n',
                           'START OF BLOCK\n',
                           '1 first\n',
                           '2 second\n',
                           '3 third\n',
                           '4 forth\n',
                           'BLOCK END\n', ]

            self.assertEqual(outlines, valid_lines)

    def test_derive_lines_fallback(self):
        """Test fallback of gnss_io.derive_lines
        """
        with open(self.derive_block_fn, 'rb') as fstream:
            block_flag = {
                'start_cond': [],
                'stop_cond': [(operator.__contains__, 'BLOCK END'),
                              ],

                'nlines': None}
            outlines = gnss_io.derive_lines(fstream, block_flag, True)
            outline = fstream.readline().decode()
            self.assertEqual(outlines[-1], outline)

    def test_bat_list_op(self):
        """Test lambda of check_flag_occur.
        """
        op_contains_tuple = (operator.__contains__, 'CONTAINS')
        op_endswith_tuple = (str.endswith, "BLOCK END")
        op_endswith_zero_tuple = (str.endswith, "0.00000000")
        op_startswith_tuple = (str.startswith, "START OF")
        op_startswith_star_tuple = (str.startswith, "*")

        op_blockstart_list = [op_startswith_star_tuple,
                              op_endswith_zero_tuple]
        op_blockstop_list = [op_endswith_tuple]

        line = "*  2011  3 11 23 45  0.00000000\n"
        start_flag_occur = any([op(line.rstrip(), para)
                                for op, para in op_blockstart_list])
        self.assertTrue(start_flag_occur)

        line = "balabalabala BLOCK END"
        stop_flag_occur = any([op(line.rstrip(), para)
                               for op, para in op_blockstop_list])
        self.assertTrue(stop_flag_occur)

        op_blockstart_list = [op_contains_tuple]
        op_blockstop_list = [op_startswith_tuple]

        line = "this line CONTAINS a key word\n"
        start_flag_occur = any([op(line.rstrip(), para)
                                for op, para in op_blockstart_list])
        self.assertTrue(start_flag_occur)

        line = "START OF BLOCK"
        stop_flag_occur = any([op(line.rstrip(), para)
                               for op, para in op_blockstop_list])
        self.assertTrue(stop_flag_occur)

        # test branchs

    def test_read_sp3_file(self):
        """Unit test of :func:`gnss_io.read_sp3_file`.
        """

        filename = path.join(path.dirname(__file__), "data", "CLK8119534.sp3")
        xr_sp3 = gnss_io.read_sp3_file(filename)
        self.assertAlmostEqual(xr_sp3.loc["2017-06-15 20:05:35.00",
                                          'G30',
                                          'x'],
                               943136.154, places=4)
        self.assertAlmostEqual(xr_sp3.loc["2017-06-15 20:05:35.00",
                                          'G30',
                                          'z'].values,
                               -8381615.830, places=4)

        filename = path.join(path.dirname(__file__), "data", "igs19501.sp3")
        xr_sp3 = gnss_io.read_sp3_file(filename)

        self.assertAlmostEqual(xr_sp3.loc['2017-05-22 00:00:00.000',
                                          'G01',
                                          'x'].values,
                               22081696.734, places=4)
        self.assertAlmostEqual(xr_sp3.loc['2017-05-22 00:00:00.000',
                                          'G01',
                                          'clock'].values,
                               54962.626, places=7)

        self.assertAlmostEqual(xr_sp3.loc['2017-05-22 23:45:00.000',
                                          'G32',
                                          'x'].values,
                               -15055802.946, places=4)

        self.assertAlmostEqual(xr_sp3.loc['2017-05-22 23:45:00.000',
                                          'G32',
                                          'clock'].values,
                               -420914.752, places=7)

    def test_parse_sp3_block(self):
        """Unit test of :func:`gnss_io.parse_sp3_block()`.
        """
        block_flag = defaultdict(None)
        filename = path.join(path.dirname(__file__), "data", "igs_block.dat")
        prnlist = ['G%02d' % iprn for iprn in range(1, 33)]
        prn_order_dict = dict([(prn, idx)
                               for idx, prn in enumerate(prnlist)])
        with open(filename, 'rb') as fread:
            block_lines = gnss_io.derive_lines(fread, block_flag)
            objtime, epoch_data = gnss_io._parse_sp3_block(block_lines,
                                                           prn_order_dict)
            self.assertAlmostEqual(epoch_data[prn_order_dict['G01']][0],
                                   22081696.734, places=4)
            self.assertAlmostEqual(epoch_data[prn_order_dict['G32']][3],
                                   -420040.490, places=7)

    def test_read_soltab_file(self):
        """Unit test of :func:`gnss_io.read_soltab_file`
        """
        xr_sol = gnss_io.read_soltab_file(self.soltab_fn)
        self.assertAlmostEqual(xr_sol.loc[57661, 'x'], 149023950)
        self.assertAlmostEqual(xr_sol.loc[58217, 'z'], -18269828)

    def test_read_trimble_solution(self):
        """Unit test of :func:`gnss_io.read_trimble`.
        """
        filename = path.join(path.dirname(__file__),
                             "data", "trimble.csv")
        xr_pos = gnss_io.read_trimble_solution(filename)
        # self.assertAlmostEqual(xr_pos.loc["2018-06-09 02:56:51.0", "x"],
        #                        -2267689.5338, places=4)

    def test_delta_trimble(self):
        str_utc = "2018 06 12 10 15 41.00"
        str_tr = "1882 05 06 11 47 43"
        delta = gnss_io.delta_trimble(str_utc, str_tr)
        str_delta = str(delta)
        self.assertEqual(str_delta, "49709 days, 22:28:16")

    def test_trimble2ppishaper(self):
        dirname = "/home/octocat/data/ppi-data/2018-06-13"
        filename = path.join(dirname, "180613.csv")
        outfile = path.join(dirname, "180613.dat")
        str_start_time = "2018-06-12 23:12:00.00"
        str_end_time = "2018-06-12 23:30:00.00"

        str_utc = "2018 06 12 22 59 39.0"
        str_tr = "1882 05 07 00 31 41.0"
        delta_xyz = [-0.872196,  0.764547,  1.187464]
        delta_time = gnss_io.delta_trimble(str_utc, str_tr)
        # xr_tr = gnss_io.trimble2ppishaper(
        #     filename, outfile, str_start_time,
        #     str_end_time, delta_time, delta_xyz)
        # xr_ppi = gnss_io.read_ppi_shaper(outfile)
        # self.assertAlmostEqual(
        #     xr_ppi.loc[str_start_time, 'x'].values - delta_xyz[0],
        #     xr_tr.loc[str_start_time, 'x'].values, places=4)

        dirname = "/home/octocat/data/ppi-data/2018-06-12"
        filename = path.join(dirname, "trimble.csv")
        outfile = path.join(dirname, "trimble.dat")

        str_utc = "2018 06 12 22 59 39.0"
        str_tr = "1882 05 07 00 31 41.0"
        str_start_time = "2018-06-12T10:15:59.00"
        str_end_time = "2018-06-12T12:58:18.00"
        delta_xyz = [-0.872196,  0.764547,  1.187464]
        xr_tr = gnss_io.trimble2ppishaper(
            filename, outfile, str_start_time,
            str_end_time, delta_time, delta_xyz)
        # print(xr_tr)

    def test_trimble_ppi(self):
        # a001 2018 6 12 10 15 41.00
        # 1882/5/6 11:47:43
        # python -m unittest tests.test_gnssio.TestIO.test_trimble_ppi

        str_start_time = "2018-06-12 23:12:00.00"
        str_end_time = "2018-06-12 23:30:00.00"
        dirname = "/home/octocat/data/ppi-data/2018-06-13"
        # dirname = "/home/octocat/data/ppi-data/2018-06-12"
        ppi_fn = "102_2018-06-13.txt"
        # ppi_fn = "ublox_2018-06-13.dat"
        tr_fn = "180613.csv"
        # tr_fn = "trimble.csv"
        ppi_filename = path.join(dirname, ppi_fn)
        tr_filename = path.join(dirname, tr_fn)
        str_utc = "2018 06 12 22 59 39.0"
        str_tr = "1882 05 07 00 31 41.0"
        delta_time = gnss_io.delta_trimble(str_utc, str_tr)
        print(delta_time)
        xr_tr = gnss_io.read_trimble_solution(tr_filename, delta_time)
        # sys.exit(0)
        xr_ppi = gnss_io.read_ppi_shaper(ppi_filename)

        xr_ppi, xr_tr = xr.align(xr_ppi, xr_tr)
        xr_deltaxyz = xr_ppi - xr_tr
        print("ppix - trx: %.4f" %
              np.mean(xr_deltaxyz.loc[
                  str_start_time:str_end_time, 'x'].values))
        print("ppiy - try: %.4f" %
              np.mean(xr_deltaxyz.loc[
                  str_start_time:str_end_time, 'y'].values))
        print("ppiz - trz: %.4f" %
              np.mean(xr_deltaxyz.loc[
                  str_start_time:str_end_time, 'z'].values))
        print(np.mean(xr_deltaxyz.loc[str_start_time:str_end_time], axis=0))
        xr_neu = gnss_geodesy.xr_xyz2neu(xr_ppi, xr_tr)
        print(np.mean(xr_neu, axis=0).values)
        # xr_neu = xr_neu.diff('time')
        # errors = np.array([xr_neu.loc[:, 'n'].values,
        #                    xr_neu.loc[:, 'e'].values,
        #                    xr_neu.loc[:, 'u'].values],
        #                   dtype=np.float)
        valid_ind = xr_ppi.loc[str_start_time:str_end_time,
                               "pdop"].values < 1.5

        stdn = np.std(
            xr_neu.loc[str_start_time:str_end_time, 'n'].values[valid_ind])  # -
        # np.mean(xr_neu.loc[str_start_time:str_end_time, 'n'].values[valid_ind]))
        stde = np.std(
            xr_neu.loc[str_start_time:str_end_time, 'e'].values[valid_ind])  # -
        # np.mean(xr_neu.loc[str_start_time:str_end_time, 'e'].values[valid_ind]))
        stdu = np.std(
            xr_neu.loc[str_start_time:str_end_time, 'u'].values[valid_ind])
        #-
        # np.mean(xr_neu.loc[str_start_time:str_end_time, 'u'].values[valid_ind]))

        plt.plot(xr_neu.loc[str_start_time:str_end_time, 'n'] -
                 np.mean(xr_neu.loc[str_start_time:str_end_time, 'n']),
                 label="N:%.2f" % stdn)
        plt.plot(xr_neu.loc[str_start_time:str_end_time, 'e'] -
                 np.mean(xr_neu.loc[str_start_time:str_end_time, 'e']),
                 label="E:%.2f" % stde)
        plt.plot(xr_neu.loc[str_start_time:str_end_time, 'u'] -
                 np.mean(xr_neu.loc[str_start_time:str_end_time, 'u']),
                 label="U:%.2f" % stdu)
        plt.ylim((-5, 5))
        plt.xlabel("Epochs")
        plt.ylabel("Positioning Errors (meter)")
        plt.legend(loc="lower left")
        ax1 = plt.twinx()
        print(xr_ppi.coords)
        ax1.plot(xr_ppi.loc[str_start_time:str_end_time,
                            "pdop"], "-", label="PDOP", color='k')
        plt.legend()
        print("N: %8.3f" % stdn)
        print("E: %8.3f" % stde)
        print("U: %8.3f" % stdu)
        ax1.set_ylim((-2, 2))
        ax1.set_ylabel("PDOP")
        # plt.plot(xr_neu.loc[:, 'u'])
        # plt.plot(xr_neu.loc[:, 'e'],
        #          xr_neu.loc[:, 'n'])
        fig_filename = path.join(dirname, "%s-%s.png" % (ppi_fn, tr_fn))
        print("%s is saved!" % fig_filename)
        plt.savefig(fig_filename)

    def test_dms2dd(self):
        str_dms = "22d43'25.99823\""
        dd = gnss_io.dms2dd(str_dms)
        print(dd)
        str_dms = "114d14'39.59886\""
        print(gnss_io.dms2dd(str_dms))

    def test_read_ppi_shaper(self):
        """Unit test of :func:`gnss_io.read_ppi_shaper`.
        """
        filename = path.join(path.dirname(__file__),
                             "data", "ppi_shaper.dat")
        xr_ppi = gnss_io.read_ppi_shaper(filename)
        self.assertAlmostEqual(xr_ppi.loc["2018-06-09 02:56:51.0", "x"],
                               -2267689.5338, places=4)
        self.assertAlmostEqual(xr_ppi.loc["2018-06-09 02:56:51.0", "y"],
                               5009407.9125, places=4)
        self.assertAlmostEqual(xr_ppi.loc["2018-06-09 02:56:51.0", "z"],
                               3220934.6871, places=4)
        self.assertAlmostEqual(xr_ppi.loc["2018-06-09 01:50:56.0", "x"],
                               -2267727.0279, places=4)
        self.assertAlmostEqual(xr_ppi.loc["2018-06-09 01:50:56.0", "y"],
                               5009354.1348, places=4)
        self.assertAlmostEqual(xr_ppi.loc["2018-06-09 01:50:56.0", "z"],
                               3220999.7686, places=4)


    def test_read_ppi_v3(self):
        filename = path.join(path.dirname(__file__),
                             "data", "ppi_v3.txt")
        xr_ppi = gnss_io.read_ppi_v3(filename)

    def test_read_rtklib_solution(self):
        """Unit test of :func:`gnss_io.read_rtklib_solution`.
        """
        filename = path.join(path.dirname(__file__),
                             "data", "kine1640_rtk.pos")
        xr_pos = gnss_io.read_rtklib_solution(filename)
        self.assertAlmostEqual(xr_pos.loc["2017-06-13 16:19:59.000", 'x'],
                               -1642547.8851, places=4)
        self.assertAlmostEqual(xr_pos.loc["2017-06-13 18:24:26.000", 'z'],
                               4939972.6680, places=4)
        self.assertEqual(xr_pos.loc["2017-06-13 16:19:59.000", 'status'],
                                1)

    def test_clock2strlist(self):
        xr_data = gnss_io.read_clock_file(path.join(
            path.dirname(__file__), "data", "test4read.clk"))
        data = xr_data.values
        coord_time = xr_data.coords["time"].values
        prns = xr_data.coords["prn"].values
        first_epoch = pd.to_datetime(coord_time[0])
        secs = (coord_time - coord_time[0])/np.timedelta64(1, "s")
        tmp = cython_extend.clock2strlist(data, list(secs), list(prns), first_epoch)
        self.assertEqual(len(tmp), 10292)

    def test_xrclk2list(self):
        xr_data = gnss_io.read_clock_file(path.join(
            path.dirname(__file__), "data", "test4read.clk"))
        lst_data = gnss_io._xr_clock2list(xr_data)
        # print(lst_data[0])
        self.assertEqual(lst_data[0][0], 2017)
        self.assertEqual(lst_data[0][1], 6)
        self.assertEqual(lst_data[0][2], 22)
        self.assertEqual(lst_data[0][3], 0)
        self.assertEqual(lst_data[0][4], 0)
        self.assertEqual(lst_data[0][5], 0)
        self.assertEqual(lst_data[1][1], 30)
        self.assertEqual(lst_data[1][2], 60)
        self.assertEqual(lst_data[2][0][0], 5.612685720553e-05)

    def test_clk2strlist(self):
        xr_data = gnss_io.read_clock_file(path.join(
            path.dirname(__file__), "data", "test4read.clk"))
        # lst_data = gnss_io._xr_clock2list(xr_data)
        t0 = datetime.datetime.now()
        list1 = gnss_io._xr_clock2lines(xr_data)
        t1 = datetime.datetime.now()
        list2 = gnss_io._xr_clock2listsCython(xr_data)
        t2 = datetime.datetime.now()
        # print("python: %s" % str(t1 - t0))
        # print("cython: %s" % str(t2 - t1))

    def test_save_clock_file(self):
        """Unit test of :func:`gnss_io.save_clock_file`
        """
        inclkfn = self.clock_filename
        outclkfn = path.join(path.dirname(__file__), "data", "test4save.clk")
        prns = ['G%02d' % tmp for tmp in range(1, 33)]
        time0 = datetime.datetime.now()
        xr_clock = gnss_io.read_clock_file(inclkfn)
        time1 = datetime.datetime.now()
        print("Reading clock costs %s to read." % str(time1 - time0))
        gnss_io.save_clock_file(outclkfn, xr_clock, prns)
        time2 = datetime.datetime.now()
        print("Reading clock costs %s to write" % str(time2 - time1))
        xr_clock2 = gnss_io.read_clock_file(outclkfn)
        self.assertEqual(
            xr_clock.loc["2017-06-22 23:59:30.000000", "G32"].values,
            xr_clock2.loc["2017-06-22 23:59:30.000000", "G32"].values)
        self.assertEqual(
            xr_clock.loc["2017-06-22 00:00:00.000000", "G01"].values,
            xr_clock2.loc["2017-06-22 00:00:00.000000", "G01"].values)
    def test_read_generic_solution(self):
        infile = path.join(path.dirname(__file__), "data",
                               "sppout.pos")
        xr_pos = gnss_io.read_solution(infile)
        self.assertAlmostEqual(xr_pos.loc["2018-08-18 11:36:30.0", "x"].values,
                         -2148782.458, places=4)


    def test_read_f107(self):
        filename = path.join(path.dirname(__file__), "data",
                            "f10.7.data")
        xr_f107 = gnss_io.read_f107(filename)
        self.assertAlmostEqual(xr_f107.loc["2015-01-01 00:00:00"].values,
                               132.9,
                               places=1)
        self.assertAlmostEqual(xr_f107.loc["2022-12-31 23:00:00"].values,
                               159.5,
                               places=1)

    def test_read_dst(self):
        filename = path.join(path.dirname(__file__), "data",
                            "dst.data")
        xr_dst = gnss_io.read_dst(filename)
        self.assertEqual(xr_dst.loc["2015-11-01 00:00:00.000"].values,
                               -17)
        self.assertEqual(xr_dst.loc["2016-12-31 23:00:00"].values,
                         -9)

    def test_read_iri_web(self):

        iri_webfile = path.join(path.dirname(__file__), "data",
                                "I16_2019_001_02.TAB") # IRI2016
        xr_iri = gnss_io.read_iri_web(iri_webfile)
        self.assertAlmostEqual(xr_iri.loc["2019-01-01 02:00:00", -67.5,160].values,
                               10.3,
                               places=2)

        self.assertAlmostEqual(xr_iri.loc["2019-01-01 02:00:00", 60, -50].values,
                               0.7,
                               places=2)


        iri_webfile = path.join(path.dirname(__file__), "data",
                                "I20_2019_001_00.TAB")  # IRI2020
        xr_iri = gnss_io.read_iri_web(iri_webfile)

        self.assertAlmostEqual(xr_iri.loc["2019-01-01 00:00:00", 5, 130].values,
                               17.2,
                               places=2)
        self.assertAlmostEqual(xr_iri.loc["2019-01-01 00:00:00", -22.5, -60].values,
                               12.2,
                               places=2)


    def test_read_anubis(self):
        anubis_file = path.join(path.dirname(__file__), "data",
                                "B2163520_2021.xtr")
        xr_els, xr_azis, xr_snrs = gnss_io.read_anubis(anubis_file)

        anubis_file = path.join(path.dirname(__file__), "data",
                              "PD02104.xtr")
        xr_eles, xr_azis, xr_snrs = gnss_io.read_anubis(anubis_file)
        self.assertEqual(xr_eles.loc["GPS", "2022-04-14 00:03:30", "03"].values,
                               23)
        self.assertEqual(xr_eles.loc["GLO", "2022-04-14 12:05:30", "04"].values,
                         33)
        self.assertEqual(xr_azis.loc["GPS", "2022-04-14 00:03:30", "03"].values,
                         260)
        self.assertEqual(xr_snrs.loc["GPSS1C", "2022-04-14 00:03:30", "03"].values,
                         34)
        self.assertEqual(xr_snrs.loc["BDSS7I", "2022-04-14 17:28:30", "08"].values,
                         48)

    def test_sec2time(self):
        sec = 85260
        seconds_in_day = 86400
        preday_max_sec = seconds_in_day - 30 * 60
        iline = 0
        linenum = 1000
        dt = gnss_io._sec2time(sec, np.datetime64("2023-04-10"), (sec>preday_max_sec)&(iline<linenum))


    def test_code2prn(self):
        code = "4"
        prn = gnss_io._code2prn("  4")
        self.assertEqual(prn, "G04")

        prn = gnss_io._code2prn("103")
        self.assertEqual(prn, "R03")

    def test_check_if_cur_day(self):
        sec = 15
        iline = 69572
        which_day = gnss_io._check_if_cur_day(sec, iline, 69585)
        self.assertEqual(which_day, gnss_io.DELTA_DAY.IS_NXTDAY)

        sec = 15
        iline = 0
        which_day = gnss_io._check_if_cur_day(sec, iline, 69585)
        self.assertEqual(which_day, gnss_io.DELTA_DAY.IS_CURDAY)

        sec = 85400
        iline = 90
        which_day = gnss_io._check_if_cur_day(sec, iline, 69585)
        self.assertEqual(which_day, gnss_io.DELTA_DAY.IS_PREDAY)

        sec = 86385
        iline = 69571
        which_day = gnss_io._check_if_cur_day(sec, iline, 69585)
        self.assertEqual(which_day, gnss_io.DELTA_DAY.IS_CURDAY)


    def test_read_refl_snr3(self):
        refl_snr_file = path.join(path.dirname(__file__), "data",
                              "jfng3560.17.snr88")
        xr_snr = gnss_io.read_refl_snr(refl_snr_file, np.datetime64("2017-11-22"))
        self.assertAlmostEqual(xr_snr.loc["2017-11-22 00:02:30", "G02", "ele"].values,
                               64.4942,
                               places=4)
        self.assertAlmostEqual(xr_snr.loc["2017-11-22 00:02:30", "G02", "S1"].values,
                               49,
                               places=4)

        self.assertAlmostEqual(xr_snr.loc["2017-11-22 00:00:30", "G05", "ele"].values,
                               65.7710,
                               places=4)
        self.assertAlmostEqual(xr_snr.loc["2017-11-22 00:00:30", "G05", "S1"].values,
                               52.40,
                               places=4)

    def test_read_refl_snr2(self):
        refl_snr_file = path.join(path.dirname(__file__), "data",
                              "pd021440.22.snr88")
        xr_snr = gnss_io.read_refl_snr(refl_snr_file, np.datetime64("2023-05-24"))
        self.assertAlmostEqual(xr_snr.loc["2023-05-24 00:00:15", "G04", "ele"].values,
                               37.4537,
                               places=4)
        self.assertAlmostEqual(xr_snr.loc["2023-05-24 00:00:15", "G04", "S1"].values,
                               47,
                               places=4)

        self.assertAlmostEqual(xr_snr.loc["2023-05-25 00:00:15", "G04", "ele"].values,
                               35.7868,
                               places=4)
        self.assertAlmostEqual(xr_snr.loc["2023-05-25 00:00:15", "G04", "S1"].values,
                               46,
                               places=4)


    def test_read_refl_snr(self):
        refl_snr_file = path.join(path.dirname(__file__), "data",
                              "pd021000.23.snr88")
        xr_snr = gnss_io.read_refl_snr(refl_snr_file, np.datetime64("2023-04-10"))
        self.assertAlmostEqual(
            xr_snr.loc["2023-04-10 00:00:30", "G04", "ele"].values,
            47.8648,
            places=4)
        self.assertAlmostEqual(
            xr_snr.loc["2023-04-10 00:00:30", "G04", "azi"].values,
            306.0612,
            places=4)
        self.assertAlmostEqual(
            xr_snr.loc["2023-04-10 00:00:30", "G04", "S1"].values,
            45,
            places=2)
        self.assertAlmostEqual(
            xr_snr.loc["2023-04-10 00:00:30", "G04", "S2"].values,
            47,
            places=2)
        self.assertAlmostEqual(
            xr_snr.loc["2023-04-10 23:59:45", "R17", "S1"].values,
            41,
            places=2
        )

    def test_read_iono_file(self):
        iono_file = path.join(path.dirname(__file__), "data",
                              "tsk22300.pos.iono")
        xr_iono = gnss_io.read_iono_file(iono_file)
        self.assertAlmostEqual(
            xr_iono.loc["2018-08-18 00:00:00.0", "G01"].values,
                               19.4733, places=4)
        self.assertAlmostEqual(
            xr_iono.loc["2018-08-18 23:55:30.0", "G01"].values,
                               12.5078, places=4)

    def test_read_ionex(self):
        gim_file = path.join(path.dirname(__file__), "data", "CODG2180.15I")
        xr_gim = gnss_io.read_ionex_file(gim_file)
        self.assertAlmostEqual(
            xr_gim.loc["2015-08-06 00:00:00", 87.5, -180].values,
            15.2, places=1
        )
        self.assertAlmostEqual(
            xr_gim.loc["2015-08-07 00:00:00", 85.0, -180].values,
            10.9, places=1
        )
        self.assertAlmostEqual(xr_gim.loc["2015-08-07 00:00:00", -85.0, -180].values,
            2.9, places = 1)

    def test_read_orbit_file(self):
        orbit_file = path.join(path.dirname(__file__), "data",
                               "nium1350.pos.orbit")
        xr_orbit = gnss_io.read_orbit_file(orbit_file)
        self.assertAlmostEqual(
            xr_orbit.loc["2018-05-15 00:00:00.0", "G32", "z"].values,
            9103778.4452,
            places=4)
        self.assertAlmostEqual(
            xr_orbit.loc["2018-05-15 23:59:30.0", "G05", "x"].values,
            -2837330.5703,
            places=4)

    def test_read_dcb_liu_file(self):
        dcb_file = path.join(path.dirname(__file__), "data",
                             "2018_132_DCB_ns.txt")
        dcb_data = gnss_io.read_dcb_liu(dcb_file)
        self.assertAlmostEqual(dcb_data["G01"], -8.00073)
        self.assertAlmostEqual(dcb_data["yar2"], -3.3468)


    def test_read_ION_file(self):
        ion_file = path.join(path.dirname(__file__), "data",
                             "COD19994.ION")
        xr_coeff = gnss_io.read_ION_file(ion_file)
        self.assertAlmostEqual(xr_coeff.loc["2018-05-03 00:00:00.00",
                               0, 0, "a"].values, 8.92296483)
        self.assertAlmostEqual(xr_coeff.loc["2018-05-03 00:00:00.00",
                               15, 15, "b"].values, 0.00229872)
        self.assertAlmostEqual(xr_coeff.loc["2018-05-04 00:00:00.00",
                               0, 0, "a"].values, 8.64139963)
        self.assertAlmostEqual(xr_coeff.loc["2018-05-04 00:00:00.00",
                               15, 15, "b"].values, -0.00043999)

    def test_read_gim_file(self):
        gim_file = path.join(path.dirname(__file__), "data",
                             "CODG1230.18I")
        xr_gim = gnss_io.read_ionex_file(gim_file)
        self.assertAlmostEqual(xr_gim.loc["2018-05-03 00:00:00.00",
                                          87.5,
                                          -180].values,
                               65.)
        self.assertAlmostEqual(xr_gim.loc["2018-05-04 00:00:00.00",
                                          -87.5,
                                          180].values, 8)


    def test_read_snx_file(self):
        vlbi_snx_filename = path.join(path.dirname(__file__), "data",
                                      "19APR01VG_bkg2023a.snx")
        
        snx_data = gnss_io.read_sinex(vlbi_snx_filename)
        self.assertAlmostEqual(snx_data["SOLUTION/DECOMPOSED_NORMAL_MATRIX"][0, 0], 1.01572632138898E+07, 12)
        self.assertAlmostEqual(snx_data["SOLUTION/DECOMPOSED_NORMAL_MATRIX"][-1, -1], 4.79886305168675E+03, 12)
        self.assertAlmostEqual(snx_data["SOLUTION/DECOMPOSED_NORMAL_VECTOR"][-1], -8.27254242632016E+02, 12)
        self.assertAlmostEqual(snx_data["SOLUTION/ESTIMATE"]["value"].iloc[-1], -3.73072581764289E+03, 12)
        self.assertAlmostEqual(snx_data["SOLUTION/ESTIMATE"]["value"].iloc[0], 1.13072988730168E+06, 12)
        
        gnss_snx_filename = path.join(path.dirname(__file__), "data",
                                      "GFZ0OPSRAP_20242930000_01D_01D_SOL.SNX")
        snx_data = gnss_io.read_sinex(gnss_snx_filename)
        self.assertAlmostEqual(snx_data["SOLUTION/STATISTICS"]["FACTOR"], 0.787946977315325E-4, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/STATISTICS"]["VTPV"], 0.192814959057435E+03, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/APRIORI"]["value"].iloc[393], .278010295810383278E7, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/MATRIX_ESTIMATE L CORR"][-1, -1], .12789904202351351E-2, 15)
        
        gnss_snx_filename = path.join(path.dirname(__file__), "data",
                                      "ESA0OPSFIN_20242880000_01D_01D_SOL.SNX")
        snx_data = gnss_io.read_sinex(gnss_snx_filename)
        self.assertAlmostEqual(snx_data["SOLUTION/STATISTICS"]["VTPV"], 0.399263112240990E+07, 15)
        self.assertEqual(snx_data["SOLUTION/STATISTICS"]["OBSERVATIONS"], 1755432)
        self.assertAlmostEqual(snx_data["SOLUTION/ESTIMATE"]["value"].iloc[-1], 0.439195582544929E+07, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/APRIORI"]["value"].iloc[-1], 0.439195582111156E+07, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/MATRIX_APRIORI L INFO"][-1, -1], 0.100000000000000E+01, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/NORMAL_EQUATION_MATRIX L"][-1, -1], 0.672282462496738E+06, 15)
        self.assertAlmostEqual(snx_data["SOLUTION/NORMAL_EQUATION_VECTOR"]["value"].iloc[-1], -.227496700227827E+04, 15)
        
        gnss_snx_filename = path.join(path.dirname(__file__), "data",
                                      "MIT0OPSFIN_20242930000_01D_01D_SOL.SNX")
        
        snx_data = gnss_io.read_sinex(gnss_snx_filename)
        print(snx_data["SOLUTION/ESTIMATE"].tail())
        print(snx_data.keys())
        