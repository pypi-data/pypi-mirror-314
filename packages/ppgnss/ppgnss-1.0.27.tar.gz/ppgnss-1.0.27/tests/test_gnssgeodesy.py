# -*- coding: utf-8 -*-
"""
   unit test of gnss time module.
"""
import unittest
from os import path
import numpy as np
import xarray as xr
from ppgnss import gnss_geodesy
from ppgnss import gnss_io
from ppgnss import gnss_utils

class TestGeodesy(unittest.TestCase):
    '''
    Unit test of ppgnss.gnss_geodesy
    '''

    def test_deg2rad(self):
        '''
        Test the function :func:`gnss_geodesy.degree2rad()`.
        '''
        for k in [.25, .5, .75, 1., 1.5, 2]:
            deg = 180. * k
            rad = gnss_geodesy.degree2radian(deg)
            self.assertAlmostEqual(
                rad, gnss_geodesy.GEO_PI * k, places=12)

    def test_rad2deg(self):
        '''
        Test the function :func:`gnss_geodesy.rad2degree()`.
        '''
        for k in [.25, .5, .75, 1., 1.5, 2]:
            rad = gnss_geodesy.GEO_PI * k
            deg = gnss_geodesy.radian2degree(rad)
            self.assertAlmostEqual(deg, 180. * k, places=12)

    def test_fdms2dms(self):
        '''
        Test the function :func:`gnss_geodesy.fdms2dms()`.
        '''
        degree, minute, second = gnss_geodesy.fdms2dms(30.1742577079)
        self.assertEqual(degree, 30)
        self.assertEqual(minute, 17)
        self.assertEqual(second, 42.577079)

        degree, minute, second = gnss_geodesy.fdms2dms(-110.13233343)
        self.assertEqual(degree, -110)
        self.assertEqual(minute, 13)
        self.assertEqual(second, 23.3343)

    def test_fdms2dd(self):
        '''
        Test the function :func:`gnss_geodesy.fdms2dd()`.
        '''
        dec_degree = gnss_geodesy.fdms2dd(30.1742577079)
        self.assertAlmostEqual(
            dec_degree, 30.295160299722223, places=12)

        dec_degree = gnss_geodesy.fdms2dd(-110.13233343)
        self.assertAlmostEqual(
            dec_degree, -110.22314841666667, places=12)

    def test_xyz2blh(self):
        '''
        Test the function :func:`gnss_geodesy.xyz2blh()`.
        '''
        latitude, longitude, height = gnss_geodesy.xyz2blh(
            gnss_geodesy.ELLIPSOIDS['wgs84']['a'], 0., 0., 'wgs84')
        self.assertEqual(latitude, 0.)
        self.assertEqual(longitude, 0.)
        self.assertEqual(height, 0.)
        latitude, longitude, height = gnss_geodesy.xyz2blh(
            0, gnss_geodesy.ELLIPSOIDS['wgs84']['a'], 0., 'wgs84')
        self.assertEqual(latitude, 0.)
        self.assertEqual(longitude, 90.)
        self.assertEqual(height, 0)


    def test_get_solar_coord(self):
        """Test the function :func:`gnss_geodesy.get_solar_coords`.
        """
        soltab_filename = path.join(path.dirname(__file__),
                                    "data", "soltab.2017.J2000")
        solar_x, solar_y, solar_z = gnss_geodesy.get_solar_coord(
            57661, soltab_filename)
        self.assertEqual(solar_x, 149023950)
        self.assertEqual(solar_y, 14491419)
        self.assertEqual(solar_z, 6281382)

    def test_xyz2rac(self):
        """Unit test of :func:`gnss_geodesy.xyz2rac`
        """
        xyz = [0, 0, 1]
        vel = [1, 1, 0]
        dxyz = [1, 1, 1]
        vec_rac = gnss_geodesy.xyz2rac(xyz, vel, dxyz)
        self.assertAlmostEqual(np.linalg.norm(vec_rac), np.linalg.norm(dxyz))
        self.assertAlmostEqual(vec_rac[0], 1, places=7)
        self.assertAlmostEqual(vec_rac[1], np.sqrt(2), places=7)
        self.assertAlmostEqual(vec_rac[2], 0., places=7)

    # def test_xr_xyz2rac(self):
    #     """Unit test of :func:`gnss_geodesy.xr_xyz2rac`.
    #     Not working.
    #     """
    #     return
    #     igs01_obj_fn = path.join(path.dirname(__file__),
    #                              "data", "xr_igs01_sp3.obj")
    #     clk01_obj_fn = path.join(path.dirname(__file__),
    #                              "data", "xr_clk01_sp3.obj")
    #     xr_clk01 = gnss_utils.loadobject(clk01_obj_fn)
    #     xr_igs01 = gnss_utils.loadobject(igs01_obj_fn)
    #     xr_error = xr_clk01 - xr_igs01
    #     vel_upper = xr_igs01.diff('time', label='upper')
    #     vel_lower = xr_igs01.diff('time', label='lower')
    #     xr_vel = (vel_upper + vel_lower) / 2
    #     xr_rac = gnss_geodesy.xr_xyz2rac(xr_igs01, xr_vel, xr_error)
    #     timestamp = '2017-06-13 00:15:00.000'
    #     error_xyz = np.linalg.norm(xr_error.loc[timestamp,
    #                                             'G01'].values[:3])
    #     error_rad = np.linalg.norm(xr_rac.loc[timestamp,
    #                                           'G01'].values[:3])
    #     self.assertAlmostEqual(error_xyz, error_rad, places=5)

    def test_adjust_vel(self):
        """Unit test of :func:`gnss_geodesy.adjust_vel`
        """
        xyz = [19710607.5990, 13855611.9860, -11598351.3600]
        vel = [-1296327.0920, -175786.6760, -2418353.8145]
        new_vel = gnss_geodesy.adjust_vel(xyz, vel)
        dot_prod = sum([x * v for x, v in zip(xyz, new_vel)])
        sin_theta = dot_prod / (np.linalg.norm(xyz) * np.linalg.norm(vel))
        self.assertAlmostEqual(sin_theta, 0, places=15)

    # def test_xr_adjust_vel(self):
    #     """Unit test of :func:`gnss_geodesy.xr_adjust_vel`.
    #     """
    #     return
    #     igs01_obj_fn = path.join(path.dirname(__file__),
    #                              "data", "xr_igs01_sp3.obj")
    #     xr_igs01 = gnss_utils.loadobject(igs01_obj_fn)
    #     xr_igs01 = xr_igs01.drop('clock', 'data')
    #     vel_upper = xr_igs01.diff('time', label='upper')
    #     vel_lower = xr_igs01.diff('time', label='lower')
    #     xr_vel = (vel_upper + vel_lower) / 2

    #     xr_new_vel = gnss_geodesy.xr_adjust_vel(xr_igs01, xr_vel)
    #     xr_sin_theta = np.sum(xr_new_vel * xr_igs01, axis=2) \
    #         / (np.linalg.norm(xr_igs01) * np.linalg.norm(xr_new_vel))
    #     self.assertTrue((abs(xr_sin_theta) < 1e-15).all())

    # def test_xyz2rac2(self):
    #     """Unit test of :func:`gnss_geodesy.xyz2rac2`
    #     """
    #     return
    #     xr_vel = gnss_utils.loadobject(path.join(path.dirname(__file__),
    #                                              "data", "xyz2rac2.vel"))
    #     xr_xyz = gnss_utils.loadobject(path.join(path.dirname(__file__),
    #                                              "data", "xyz2rac2.xyz"))
    #     xr_dxyz = gnss_utils.loadobject(path.join(path.dirname(__file__),
    #                                               "data", "xyz2rac2.dxyz"))

    #     xr_rac2 = gnss_geodesy.xr_xyz2rac2(xr_xyz, xr_vel, xr_dxyz)

    #     norm_rac = np.linalg.norm(xr_rac2, axis=2)
    #     norm_xyz = np.linalg.norm(xr_dxyz, axis=2)
    #     for rac_epoch, xyz_epoch in zip(norm_rac, norm_xyz):
    #         for rac_sat, xyz_sat in zip(rac_epoch, rac_epoch):
    #             if np.isnan(rac_sat):
    #                 self.assertTrue(np.isnan(xyz_sat))
    #             else:
    #                 self.assertEqual(rac_sat, xyz_sat)

    # def test_xyz2rac2_2(self):
    #     """Unit test of :func:`gnss_geodesy.xyz2rac2`
    #     """
    #     return
    #     xr_clk = gnss_utils.loadobject(path.join(path.dirname(__file__),
    #                                              "data", "CLK0119544.obj"))
    #     xr_igs = gnss_utils.loadobject(path.join(path.dirname(__file__),
    #                                              "data", "igs19544.obj"))

    #     xr_xyz = xr_igs.copy(deep=True)
    #     xr_xyz = xr_xyz[-10:]
    #     xr_clk = xr_clk.drop("clock", "data")
    #     xr_xyz = xr_xyz.drop("clock", "data")
    #     xr_dxyz = xr_clk - xr_xyz

    #     xr_vel_upper = xr_xyz.diff('time', label='upper')
    #     xr_vel_lower = xr_xyz.diff('time', label='lower')
    #     xr_vel = (xr_vel_lower + xr_vel_upper) / 2
    #     xr_vel = gnss_geodesy.xr_adjust_vel(xr_xyz, xr_vel)

    #     xr_xyz, xr_dxyz, xr_vel = xr.align(
    #         xr_xyz, xr_dxyz, xr_vel, join="inner")
    #     xr_rac = gnss_geodesy.xr_xyz2rac2(xr_xyz, xr_vel, xr_dxyz)
    #     self.assertTrue(np.all(np.isnan(xr_rac[0, 0])))

    def test_xr_xyz2neu(self):
        """Unit test of :func:`gnss_geodesy.xr_xyz2neu`
        """
        rtk_filename = path.join(path.dirname(__file__),
                                 "data", "kine1640_rtk.pos")
        ppp_filename = path.join(path.dirname(__file__),
                                 "data", "kine_CLK70_164.pos")
        xr_ref = gnss_io.read_rtklib_solution(rtk_filename)
        xr_ppp = gnss_io.read_rtklib_solution(ppp_filename)
        # print(xr_ref[-4:])
        xr_neu = gnss_geodesy.xr_xyz2neu(xr_ppp, xr_ref)
        self.assertAlmostEqual(
            xr_neu.loc["2017-06-13 16:19:59", 'n'].values, 0.311836, places=4)

    def test_xr_xyz2blh(self):
        """Unit test of :func:`gnss_geodesy.xr_xyz2blh`
        """
        rtk_filename = path.join(path.dirname(__file__),
                                 "data", "kine1640_rtk.pos")
        xr_xyz = gnss_io.read_rtklib_solution(rtk_filename)
        blh_mat = gnss_geodesy.arr_xyz2blh(xr_xyz.loc[:, 'x'].values,
                                           xr_xyz.loc[:, 'y'].values,
                                           xr_xyz.loc[:, 'z'].values)
        # print blh_mat

    def test_xyz2azel(self):
        ref = np.array([[6378137., 0., 0.]])
        pos = np.array([[6378137., 1., 0.]])
        az, el = gnss_geodesy.arr_xyz2az_el(pos, ref)
        self.assertAlmostEqual(az, gnss_geodesy.GEO_PI/2)
        self.assertAlmostEqual(el, 0)

        ref = np.array([[0, 6378137.0, 0]])
        pos = np.array([[0, 6378138.0, 0]])
        az2, el2 = gnss_geodesy.xyz2az_el(pos, ref)
        self.assertAlmostEqual(el2[0], gnss_geodesy.GEO_PI/2)

        pos = np.array([[1., 6378138.0, 0.]])
        az, el = gnss_geodesy.xyz2az_el(pos, ref)
        az2, el2 = gnss_geodesy.arr_xyz2az_el(pos, ref)
        self.assertAlmostEqual(az, az2)
        self.assertAlmostEqual(el, el2)
        self.assertAlmostEqual(gnss_geodesy.radian2degree(az[0]), 270.)
        self.assertAlmostEqual(gnss_geodesy.radian2degree(el[0]), 45.)

        pos = np.array([[1, 6378138.0, -1]])
        az, el = gnss_geodesy.xyz2az_el(pos, ref)
        az2, el2 = gnss_geodesy.arr_xyz2az_el(pos, ref)
        self.assertAlmostEqual(az[0], az2[0])
        self.assertAlmostEqual(el[0], el2[0])
        self.assertAlmostEqual(gnss_geodesy.radian2degree(az[0]), 225.)
        self.assertAlmostEqual(el[0], np.arctan(1/np.sqrt(2)))

    def test_arr_xyz2neu(self):
        orbit_file = path.join(path.dirname(__file__), "data",
                           "nium1350.pos.orbit")
        # xr_orbit = gnss_io.read_orbit_file(orbit_file)
        ref_xyz = np.array([[0, 6378137.0, 0]])
        pos_xyz = np.array([[0, 6378138.0, 0]])
        # sites = np.repeat(site, len(xr_orbit.loc[:, "G05"].values), axis=0)
        # n, e, u = gnss_geodesy.arr_xyz2neu(xr_orbit.loc[:, "G05"].values, sites)
        n, e, u = gnss_geodesy.arr_xyz2neu(pos_xyz, ref_xyz)
        self.assertAlmostEqual(n[0], 0)
        self.assertAlmostEqual(e[0], 0)
        self.assertAlmostEqual(u[0], 1)


        ref_xyz = np.array([[6378137., 0., 0.]])
        pos_xyz = np.array([[6378137., 1., 0.]])
        n, e, u = gnss_geodesy.arr_xyz2neu(pos_xyz, ref_xyz)
        self.assertAlmostEqual(n[0], 0)
        self.assertAlmostEqual(e[0], 1)
        self.assertAlmostEqual(u[0], 0)

