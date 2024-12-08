# -*- coding: utf-8 -*-
"""
   unit test of gnss ftp module.
"""
import os
from os import path
import shutil
import random
import unittest
from ppgnss import gnss_ftp


class TestFtp(unittest.TestCase):
    '''
    Unit test of ppgnss.gnss_ftp.
    '''

    def test_getftpfile(self):
        '''
        Test :func:`ppgnss.gnss_ftp.get_ftpfile()`
        '''
        remote_url = "cddis.gsfc.nasa.gov"
        remote_path = "/gps/data/daily/2017/002/17o/"
        remote_filename = "algo0020.17o.Z"
        local_tmp_download_dir = "./__tmp%.1f__" % random.random()
        local_filename = "algo0020.17o.Z"
        # "ftp://cddis.gsfc.nasa.gov/gps/data/daily/2017/002/17o/algo0020.17o.Z"

        if not path.isdir(local_tmp_download_dir):
            os.mkdir(local_tmp_download_dir)
        local_fullname = path.join(
            local_tmp_download_dir, local_filename)
        if path.isfile(local_fullname):
            os.remove(local_fullname)
        gnss_ftp.get_ftpfile(remote_url, remote_path, remote_filename,
                             local_tmp_download_dir, local_filename)
        file_exists = path.isfile(local_fullname)
        self.assertEqual(file_exists, True)
        if path.isdir(local_tmp_download_dir):
            shutil.rmtree(local_tmp_download_dir)

    def __test_derive_sp3_path_doy(self, year, doy, valid_sp3_dir,
                                   valid_sp3_file, data_center):
        sp3_path, sp3_filename = gnss_ftp.derive_sp3_path_by_doy(
            year, doy, data_center=data_center)
        self.assertEqual(sp3_filename, valid_sp3_file)
        self.assertEqual(sp3_path, valid_sp3_dir)

    def __test_derive_sp3_path_gw(self, gpsw, dow, valid_sp3_dir,
                                  valid_sp3_file, data_center):
        sp3_path, sp3_filename = gnss_ftp.derive_sp3_path_by_gw(
            gpsw, dow, data_center=data_center)
        self.assertEqual(sp3_filename, valid_sp3_file)
        self.assertEqual(sp3_path, valid_sp3_dir)

    def test_derive_sp3_path(self):
        '''
        Unit test of :func:`ppgnss.gnss_ftp.derive_sp3_path()`.
        '''
        year = 2017
        doy = 2
        gpsw = 1930
        dow = 1
        self.__test_derive_sp3_path_doy(year, doy, "/pub/gps/products/1930",
                                        "igs19301.sp3.Z", "cddis")

        self.__test_derive_sp3_path_gw(gpsw, dow, "/pub/gps/products/1930",
                                       "igs19301.sp3.Z", "cddis")

        data_center = "sopac"
        self.__test_derive_sp3_path_doy(year, doy, "/pub/products/1930",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_sp3_path_gw(gpsw, dow, "/pub/products/1930",
                                       "igs19301.sp3.Z", data_center)

        data_center = "mit"
        self.__test_derive_sp3_path_doy(year, doy, "/pub/MIT_SP3",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_sp3_path_gw(gpsw, dow, "/pub/MIT_SP3",
                                       "igs19301.sp3.Z", data_center)

        data_center = "igscb"

        self.__test_derive_sp3_path_doy(year, doy, "/igscb/product/1930",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_sp3_path_gw(gpsw, dow, "/igscb/product/1930",
                                       "igs19301.sp3.Z", data_center)

        data_center = "whu"

        self.__test_derive_sp3_path_doy(year, doy, "/pub/gps/products/1930",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_sp3_path_gw(gpsw, dow, "/pub/gps/products/1930",
                                       "igs19301.sp3.Z", data_center)

    def __test_derive_prod_path_gw(self, gpsw, dow, valid_prod_dir,
                                   valid_prod_file, data_center, ptype="sp3"):
        prod_path, prod_filename = gnss_ftp.derive_prod_path_by_gw(
            gpsw, dow, data_center=data_center, ptype=ptype)
        self.assertEqual(prod_filename, valid_prod_file)
        self.assertEqual(prod_path, valid_prod_dir)

    def __test_derive_prod_path_doy(self, year, doy, valid_prod_dir,
                                    valid_prod_file, data_center, ptype="sp3"):
        prod_path, prod_filename = gnss_ftp.derive_prod_path_by_doy(
            year, doy, data_center=data_center, ptype=ptype)
        self.assertEqual(prod_filename, valid_prod_file)
        self.assertEqual(prod_path, valid_prod_dir)

    def test_derive_prod_path(self):
        '''
        Unit test of :func:`ppgnss.gnss_ftp.derive_prod_path()`.
        '''
        year = 2017
        doy = 2
        gpsw = 1930
        dow = 1
        self.__test_derive_prod_path_doy(year, doy, "/pub/gps/products/1930",
                                         "igs19301.sp3.Z", "cddis")

        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/gps/products/1930",
                                        "igs19301.sp3.Z", "cddis")

        self.__test_derive_prod_path_doy(year, doy, "/pub/gps/products/1930",
                                         "igs19301.clk_30s.Z",
                                         "cddis", "clk_30s")

        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/gps/products/1930",
                                        "igs19301.clk_30s.Z",
                                        "cddis", "clk_30s")

        data_center = "sopac"
        self.__test_derive_prod_path_doy(year, doy, "/pub/products/1930",
                                         "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/products/1930",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_doy(year, doy, "/pub/products/1930",
                                         "igs19301.clk_30s.Z",
                                         data_center, "clk_30s")
        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/products/1930",
                                        "igs19301.clk_30s.Z",
                                        data_center, "clk_30s")
        data_center = "mit"
        self.__test_derive_prod_path_doy(year, doy, "/pub/MIT_SP3",
                                         "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/MIT_SP3",
                                        "igs19301.sp3.Z", data_center)
        try:
            self.__test_derive_prod_path_doy(year, doy, "/pub/MIT_SP3",
                                             "igs19301.clk_30s.Z",
                                             data_center, "clk_30s")
            self.__test_derive_prod_path_gw(gpsw, dow, "/pub/MIT_SP3",
                                            "igs19301.clk_30s.Z",
                                            data_center, "clk_30s")
        except ValueError as exception:
            print("no clk_30 data in %s: %s" % (data_center, str(exception)))

        data_center = "igscb"
        self.__test_derive_prod_path_doy(year, doy, "/igscb/product/1930",
                                         "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_gw(gpsw, dow, "/igscb/product/1930",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_doy(year, doy, "/igscb/product/1930",
                                         "igs19301.clk_30s.Z",
                                         data_center, "clk_30s")
        self.__test_derive_prod_path_gw(gpsw, dow, "/igscb/product/1930",
                                        "igs19301.clk_30s.Z",
                                        data_center, "clk_30s")

        data_center = "whu"

        self.__test_derive_prod_path_doy(year, doy, "/pub/gps/products/1930",
                                         "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/gps/products/1930",
                                        "igs19301.sp3.Z", data_center)
        self.__test_derive_prod_path_doy(year, doy, "/pub/gps/products/1930",
                                         "igs19301.clk_30s.Z",
                                         data_center, "clk_30s")
        self.__test_derive_prod_path_gw(gpsw, dow, "/pub/gps/products/1930",
                                        "igs19301.clk_30s.Z",
                                        data_center, "clk_30s")

    def __test_derive_brdc(self, year, doy, data_center, valid_brdc_path,
                           valid_brdc_filename):
        brdc_path, brdc_filename = gnss_ftp.derive_brdc_path(
            year, doy, data_center=data_center)
        self.assertEqual(brdc_filename, valid_brdc_filename)
        self.assertEqual(brdc_path, valid_brdc_path)

    def test_derive_brdc_path(self):
        '''
        Unit test of :func:`ppgnss.gnss_ftp.derive_brdc_path()`
        '''
        year = 2017
        doy = 2
        data_center = 'cddis'
        self.__test_derive_brdc(year, doy, data_center,
                                "/pub/gps/data/daily/2017/002/17n",
                                "brdc0020.17n.Z")

        data_center = 'sopac'
        self.__test_derive_brdc(year, doy, data_center,
                                "/pub/rinex/2017/002",
                                "auto0020.17n.Z")

        data_center = 'whu'
        self.__test_derive_brdc(year, doy, data_center,
                                "/pub/gps/data/daily/2017/002/17n/",
                                "brdc0020.17n.Z")

        data_center = 'mit'
        try:
            gnss_ftp.derive_brdc_path(
                year, doy, data_center=data_center)
        except ValueError as exception:
            self.assertEqual(
                str(exception), "no brdc data in the data center")

        data_center = 'igscb'
        try:
            gnss_ftp.derive_brdc_path(
                year, doy, data_center=data_center)
        except ValueError as exception:
            self.assertEqual(
                str(exception), "no brdc data in the data center")

    def __test_downloadbrdc(self, year, doy, local_dir, local_filename,
                            data_center, success_flag):
        local_fullname = path.join(local_dir, local_filename)
        if path.isfile(local_fullname):
            os.remove(local_fullname)
        is_success = gnss_ftp.download_brdc(year, doy, local_path=local_dir,
                                            data_center=data_center)
        file_exists = False
        if path.isfile(local_fullname):
            file_exists = True
        self.assertEqual(file_exists, success_flag)
        self.assertEqual(is_success, success_flag)
        if path.isfile(local_fullname):
            os.remove(local_fullname)

    def test_downloadbrdc(self):
        '''
        Unit test of :func:`ppgnss.gnss_ftp.download_brdc`
        '''
        year = 2017
        doy = 2
        rdm = random.random()
        tmp_download_dir = "./__tmp%.1f__" % rdm

        if not path.isdir(tmp_download_dir):
            os.mkdir(tmp_download_dir)

        data_center = "cddis"
        self.__test_downloadbrdc(
            year, doy, tmp_download_dir, "brdc0020.17n.Z", data_center, True)
        data_center = "whu"
        self.__test_downloadbrdc(
            year, doy, tmp_download_dir, "brdc0020.17n.Z", data_center, True)

        data_center = "sopac"
        self.__test_downloadbrdc(
            year, doy, tmp_download_dir, "auto0020.17n.Z", data_center, True)

        data_center = "mit"
        local_filename = path.join(tmp_download_dir, "brdc0020.17n.Z")
        if path.isfile(local_filename):
            os.remove(local_filename)
        try:
            gnss_ftp.download_brdc(
                year, doy,
                local_path=tmp_download_dir, data_center=data_center)
        except ValueError as exception:
            self.assertIn(
                "no brdc data in the data center", str(exception))
        if path.isdir(tmp_download_dir):
            shutil.rmtree(tmp_download_dir)

    def __test_downloadsp3(self, year, doy, local_dir, local_filename,
                           product, data_center, success_flag):
        local_fullname = path.join(local_dir, local_filename)
        if path.isfile(local_fullname):
            os.remove(local_fullname)
        is_success = gnss_ftp.download_sp3_by_doy(year, doy, local_dir,
                                                  local_filename, product,
                                                  data_center)
        file_exists = False
        if path.isfile(local_fullname):
            file_exists = True
        self.assertEqual(file_exists, success_flag)
        self.assertEqual(is_success, success_flag)
        if path.isfile(local_fullname):
            os.remove(local_fullname)

    def test_downloadsp3(self):
        '''
        Unit test of :func:`gnss_ftp.download_sp3`.
        '''
        year = 2017
        doy = 10
        # gpsw = 1931
        # dow = 2
        tmp_download_dir = "./__tmp%.1f__" % random.random()
        if not path.isdir(tmp_download_dir):
            os.mkdir(tmp_download_dir)

        try:
            data_center = "cddis"
            self.__test_downloadsp3(year, doy, tmp_download_dir,
                                    "igs19312.sp3.Z",
                                    "igs", data_center, True)
        except IOError as exception:
            print("IO Error When download sp3:" + str(exception))

        try:
            data_center = "sopac"
            self.__test_downloadsp3(year, doy, tmp_download_dir,
                                    "igs19312.sp3.Z",
                                    "igs", data_center, True)
        except IOError as exception:
            print("IO Error When download sp3:" + str(exception))
        try:
            data_center = "igscb"
            self.__test_downloadsp3(year, doy, tmp_download_dir,
                                    "igs19312.sp3.Z",
                                    "igs", data_center, True)
        except IOError as exception:
            print("IO Error When download sp3:" + str(exception))
        try:
            data_center = "mit"
            self.__test_downloadsp3(year, doy, tmp_download_dir,
                                    "mit19312.sp3.Z",
                                    "mit", data_center, True)
        except IOError as exception:
            print("IO Error When download sp3:" + str(exception))
            # print("Value Error When download sp3")
        try:
            data_center = "whu"
            self.__test_downloadsp3(year, doy, tmp_download_dir,
                                    "igs19312.sp3.Z",
                                    "igs", data_center, True)
        except IOError as exception:
            print("IO Error When download sp3:" + str(exception))
            # print("Value Error When download sp3")

        if path.isdir(tmp_download_dir):
            shutil.rmtree(tmp_download_dir)

    def __test_download_prod(self, year, doy, local_dir, local_filename,
                             product, data_center,
                             success_flag, ptype="sp3"):
        local_fullname = path.join(local_dir, local_filename)
        if path.isfile(local_fullname):
            os.remove(local_fullname)

        is_success = gnss_ftp.download_prod_by_doy(year, doy, local_dir,
                                                   local_filename,
                                                   product,
                                                   data_center,
                                                   ptype=ptype)
        file_exists = False
        if path.isfile(local_fullname):
            file_exists = True
        self.assertEqual(file_exists, success_flag)
        self.assertEqual(is_success, success_flag)
        if path.isfile(local_fullname) and path.getsize(local_fullname) != 0:
            os.remove(local_fullname)

    def test_downloadsp3_by_prod(self):
        '''
        Unit test of :func:`gnss_ftp.download_sp3`.
        '''
        year = 2017
        doy = 10
        # gpsw = 1931
        # dow = 2
        tmp_download_dir = "./__tmp%.1f__" % random.random()
        if not path.isdir(tmp_download_dir):
            os.mkdir(tmp_download_dir)
        try:
            data_center = "cddis"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.sp3.Z",
                                      "igs", data_center, True, "sp3")
        except IOError as exception:
            print("IO Error When download sp3:" + data_center + str(exception))

        try:
            data_center = "sopac"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.sp3.Z",
                                      "igs", data_center, True, "sp3")
        except IOError as exception:
            print("IO Error When download sp3:" + data_center + str(exception))
        try:
            data_center = "igscb"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.sp3.Z",
                                      "igs", data_center, True, "sp3")
        except IOError as exception:
            print("IO Error When download sp3:" + data_center + str(exception))
        try:
            data_center = "mit"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "mit19312.sp3.Z",
                                      "mit", data_center, True, "sp3")
        except IOError as exception:
            print("IO Error When download sp3:" + data_center + str(exception))
            # print("Value Error When download sp3")
        try:
            data_center = "whu"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.sp3.Z",
                                      "igs", data_center, True, "sp3")
        except IOError as exception:
            print("IO Error When download sp3:" + data_center + str(exception))
            # print("Value Error When download sp3")

        if path.isdir(tmp_download_dir):
            shutil.rmtree(tmp_download_dir)

    def test_downloadclk30(self):
        '''
        Unit test of :func:`gnss_ftp.download_sp3`.
        '''
        year = 2017
        doy = 10
        # gpsw = 1931
        # dow = 2
        tmp_download_dir = "./__tmp%.1f__" % random.random()
        if not path.isdir(tmp_download_dir):
            os.mkdir(tmp_download_dir)

        try:
            data_center = "cddis"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.clk_30s.Z",
                                      "igs", data_center, True, "clk_30s")
        except IOError as exception:
            print("IO Error When download clk_30 of cddis:" + str(exception))

        try:
            data_center = "sopac"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.clk_30s.Z",
                                      "igs", data_center, True, "clk_30s")
        except IOError as exception:
            print("IO Error When download clk_30 of sopac:" + str(exception))
        try:
            data_center = "igscb"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.clk_30s.Z",
                                      "igs", data_center, True, "clk_30s")
        except IOError as exception:
            print("IO Error When download clk_30 of igscb:" + str(exception))

        try:
            data_center = "whu"
            self.__test_download_prod(year, doy, tmp_download_dir,
                                      "igs19312.clk_30s.Z",
                                      "igs", data_center, True, "clk_30s")
        except IOError as exception:
            print("IO Error When download clk_30 of whu:" + str(exception))
            # print("Value Error When download sp3")

        if path.isdir(tmp_download_dir):
            shutil.rmtree(tmp_download_dir)
