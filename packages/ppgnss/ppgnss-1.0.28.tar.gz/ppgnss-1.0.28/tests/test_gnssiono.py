import  unittest
import os
from os import path

import numpy as np
from ppgnss import gnss_iono
from ppgnss import gnss_io
import ppgnss.gnss_geodesy as gg



class TestIono(unittest.TestCase):
    def test_calculate_ipp(self):
        site = {
            "x": 5937160.883447,
            "y": 1054675.266102,
            "z": 2071386.048307,
        }

        sat = {"x": 2914689.1575,
               "y": 25573546.4781,
               "z": 6187123.8898,
               }
        lat_ipp, lon_ipp, fac_to_stec = gnss_iono.calculate_ipp(site, sat, alpha=1)
        lat_ipp2, lon_ipp2 = gnss_iono.calculate_intersect(sat, site)

        print(lat_ipp, lat_ipp2)
        print(lon_ipp, lon_ipp2)
        self.assertAlmostEqual(lat_ipp[0], -0.3279952993687434, 12)
        self.assertAlmostEqual(lon_ipp[0], -2.9473298285608172, 12)
        self.assertAlmostEqual(fac_to_stec[0], 1.0244719935552744, 12)  #  1.0255951572252258, 12)


    def test_calculate_xripp(self):
        orbit_file = path.join(path.dirname(__file__), "data",
                               "nium1350.pos.orbit")
        xr_orbit = gnss_io.read_orbit_file(orbit_file)
        site = {
            "x": -5937160.883447,
            "y": -1054675.266102,
            "z": -2071386.048307,
        }

        # xr_ipp = gnss_iono.calculate_xr_ipp(xr_orbit, site)
        xr_ipp = gnss_iono.calculate_xr_intersect(xr_orbit, site)
        print(xr_orbit.loc["2018-05-15 00:00:00.00",
                                          "G05"])
        print(xr_ipp.loc["2018-05-15 00:00:00.00",
                                          "G05"])
        self.assertAlmostEqual(xr_ipp.loc["2018-05-15 00:00:00.00",
                                          "G05", "lat"].values,
                               -0.11586472, 12)
        self.assertAlmostEqual(xr_ipp.loc["2018-05-15 23:59:30.00",
              "G15",
              "el"].values, 46.248789494029, 9)


    def test_norm_legendre(self):
        p_nm, n_nm, norm_p = gnss_iono.norm_legendre(3, 3, .5)
        self.assertAlmostEqual(n_nm[1, 1], 1.7320508)
        self.assertAlmostEqual(p_nm[1, 1], -0.87758256 )


    def test_normalize(self):
        self.assertAlmostEqual(gnss_iono.normalize(1, 1), 1.7320508075688772)
        self.assertAlmostEqual(gnss_iono.normalize(1, 0), 1.7320508075688772)
        self.assertAlmostEqual(gnss_iono.normalize(2, 0), 2.23606797749979)


    def test_get_sin_cos_mat(self):
        cos_mat, sin_mat = gnss_iono.get_cos_sin_mat(2, gg.GEO_PI/2)
        self.assertAlmostEqual(cos_mat[0, 0], 1)
        self.assertAlmostEqual(cos_mat[1, 0], 0)
        self.assertAlmostEqual(sin_mat[0, 0], 0)
        self.assertAlmostEqual(sin_mat[1, 0], 1)


    def test_create_design_vec(self):
        design_mtrx = gnss_iono.create_design_vec(2, gg.GEO_PI/4, gg.GEO_PI/3)
        self.assertAlmostEqual(design_mtrx[ 1], 0.61237244)
        self.assertAlmostEqual(design_mtrx[11], 0.83852549)

    def test_create_design_mtrx(self):
        betas = [gg.GEO_PI/2, gg.GEO_PI/3, gg.GEO_PI/4]
        ss = [gg.GEO_PI/4, gg.GEO_PI/3, gg.GEO_PI/2]
        design_mtrx = gnss_iono.create_desiga_mtrx(3, betas, ss)
        nrow, ncol = design_mtrx.shape
        self.assertEqual(nrow, 3)
        self.assertEqual(ncol, 10+6)

    def test_xr_coef2grid(self):
        ion_file = path.join(path.dirname(__file__), "data",
                             "COD19994.ION")
        xr_coef = gnss_io.read_ION_file(ion_file)
        gnss_iono.xr_coef2grid(xr_coef)