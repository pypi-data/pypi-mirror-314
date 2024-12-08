# -*- coding: utf-8 -*-
"""
gnss_geodesy
=====================

   Geodesy module of ppgnss.

"""
import string
import math
import numpy as np
import xarray as xr
from ppgnss import gnss_io

ELLIPSOIDS = {
    "wgs84": {
        "a": 6378137.,
        "f": 1 / 298.257223563,
    },
    "cgcs2000": {
        "a": 6378137.,
        "f": 1 / 298.257222101,
    },
    "grs80": {
        "a": 6378137.,
        "f": 1 / 298.257222100882711243,
    },
}

GEO_RE = 6371137.  # 地球平均半径


GEO_PI = 3.14159265358979323846

# see P88 of IS-GPS-200D
GPS_LIGHT_SPEED = 2.99792458E8
GPS_UN_GRAV = 3.986005E14
GPS_F_RELAT = -4.442807633E-10


def degree2radian(deg):
    """
    Convert degree to radians.

    :param deg: decimal degree.
    :type deg: float
    :return: radians
    :rtype: float

    Example usage::

    >> degree2radian(45.)
    >>
    """
    return deg * GEO_PI / 180.


def radian2degree(rad):
    """
    Convert radians to degree.

    :param rad: radians
    :type rad: float
    :return: degree
    :rtype: float

    Example usage::

    >> radian2degree(3.14)
    >>
    """
    return rad * 180. / GEO_PI

def dd2dms(dd):
    """
    Convert decimal degree to degree-minute-second.
    :param dd: 
    :return: 
    """
    deg = np.floor(dd)
    mi = np.floor(dd*60 - deg*60)
    sec = dd*3600 - deg*3600 - mi*60
    return deg, mi, sec


def fdms2dms(f_dms):
    """
    Convert degree-minute-second float like to degree minute second float.

    :param dms: degree-minute-second format float like ``dd.mmsssssss``
    :type dms: float
    :return: decimal degree minute second format like ``(dd, mm, ss.sssss)``
    :rtype: (int, int, float)

    Example usage::

    >>> dms2dd(30.1742577079)
    >>> (30, 17, 42.577079)
    >>> dms2dd(-110.13233343)
    >>> (-110, 13, 23.3343)
    """
    try:
        strdms = '%+018.13f' % f_dms
    except TypeError:
        raise TypeError("float parameter is expected")

    strd = strdms[:4]
    strm = strdms[5:7]
    strs = strdms[7:9] + '.' + strdms[9:]
    try:
        degree = int(strd)
        minute = int(strm)
        second = float(strs)
    except Exception:
        raise TypeError("invalide parameters")
    # dec_degree = abs(degree) + minute / 60. + second / 3600.
    # if degree < 0:
    #     dec_degree *= -1
    return degree, minute, second


def fdms2dd(f_dms):
    """
    Convert degree-minute-second to degree minute second.

    :param dms: degree-minute-second format float like ``dd.mmsssssss``
    :type dms: float
    :return: decimal degree minute second format like ``(dd, mm, ss.sssss)``
    :rtype: float

    Example usage::

    >>> dms2dd(30.1742577079)
    >>> 30.295160299722223
    >>> dms2dd(-110.13233343)
    >>> 110.22314841666667
    """

    degree, minute, second = fdms2dms(f_dms)
    dec_degree = abs(degree) + minute / 60. + second / 3600.
    if degree < 0:
        dec_degree *= -1

    return dec_degree


def xyz2geoblh(xMat, yMat, zMat):
    """Convert Cartesian Coordinate system to geographical coordinate system.
    :param xMat: x coordinates
    :type xMat: numpy.array or xarray.DataArray
    :param yMat: y coordinates
    :type yMat: numpy.array or xarray.DataArray
    """
    lon_ell = np.arctan2(yMat, xMat)
    # print(yMat, xMat, lon_ell)
    lat_ell = np.arctan2(zMat, np.sqrt(np.power(xMat, 2) + np.power(yMat, 2)))
    return radian2degree(lat_ell), radian2degree(lon_ell)


