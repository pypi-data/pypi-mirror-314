import unittest
import datetime
import numpy as np
from ppgnss import gnss_trop
from ppgnss import gnss_geodesy

class TestTrop(unittest.TestCase):
    '''
    Unit test of ppgnss.gnss_time
    '''


    def test_saasthdy(self):
        '''
        Test function :func:`gnss_time.ymd2doy()`

        '''
        p = 1000
        dlat = 48.e0*np.pi/180.e0
        hell = 200.e0
        zhd = gnss_trop.saasthyd(p, dlat, hell)
        self.assertEqual(zhd, 2.2695)

    def test_an(self):
        e = 10.9621
        Tm = 273.8720
        lbd = 2.8071
        zwd = gnss_trop.asknewet(e, Tm, lbd)
        self.assertAlmostEqual(zwd, 0.1176, 4)

    def test_read_gpt2w(self):
        xr_gpt2w = gnss_trop.read_GPT2w()
        self.assertAlmostEqual(xr_gpt2w.loc["undu", 89.5, 0.5].values, 15.05, 3)
        self.assertAlmostEqual(xr_gpt2w.loc["Hs", 66.5, 29.5].values, 281.83, 4)
        self.assertAlmostEqual(xr_gpt2w.loc["lam_B2", -89.5, 360-0.5].values, -0.2229, 5)

    def test_gpt2w(self):
        dmjd = 56141.
        lat = 48.2  # gnss_geodesy.degree2radian(48.2)
        lon = 16.37  # gnss_geodesy.degree2radian(16.37)
        hell = 156.
        xr_gpt2w = gnss_trop.read_GPT2w()
        # from ppgnss import gnss_utils
        # xr_gpt2w = gnss_utils.loadobject(r"E:\code\gpt2w\gpt2_1w.obj")
        # self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "undu"), 45.756, 3)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "dT"), -5.488, 3)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "Tm"), 273.217, 3)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "lam"), 2.636, 3)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "p"), 1003.709, 3)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "T"), 11.791, 3)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "e"), 10.257, 2)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "ah"), 0.00124, 7)
        self.assertAlmostEqual(gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, "aw"), 0.00056, 7)

    def test_get_box(self):
        lat = 48.2
        lon = 16.37
        lat_low, lat_upper, lon_left, lon_right = gnss_trop.get_box(lat, lon)

        self.assertAlmostEqual(lat_low, 47.5, 2)
        self.assertAlmostEqual(lat_upper, 48.5, 2)
        self.assertAlmostEqual(lon_left, 15.5, 2)
        self.assertAlmostEqual(lon_right, 16.5, 2)


    def test_get_nearest_grid(self):
        lat = 48.2
        lon = 16.37
        lat_nearest, lon_nearest = gnss_trop.nearest_grid(lat, lon)
        self.assertAlmostEqual(lat_nearest, 48.5)
        self.assertAlmostEqual(lon_nearest, 16.5)