def arr_xyz2blh(xMat, yMat, zMat, ell='wgs84'):
    """Convert Cartesian Coordinate system to geographical coordinate system.
    :param xMat: x coordinates
    :type xMat: numpy.array or xarray.DataArray
    :param yMat: y coordinates
    :type yMat: numpy.array or xarray.DataArray
    """
    a_ell = ELLIPSOIDS[ell]['a']
    f_ell = ELLIPSOIDS[ell]['f']
    e2_ell = f_ell * (2 - f_ell)

    lon_ell = np.arctan2(yMat, xMat)
    p_ell = np.sqrt(xMat**2 + yMat**2)
    r_ell = np.sqrt(p_ell**2 + zMat**2)
    u_ell = np.arctan2(zMat * ((1 - f_ell) +
                               e2_ell * a_ell / r_ell), p_ell)
    lat_ell = np.arctan2(
        zMat * (1 - f_ell) + e2_ell * a_ell * np.sin(u_ell) ** 3,
        (1 - f_ell) * (p_ell - e2_ell * a_ell * np.cos(u_ell)**3))

    height = p_ell * np.cos(lat_ell) + zMat * np.sin(lat_ell) - \
        a_ell * np.sqrt(1 - e2_ell * np.sin(lat_ell)**2)
    # lat_deg = radian2degree(lat_ell)  # / Deg2Rad
    # lon_deg = radian2degree(lon_ell)  # / Deg2Rad
    lat_deg = lat_ell * 180. / GEO_PI
    lon_deg = lon_ell * 180. / GEO_PI
    # blh = np.array([lat_deg, lon_deg, height], dtype=np.float64).transpose()
    return lat_deg, lon_deg, height


def xyz2blh(xcoordinate, ycoordinate, zcoordinate, ell='wgs84'):
    """
    Convert Cartesian Coordinate system to geographical coordinate system.

    :param xcoordinate: x coordinate
    :type xcoordinate: float.
    :param ycoordinate: y coordinate
    :type ycoordinate: float.
    :param zcoordinate: z coordinate
    :type zcoordinate: float
    :param ell: ellipsoid name. Candidates are 'wgs84', 'cgcs2000'. see `ELLIPSOIDS`.
    :returns: (latitude, longitude, height). Latitude and longitude are in decimal degree.
    :rtype: (float, float, float)

    Example usage::

    >> xyz2blh(6378137., 0, 0, 'wgs84')
    >> (0.0, 0.0, 0.0)
    """

    a_ell = ELLIPSOIDS[ell]['a']
    f_ell = ELLIPSOIDS[ell]['f']
    e2_ell = f_ell * (2 - f_ell)
    # l = np.atan2(y,x)
    lon_ell = np.arctan2(ycoordinate, xcoordinate)
    p_ell = np.sqrt(xcoordinate**2 + ycoordinate**2)
    r_ell = np.sqrt(p_ell**2 + zcoordinate**2)
    u_ell = np.arctan2(zcoordinate * ((1 - f_ell) +
                                      e2_ell * a_ell / r_ell), p_ell)
    lat_ell = np.arctan2(zcoordinate * (1 - f_ell) + e2_ell * a_ell * np.sin(u_ell)
                         ** 3, (1 - f_ell) * (p_ell - e2_ell * a_ell * np.cos(u_ell)**3))

    height = p_ell * np.cos(lat_ell) + zcoordinate * np.sin(lat_ell) - \
        a_ell * np.sqrt(1 - e2_ell * np.sin(lat_ell)**2)
    lat_deg = radian2degree(lat_ell)  # / Deg2Rad
    lon_deg = radian2degree(lon_ell)  # / Deg2Rad
    return lat_deg, lon_deg, height


def blh2xyz(b_deg, l_deg, height, ellipsoid='cgcs2000'):
    """
    Convert geographical coordinate system to cartesian coordinate syste.

    :param b_deg: latitude in decimal degree.
    :type b_deg: float
    :param l_deg: longitude in decimal degree.
    :type l_deg: float
    :param height: height in meter.
    :type height: float
    :param ellipsoid: ellipsoid name like 'wgs84', 'cgcs2000'.
    :type ellipsoid: float
    :return: (x coordinate, y coordinate, z coordinate)
    :rtype: (float, float, float)
    """

    a_ell = ELLIPSOIDS[ellipsoid]['a']
    f_ell = ELLIPSOIDS[ellipsoid]['f']
    b_rad = degree2radian(b_deg)
    l_rad = degree2radian(l_deg)
    e2_ell = f_ell * (2 - f_ell)
    n_radius = a_ell / np.sqrt(1 - e2_ell * np.sin(b_rad) ** 2)
    xcoordinate = (n_radius + height) * np.cos(b_rad) * np.cos(l_rad)
    ycoordinate = (n_radius + height) * np.cos(b_rad) * np.sin(l_rad)

    zcoordinate = (n_radius * (1 - e2_ell) + height) * np.sin(b_rad)
    return xcoordinate, ycoordinate, zcoordinate


def get_solar_coord(mjd, sol_tab=None):
    """Calculate the coordinate of Solar.
    If ``sol_tab`` is not None, read soltab file and do interplotion.
    If ``sol_tab`` is None, derive from function.

    :param mjd: Modified Julian Date
    :type mjd: float
    :param sol_tab: filename of soltab.
    :type sol_tab: string
    :return: solar coordinate in ECI
    :rtype: (float, float, float)
    """
    if sol_tab:
        xr_sol = gnss_io.read_soltab_file(sol_tab)
        if mjd in xr_sol.coords['time'].values:
            return xr_sol.loc[mjd, :].values


def xr_xyz2neu(xr_pos, xr_ref):
    arr_xyz = np.array([xr_pos.loc[:, 'x'].values,
                        xr_pos.loc[:, 'y'].values,
                        xr_pos.loc[:, 'z'].values], dtype=np.float64).transpose()
    if len(xr_ref) == 3:
        ref_xyz = np.reshape(xr_ref, (-1, 3))
    else:
        ref_xyz = np.array(
            [xr_ref.loc[:, 'x'].values,
             xr_ref.loc[:, 'y'].values,
             xr_ref.loc[:, 'z'].values], dtype=np.float64).transpose()

    dN, dE, dU = arr_xyz2neu(arr_xyz, ref_xyz)

    ndata = np.stack(
        (dN, dE, dU), axis=0).transpose()

    coords = {'time': xr_pos.coords['time'].values,
              'data': ['n', 'e', 'u']}
    xr_neu = xr.DataArray(ndata, coords=coords, dims=['time', 'data'])
    return xr_neu

def xyz2az_el(xyz, ref_xyz):
    n, e, u = arr_xyz2neu(xyz, ref_xyz)
    az = np.arctan(np.abs(e / n))
    el = np.arctan(u / np.sqrt(n ** 2 + e ** 2))
    if n > 0 and e > 0:  # 1象限
        # print("1")
        pass
    elif n > 0 and e <= 0:  # 4象限
        # print("4")
        az = 2*GEO_PI - az
    elif n <= 0 and e > 0:  # 3
        # print("3")
        az = GEO_PI - az
    elif n <= 0 and e <= 0:
        # print("2")
        az = GEO_PI + az
    return az, el

def arr_xyz2az_el(arr_xyz, ref_xyz):
    """calculate azimuth and elevation.

    :param arr_xyz:
    :param ref_xyz:
    :return: az, el, radius
    """
    n, e, u = arr_xyz2neu(arr_xyz, ref_xyz)
    az = np.arctan(np.abs(e/n))
    el = np.arctan(u/np.sqrt(n**2+e**2))
    # print(az, el, n, e, u)
    k0 = n > 0
    k1 = n <= 0
    k2 = e > 0
    k3 = e <= 0

    k4 = np.logical_xor(k0, k2)  # n 和 e 符号相反

    # print(k0, k1, k2, k3, k4)
    # print(k1, np.power(-1, k4))
    az = k1*GEO_PI + np.power(-1, k4) * az

    az[az < 0] += 2*GEO_PI
    return az, el

    if n > 0 and e > 0:  # 1象限
        # print("1")
        pass
    elif n > 0 and e <= 0:  # 4象限
        # print("4")
        az = 2*GEO_PI - az
    elif n <= 0 and e > 0:  # 3
        # print("3")
        az = GEO_PI - az
    elif n <= 0 and e <= 0:
        # print("2")
        az = GEO_PI + az
    return az, el


def arr_xyz2neu(arr_xyz, ref_xyz):
    """Calcualte positioning error.
    """
    xr_diff = arr_xyz - ref_xyz
    x_array = ref_xyz[:, 0]
    y_array = ref_xyz[:, 1]
    z_array = ref_xyz[:, 2]
    xr_lat, xr_lon, xr_hgt = arr_xyz2blh(x_array,
                                         y_array,
                                         z_array)
    # import matplotlib.pyplot as plt
    # plt.plot(xr_lon, xr_lat)
    # plt.show()

    rad_lat = xr_lat * GEO_PI / 180.
    rad_lon = xr_lon * GEO_PI / 180.
    T11 = -np.sin(rad_lat) * np.cos(rad_lon)
    T12 = -np.sin(rad_lat) * np.sin(rad_lon)
    T13 = np.cos(rad_lat)

    T21 = -np.sin(rad_lon)
    T22 = np.cos(rad_lon)
    T23 = 0

    T31 = np.cos(rad_lat) * np.cos(rad_lon)
    T32 = np.cos(rad_lat) * np.sin(rad_lon)
    T33 = np.sin(rad_lat)

    dx = xr_diff[:, 0]
    dy = xr_diff[:, 1]
    dz = xr_diff[:, 2]

    dN = T11 * dx + T12 * dy + T13 * dz
    dE = T21 * dx + T22 * dy + T23 * dz
    dU = T31 * dx + T32 * dy + T33 * dz

    return dN, dE, dU


def dxyz2neu(dxyz, xyz, ellipsoid='wgs84'):
    """Convert dxyz to neu.
    xyz为站心的空间直角坐标
    """

    # 先计算站心大地坐标
    b, l, h = xyz2blh(xyz[0], xyz[1], xyz[2])  # degree
    B = degree2radian(b)
    L = degree2radian(l)

    # 计算旋转矩阵
    T11 = -math.sin(B) * math.cos(L)
    T12 = -math.sin(B) * math.sin(L)
    T13 = math.cos(B)

    T21 = -math.sin(L)
    T22 = math.cos(L)
    T23 = 0

    T31 = math.cos(B) * math.cos(L)
    T32 = math.cos(B) * math.sin(L)
    T33 = math.sin(B)

    dx = dxyz[0]
    dy = dxyz[1]
    dz = dxyz[2]

    # 计算北东高三个方向坐标值
    dN = T11 * dx + T12 * dy + T13 * dz
    dE = T21 * dx + T22 * dy + T23 * dz
    dU = T31 * dx + T32 * dy + T33 * dz

    return dN, dE, dU


def xr_xyz2rac(xr_xyz, xr_vel, xr_dxyz):
    """Convert dxyz from ECEF coordinate to radius-along-cross directions.

    :param xr_xyz: satellites' coordinates
    :type xr_xyz: xarray.DataArray
    :param xr_vel: satellites' velocities
    :type xr_vel: xarray.DataArray
    :param xr_dxyz: vector in ECEF from satellite to the point.
    :type xr_dxyz: xarray.DataArray

    Inputs data struct::

      >>> print xr_xyz.dims
      ('time', 'prn', 'data')
      >>> print xr_vel.coords['data']
      <xarray.DataArray 'data' (data: 3)>
      array(['x', 'y', 'z'],
            dtype='|S5')
      Coordinates:
        * data     (data) |S5 'x' 'y' 'z'

    """
    xr_rac = xr_dxyz.copy(deep=True)
    xr_rac.coords['data'] = ('data', ['radius', 'along', 'corss', 'clock'])
    for timestamp in xr_dxyz.coords['time']:
        if timestamp.values not in xr_xyz.coords['time'].values \
           or timestamp.values not in xr_vel.coords['time'].values:
            continue
        for prn in xr_dxyz.coords['prn']:
            if prn not in xr_xyz.loc[timestamp, :].coords['prn'].values:
                continue
            xyz = xr_xyz.loc[timestamp.values, prn].values[:3] * 1E-6
            vel = xr_vel.loc[timestamp.values, prn].values[:3] * 1E-5
            dxyz = xr_dxyz.loc[timestamp.values, prn].values[:3]
            vel_adjusted = adjust_vel(xyz, vel)
            vec_rac = xyz2rac(xyz, vel_adjusted, dxyz)
            vec_rac.append(xr_xyz.loc[timestamp.values, prn, 'clock'].values)
            xr_rac.loc[timestamp.values, prn] = vec_rac
    return xr_rac


def xyz2rac(xyz, vel, dxyz):
    """Convert vector ``dxyz`` from ECEF coordinate system  to satellite
    coordinate system. In the satellite coordinate system, ``radius`` is
    the direction from Earth Center to Satellite, and ``along-track`` is
    the same direction with ``vel``. ``cross-track`` is right-hand
    system with ``radius`` and ``vel``. This function can be used when
    converting satellite coordinate errors to r-a-c directions.
    Which ``xyz`` is coordniate of satellite, ``vel`` is velocity and
    ``dxyz`` is vector from


    :param xyz: coordinate of satellite
    :type xyz: list, [float, float, float]
    :param vel: velocity of satellite
    :type vel: list, [float, float, float]
    :param dxyz: vector in ECEF coordinate system from satellite
    :type dxyz: list, [float, float, float]

    Example usage::

        >> xyz = [0, 0, 1]
        >> vel = [1, 0, 0]
        >> dxyz = [1, 1, 1]
        >> gnss_geodesy.xyz2rac(xyz, vel, dxyz):

    """
    if not (len(xyz) == len(dxyz) == len(vel) == 3):
        raise ValueError("Error: length are not 3: "
                         + str(xyz) + str(dxyz) + str(vel))

    dot_prod = sum([x * v for x, v in zip(xyz, vel)])
    sin_theta = dot_prod / (np.linalg.norm(xyz) * np.linalg.norm(vel))
    if abs(sin_theta) > 1E-10:
        raise ValueError(("Error: velocity vector is not vertical"
                          "with position vector: ") + str(sin_theta))

    length_xyz = np.linalg.norm(xyz)
    dot_xyz_dxyz = sum([x0 * x1 for x0, x1 in zip(xyz, dxyz)])
    radius = dot_xyz_dxyz / length_xyz

    length_vel = np.linalg.norm(vel)
    dot_vel_dxyz = sum([x0 * x1 for x0, x1 in zip(vel, dxyz)])
    along = dot_vel_dxyz / length_vel

    vec_cross = [xyz[1] * vel[2] - xyz[2] * vel[1],
                 xyz[2] * vel[0] - xyz[0] * vel[2],
                 xyz[0] * vel[1] - xyz[1] * vel[0]]

    length_cross = np.linalg.norm(vec_cross)
    dot_cross_dxyz = sum([x0 * x1 for x0, x1 in zip(vec_cross, dxyz)])
    cross = dot_cross_dxyz / length_cross
    return [radius, along, cross]


def adjust_vel(xyz, vel):
    """Adjust velocity to the xyz's vertical plane. Firstly, the new vector
    should satisfy the conditions.

    ..:math:`\arrow{n} = k_1\arrow{x} + \arrow{v}`
    ..:math:`\arrow{n}\dot \arrow{x} = 0`

    which :math:`\arrow{n}` is the new vector and :math:`\arrow{x}` is the
    vector from Earth Center to Satellite. :math:`\arrow{v}` is the velocity
    vector. It can be solved that :math:`\arrow{n} = k_1\arrow{x} + \arrow{v}`
    :math:`k_1 = -\frac{xv_x + yv_y + zv_z}{x^2 + y^2 + z^2}`

    """

    if not len(xyz) == len(vel) == 3:
        raise ValueError("Error: length are not 3: "
                         + str(xyz) + str(vel))
    up = sum([x * v for x, v in zip(xyz, vel)])
    down = sum([x**2 for x in xyz])
    k_factor = - up / down

    new_vec = [k_factor * x + v for x, v in zip(xyz, vel)]
    return new_vec


def xr_adjust_vel(xr_xyz, xr_vel):
    """Similar with :func:`adjust_vel`. But the inputs are xArray.DataArray.
    """

    axises = ['x', 'y', 'z']
    if not axises == list(xr_xyz.coords['data'].values) \
       == list(xr_vel.coords['data'].values):
        raise ValueError("Error: xr_xyz and xr_vel's 'data' coord is"
                         " not equal to ['x', 'y', 'z']")

    xr_xyz = xr_xyz.copy(deep=True)
    xr_vel = xr_vel.copy(deep=True)
    up = np.sum(xr_xyz * xr_vel, axis=2)
    down = np.sum(xr_xyz * xr_xyz, axis=2)
    k_factor = -up / down
    xr_new_vel = k_factor * xr_xyz + xr_vel
    return xr_new_vel


def xr_xyz2rac2(xr_xyz, xr_vel, xr_dxyz):
    """Convert vector ``dxyz`` from ECEF coordinate system  to satellite
    coordinate system. In the satellite coordinate system, ``radius`` is
    the direction from Earth Center to Satellite, and ``along-track`` is
    the same direction with ``vel``. ``cross-track`` is right-hand
    system with ``radius`` and ``vel``. This function can be used when
    converting satellite coordinate errors to r-a-c directions.
    Which ``xyz`` is coordniate of satellite, ``vel`` is velocity and
    ``dxyz`` is vector from satellite.
    This function is faster than :func:`gnss_geodesy.xyz2rac`.


    :param xyz: coordinate of satellite
    :type xyz: xarray.DataArray
    :param vel: velocity of satellite
    :type vel: xarray.DataArray
    :param dxyz: vector in ECEF coordinate system from satellite
    :type dxyz: xarray.DataArray

    Example usage::

      >>> xr_vel = gnss_utils.loadobject("test", "data", "xyz2rac2.vel"))
      >>> xr_xyz = gnss_utils.loadobject("test", "data", "xyz2rac2.xyz"))
      >>> xr_dxyz = gnss_utils.loadobject("test", "data", "xyz2rac2.dxyz"))
      >>> xr_rac = gnss_geodesy.xyz2rac2(xr_xyz, xr_vel, xr_dxyz)
      >>> print np.linalg.norm(xr_dxyz[0, 0])
      0.0216101842585
      >>> print np.linalg.norm(xr_rac[0, 0])
      0.0216101842585

    """
    axises = ['x', 'y', 'z']
    if not axises == list(xr_xyz.coords['data'].values) \
       == list(xr_vel.coords['data'].values) \
       == list(xr_dxyz.coords['data'].values):
        raise ValueError("Error: xr_xyz and xr_vel's 'data' coord is"
                         " not equal to ['x', 'y', 'z']")

    coords = ['time', 'prn', 'data']
    if not all([list(xr_vel.coords[coord].values)
                == list(xr_xyz.coords[coord].values)
                == list(xr_dxyz.coords[coord].values)
                for coord in coords]):
        raise ValueError("Inputs parameters don't have same coords"
                         + str(xr_vel) + str(xr_xyz) + str(xr_dxyz))

    dot_prod = np.sum(xr_xyz * xr_vel, axis=2)

    # angles of vector xr_xyz and vector xr_vel
    xr_sin_theta = dot_prod / (np.linalg.norm(xr_xyz, axis=2)
                               * np.linalg.norm(xr_vel, axis=2))
    not_theta_almost_zero = (abs(xr_sin_theta) > 1e-10).any()
    if not_theta_almost_zero:
        raise ValueError(("Error: velocity vector is not vertical"
                          "with position vector: ") + str(xr_sin_theta))

    length_xyz = np.linalg.norm(xr_xyz, axis=2)
    invalid_idx = np.any(np.isnan(xr_dxyz), axis=2)

    dot_xyz_dxyz = np.sum(xr_xyz * xr_dxyz, axis=2)
    radius = dot_xyz_dxyz / length_xyz

    radius.values[invalid_idx] = np.nan

    length_vel = np.linalg.norm(xr_vel, axis=2)
    dot_vel_dxyz = np.sum(xr_vel * xr_dxyz, axis=2)
    along = dot_vel_dxyz / length_vel

    along.values[invalid_idx] = np.nan

    vec_cross = xr_vel.copy(deep=True)
    xyz_x = xr_xyz.loc[:, :, 'x']
    xyz_y = xr_xyz.loc[:, :, 'y']
    xyz_z = xr_xyz.loc[:, :, 'z']

    vel_x = xr_vel.loc[:, :, 'x']
    vel_y = xr_vel.loc[:, :, 'y']
    vel_z = xr_vel.loc[:, :, 'z']

    x_data = xyz_y * vel_z - xyz_z * vel_y
    y_data = xyz_z * vel_x - xyz_x * vel_z
    z_data = xyz_x * vel_y - xyz_y * vel_x
    vec_cross.loc[:, :, 'x'] = x_data
    vec_cross.loc[:, :, 'y'] = y_data
    vec_cross.loc[:, :, 'z'] = z_data
    # vec_cross = [xyz[1] * vel[2] - xyz[2] * vel[1],
    #              xyz[2] * vel[0] - xyz[0] * vel[2],
    #              xyz[0] * vel[1] - xyz[1] * vel[0]]

    length_cross = np.linalg.norm(vec_cross, axis=2)
    # dot_cross_dxyz = sum([x0 * x1 for x0, x1 in zip(vec_cross, dxyz)])
    dot_cross_dxyz = np.sum(vec_cross * xr_dxyz, axis=2)
    cross = dot_cross_dxyz / length_cross

    cross.values[invalid_idx] = np.nan

    xr_rac = xr_vel.copy(deep=True)
    xr_rac['data'] = ('data', ['radius', 'along', 'cross'])
    xr_rac.loc[:, :, "radius"] = radius
    xr_rac.loc[:, :, "along"] = along
    xr_rac.loc[:, :, "cross"] = cross
    return xr_rac


def xr_brdc2ecef(xr_brdc, interval=1):
    """Calculating Satellites' coordinates from Broadcast Ephermeris.

    :param xr_brdc: brdc data from :func:`gnss_io.read_brdc_file`.
    :type xr_brdc: xarray.DataArray
    :param interval: interval of output
    :type interval: int
    :return: coordinates of satellites
    :rtype: xarray.DataArray
    """
    prns = xr_brdc.coords['prn'].values
    prns_brdc_list = []
    for prn in prns:
        xr_prn_brdc = xr_brdc.loc[:, prn, :]
        xr_prn_brdc_valid = xr_prn_brdc[np.logical_not(
            np.all(np.isnan(xr_prn_brdc), axis=1))]

        pass


def ellip2ortho(ellip_height, geoid):
    """
    Convert ellipsoidal height to orthometric height

    ellipsoidal height= orthometric height  + geoid

    :param height:
    :param geoid:
    :return:
    """

    return ellip_height - geoid


def ortho2ellip(ortho_height, geoid):
    """
    Convert orthometric height to ellipsoidal height.

    ellipsoidal height= orthometric height  + geoid

    :param ortho_height:
    :param geoid:
    :return:
    """
    return ortho_height + geoid