import sys
import math
from os import path
from io import BytesIO
import operator
from collections import defaultdict
import datetime

try:
    from builtins import chr
except ImportError:
    from __builtin__ import chr
    # from builtins import chr
# import collections
# import datetime
try:
    import cython_extend
except ImportError:
    pass
import numpy as np
import xarray as xr
import pandas as pd

from ppgnss import gnss_time
from ppgnss import gnss_geodesy

# R = 8.3144 # J/(mok*K) 普适气体常数
# #Rd = 0.287 # J/(g*K)
# g0 = 9.80 # m^2/(s^2*gpm) 或 J/kg
# Rw = 461.5 #J/(kg*K) 水汽的比气体常数
#
# def waterpress2rho(e, T):
#     """
#     水气压转绝对湿度。
#
#     :return: g/m^3
#     """
#     return e/(Rw*T)
#
# def temp2vtemp(T, e, p):
#     """
#     温度转虚温。
#
#     :param T: temperature, K
#     :param e: water vapor press, Pa
#     :param p: total press (dry + wet), Pa
#     :return:
#     """
#     return (1+0.378*e/p)*T
#
# def press2gpm(Tv, p1, p2):
#     return R*Tv*np.log(p1/p2)*g0
#
# def press2altitude(Tv, p1, p2):
#     """
#
#     :return: delta altitude.
#     """
#     return 18400*(1+Tv/273)*np.log(p1/p2)

def saaszwd(tempK, e):
    """
    return saas zwd.

    :param temp:
    :param e:
    :return:
    """
    zwd = 0.002277 * (1255.0 / tempK + 0.05) * e
    return zwd

def saasthyd(p, dlat, hell):
    # This subroutine determines the zenith hydrostatic delay based on the
    # equation by Saastamoinen (1972) as refined by Davis et al. (1985)
    #
    # c Reference:
    # Saastamoinen, J., Atmospheric correction for the troposphere and
    # stratosphere in radio ranging of satellites. The use of artificial
    # satellites for geodesy, Geophys. Monogr. Ser. 15, Amer. Geophys. Union,
    # pp. 274-251, 1972.
    # Davis, J.L, T.A. Herring, I.I. Shapiro, A.E.E. Rogers, and G. Elgered,
    # Geodesy by Radio Interferometry: Effects of Atmospheric Modeling Errors
    # on Estimates of Baseline Length, Radio Science, Vol. 20, No. 6,
    # pp. 1593-1607, 1985.
    #
    # input parameters:
    #
    # p:     pressure in hPa
    # dlat:  ellipsoidal latitude in radians
    # dlon:  longitude in radians
    # hell:  ellipsoidal height in m
    #
    # output parameters:
    #
    # zhd:  zenith hydrostatic delay in meter
    #
    # Example 1 :
    #
    # p = 1000;
    # dlat = 48d0*pi/180.d0
    # hell = 200.d0
    #
    # output:
    # zhd = 2.2695 m
    #
    # Johannes Boehm, 8 May 2013
    # ---
    #
    # calculate denominator f

    f = 1 - 0.00266 * np.cos(2 * dlat) - 0.00000028 * hell

    # calculate the zenith hydrostatic delay
    zhd = 0.0022768 * p / f
    return zhd


def read_GPT2w(filename=None):
    """
    Read GPT2w Grid file, return xr.

    :param filename:
    :return:
    """
    if not filename:
        filename = path.join(path.dirname(__file__), "..", "data", "gpt2_1wA.grd")
    else:
        pass
    data = np.loadtxt(filename,
                      dtype={"names": ("lat", "lon",
                                       "p_a0", "p_A1", "p_B1", "p_A2", "p_B2",
                                       "T_a0", "T_A1", "T_B1", "T_A2", "T_B2",
                                       "Q_a0", "Q_A1", "Q_B1", "Q_A2", "Q_B2",
                                       "dT_a0", "dT_A1", "dT_B1", "dT_A2", "dT_B2",
                                       "undu", "Hs",
                                       "ah_a0", "ah_A1", "ah_B1", "ah_A2", "ah_B2",
                                       "aw_a0", "aw_A1", "aw_B1", "aw_A2", "aw_B2",
                                       "lam_a0", "lam_A1", "lam_B1", "lam_A2", "lam_B2",
                                       "Tm_a0", "Tm_A1", "Tm_B1", "Tm_A2", "Tm_B2"),
                             "formats": ("f", "f",
                                         "i", "i", "i", "i", "i",
                                         "f", "f", "f", "f", "f",
                                         "f", "f", "f", "f", "f",
                                         "f", "f", "f", "f", "f",
                                         "f", "f",
                                         "f", "f", "f", "f", "f",
                                         "f", "f", "f", "f", "f",
                                         "f", "f", "f", "f", "f",
                                         "f", "f", "f", "f", "f",
                                         )},
                      comments="%")
    coord_var = ["p_a0", "p_A1", "p_B1", "p_A2", "p_B2",
                 "T_a0", "T_A1", "T_B1", "T_A2", "T_B2",
                 "Q_a0", "Q_A1", "Q_B1", "Q_A2", "Q_B2",
                 "dT_a0", "dT_A1", "dT_B1", "dT_A2", "dT_B2",
                 "undu", "Hs",
                 "ah_a0", "ah_A1", "ah_B1", "ah_A2", "ah_B2",
                 "aw_a0", "aw_A1", "aw_B1", "aw_A2", "aw_B2",
                 "lam_a0", "lam_A1", "lam_B1", "lam_A2", "lam_B2",
                 "Tm_a0", "Tm_A1", "Tm_B1", "Tm_A2", "Tm_B2"]

    data["lon"] = [v + 360 * (v < 0) for v in data["lon"]]
    lat_min, lat_max = np.min(data["lat"]), np.max(data["lat"])
    lon_min, lon_max = np.min(data["lon"]), np.max(data["lon"])
    coord_lat = np.arange(lat_max, lat_min - .5, -1)
    coord_lon = np.arange(lon_min, lon_max + .5, 1)
    rows = len(coord_lat)

    grds = list()
    for var_name in coord_var:
        grd = np.reshape(data[var_name], (rows, -1))
        grds.append(grd)

    xr_gpt2w = xr.DataArray(grds, coords=[coord_var, coord_lat, coord_lon],
                            dims=["var", "lat", "lon"])

    return xr_gpt2w


def _get_sincos(v_list, dmjd):
    """
    covert GPT2w a0, a1, b1, a2, b2, to Value

    :param v_list:
    :param dmjd:
    :return:
    """
    dmjd1 = dmjd - 51544.5
    cosfy = np.cos(dmjd1 / 365.25 * 2 * np.pi)
    coshy = np.cos(dmjd1 / 365.25 * 4 * np.pi)
    sinfy = np.sin(dmjd1 / 365.25 * 2 * np.pi)
    sinhy = np.sin(dmjd1 / 365.25 * 4 * np.pi)
    v = v_list[0] + v_list[1] * cosfy + v_list[2] * sinfy + v_list[3] * coshy + v_list[4] * sinhy
    return v


def get_grid_metro_dmjd(xr_gpt2w, lat, lon, hell, dmjd):
    """
    return grid value of air pressure, temperature and water vapor pressure.

    :param xr_gpt2w:
    :param lat: should on the grid point.
    :param lon: should on the grid point.
    :param hell: the ell height of required point.
    :param dmjd: dmjd.
    :return:
    """
    gm = 9.80665
    dMtr = 28.965E-3
    Rg = 8.3143

    undu = xr_gpt2w.loc["undu", lat, lon].values
    Hs = xr_gpt2w.loc["Hs", lat, lon].values
    hgt = hell - undu
    redh = hgt - Hs

    T0 = get_grid_var_dmjd(xr_gpt2w, lat, lon, dmjd, "T")
    dT = get_grid_var_dmjd(xr_gpt2w, lat, lon, dmjd, "dT")/1000.
    T = T0 + dT*redh - 273.15  # temperature

    p0 = get_grid_var_dmjd(xr_gpt2w, lat, lon, dmjd, "p")
    Q = get_grid_var_dmjd(xr_gpt2w, lat, lon, dmjd, "Q")/1000.
    Tv = T0 * (1+0.6077*Q)
    cc = gm*dMtr/(Rg*Tv)
    p = (p0*np.exp(-cc*redh))/100.  # air pressure

    lam = get_grid_var_dmjd(xr_gpt2w, lat, lon, dmjd, "lam")

    e0 = Q*p0/(0.622+0.374*Q)/100.
    e = e0*(100.*p/p0)**(lam+1)  # water vapor pressure

    return T, dT, p, e


def get_grid_var_dmjd(xr_gpt2w, lat, lon, dmjd, var_name):
    """
    Get grid var in time dmjd.

    :param xr_gpt2w:
    :param lat:
    :param lon:
    :param hell:
    :param dmjd:
    :param var_name:
    :return:
    """

    var_a0 = xr_gpt2w.loc[var_name+"_a0", lat, lon].values
    var_a1 = xr_gpt2w.loc[var_name+"_A1", lat, lon].values
    var_b1 = xr_gpt2w.loc[var_name+"_B1", lat, lon].values
    var_a2 = xr_gpt2w.loc[var_name+"_A2", lat, lon].values
    var_b2 = xr_gpt2w.loc[var_name+"_B2", lat, lon].values
    var = _get_sincos([var_a0, var_a1, var_b1, var_a2, var_b2], dmjd)
    return var


def nearest_grid(lat, lon, min_lat=None, min_lon=None, lat_cellsize=None, lon_cellsize=None):
    """

    :param lat:
    :param lon:
    :param min_lat:
    :param min_lon:
    :param lat_cellsize:
    :param lon_cellsize:
    :return:
    """
    if not min_lon:
        min_lon = 0.5
    if not min_lat:
        min_lat = 89.5
    if not lat_cellsize:
        lat_cellsize = 1
    if not lon_cellsize:
        lon_cellsize = 1
    lat_nearest = np.int((lat-min_lat)/lat_cellsize)*lat_cellsize + min_lat
    lon_nearest = np.int((lon-min_lon)/lon_cellsize)*lon_cellsize + min_lon
    return lat_nearest, lon_nearest


def get_box(lat, lon, min_lat=None, min_lon=None, lat_cellsize=None, lon_cellsize=None):
    """
    return box points for lat, lon
    :param lat:
    :param lon:
    :return:
    """
    if not min_lon:
        min_lon = 0.5
    if not min_lat:
        min_lat = 89.5
    if not lat_cellsize:
        lat_cellsize = 1
    if not lon_cellsize:
        lon_cellsize = 1

    lat_low = np.int(np.floor((lat - min_lat)/lat_cellsize))*lat_cellsize + min_lat
    lat_upper = lat_low + lat_cellsize

    lon_left = np.int(np.floor((lon - min_lon)/lon_cellsize))*lon_cellsize+min_lon
    lon_right = lon_left+lon_cellsize
    return lat_low, lat_upper, lon_left, lon_right


def gpt2w(xr_gpt2w, lat, lon, hell, dmjd, interpolation="bilinear"):
    """
    return gpt2w model.
    :param xr_gpt2w:
    :param lat:
    :param lon:
    :param hell:
    :param dmjd:
    :return:
    """
    if interpolation == "nearest":
        pass
    elif interpolation == "bilinear":
        pass


def get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hell, dmjd, var_name):

    """
    :param xr_gpt2w:
    :param lat:
    :param lon:
    :param hell:
    :param var_name:
    :return:
    """
    if var_name in []:
        raise TypeError("Error: var name error")
    if lon < 0:
        lon = lon + 360.

    lat_low, lat_up, lon_left, lon_right = get_box(lat, lon)

    T_left_low, dT_left_low, p_left_low, e_left_low = get_grid_metro_dmjd(xr_gpt2w, lat_low, lon_left, hell, dmjd)
    T_left_up, dT_left_up, p_left_up, e_left_up = get_grid_metro_dmjd(xr_gpt2w, lat_up, lon_left, hell, dmjd)
    T_right_low, dT_right_low, p_right_low, e_right_low = get_grid_metro_dmjd(xr_gpt2w, lat_low, lon_right, hell, dmjd)
    T_right_up, dT_right_up, p_right_up, e_right_up = get_grid_metro_dmjd(xr_gpt2w, lat_up, lon_right, hell, dmjd)

    if var_name == "T":
        var_left_low = T_left_low
        var_left_up = T_left_up
        var_right_low = T_right_low
        var_right_up = T_right_up
    elif var_name == "dT":
        var_left_low = dT_left_low
        var_left_up = dT_left_up
        var_right_low = dT_right_low
        var_right_up = dT_right_up
    elif var_name == "p":
        var_left_low = p_left_low
        var_left_up = p_left_up
        var_right_low = p_right_low
        var_right_up = p_right_up
    elif var_name == "e":
        var_left_low = e_left_low
        var_left_up = e_left_up
        var_right_low = e_right_low
        var_right_up = e_right_up
    elif var_name == "undu" or var_name == "Hs":
        var_left_low = xr_gpt2w.loc[var_name, lat_low, lon_left].values
        var_left_up = xr_gpt2w.loc[var_name, lat_up, lon_left].values
        var_right_low = xr_gpt2w.loc[var_name, lat_low, lon_right].values
        var_right_up = xr_gpt2w.loc[var_name, lat_up, lon_right].values

    else:
        # var_left_low = xr_gpt2w.loc[var_name, lat_low, lon_left].values
        var_left_low = get_grid_var_dmjd(xr_gpt2w, lat_low, lon_left, dmjd, var_name)
        # var_left_up = xr_gpt2w.loc[var_name, lat_up, lon_left].values
        var_left_up = get_grid_var_dmjd(xr_gpt2w, lat_up, lon_left, dmjd, var_name)
        # var_right_low = xr_gpt2w.loc[var_name, lat_low, lon_right].values
        var_right_low = get_grid_var_dmjd(xr_gpt2w, lat_low, lon_right, dmjd, var_name)
        # var_right_up = xr_gpt2w.loc[var_name, lat_up, lon_right].values
        var_right_up = get_grid_var_dmjd(xr_gpt2w, lat_up, lon_right, dmjd, var_name)

    #            1- beta   beta
    #         | +---------------+
    #   alpha + |               |
    #         | |  ★           |
    #         | |               |
    # 1-alpha + |               |
    #         | +---------------+

    # print(var_name, var_left_up, var_left_low, var_right_up, var_right_low)
    alpha = (lat - lat_low) / (lat_up - lat_low)
    beta = (lon - lon_left) / (lon_right - lon_left)

    var_left = alpha * var_left_up + (1 - alpha) * var_left_low
    var_right = alpha * var_right_up + (1 - alpha) * var_right_low
    var = (1 - beta) * var_left + beta * var_right
    if var_name == "ah" or var_name == "aw":
        var = var/1000.
    return var


def asknewet(e, Tm, lbd):
    # This subroutine determines the zenith wet delay based on the
    # equation 22 by Aske and Nordius (1987)
    #
    # c Reference:
    # Askne and Nordius, Estimation of tropospheric delay for microwaves from
    # surface weather data, Radio Science, Vol 22(3): 379-386, 1987.
    #
    # input parameters:
    #
    # e:      water vapor pressure in hPa
    # Tm:     mean temperature in Kelvin
    # lambda: water vapor lapse rate (see definition in Askne and Nordius 1987)
    #
    # output parameters:
    #
    # zwd:  zenith wet delay in meter
    #
    # Example 1 :
    #
    # e =  10.9621 hPa
    # Tm = 273.8720
    # lambda = 2.8071
    #
    # output:
    # zwd = 0.1176 m
    #
    # Johannes Boehm, 3 August 2013
    # Johannes Boehm, 24 December 2014, converted to Fortran
    # ---

    #  implicit double precision (a-h,o-z)

    #  double precision k1,k2,k2p,k3,lambda

    #  !% coefficients
    k1 = 77.604e0  # K/hPa
    k2 = 64.79e0  # K/hPa
    k2p = k2 - k1 * 18.0152e0 / 28.9644e0  # K/hPa
    k3 = 377600.e0  # % KK/hPa

    #  !% mean gravity in m/s**2
    gm = 9.80665e0
    #  !% molar mass of dry air in kg/mol
    dMtr = 28.965 * 1e-3

    wM = 18.0152e0

    #  !% universal gas constant in J/K/mol
    R = 8.3143e0

    #  !% specific gas constant for dry consituents
    Rd = R / dMtr

    zwd = 1.e-6 * (k2p + k3 / Tm) * Rd / (lbd + 1.e0) / gm * e

    return zwd


def _get_wdd_gpt2w_fast(dmjd, lat, lon, hell):
    """
    返回乌东德气温、气压、水汽压(GPT2w模型)

    :param dmjd:
    :param lat:
    :param lon:
    :param hgt:
    :return:
    """
    gm = 9.80665  # mean gravity in m/s**2
    dMtr = 28.965E-3  # molar mass of dry air in kg/mol
    Rg = 8.3143  # universal gas constant in J/K/mol

    p_list = [78551, 182, -189, -98, -76]
    T_list = [287.1, -5.5, -0.3, -1.2, 0.3]
    Q_list = [8.46, -3.59, -2.35, 0.48, 0.22] # need div 1000
    dT_list = [-6.6, 0.5, -0.3, 0.4, 0.0] # need div 1000
    undu = -33.83
    Hs = 2148.86
    ah_list = [1.2756, -0.0133, -0.0050, 0.0000, 0.0003] # need div 1000
    aw_list = [0.5035, -0.0624, -0.0149, -0.0068, -0.0001] # need div 1000
    lam_list = [2.9695, 0.9129, -0.0071, 0.3424, 0.0097]
    Tm_list = [276.3, -2.9, -1.0, -0.2, 0.2]

    tem0 = _get_sincos(T_list, dmjd)
    dt = _get_sincos(dT_list, dmjd) / 1000.
    Q = _get_sincos(Q_list, dmjd) / 1000.
    lam = _get_sincos(lam_list, dmjd)
    p0 = _get_sincos(p_list, dmjd)
    tm = _get_sincos(Tm_list, dmjd)

    hgt = hell - undu # transforming ellipsoidal height to orthometric height
    redh = hgt - Hs
    tem = tem0 + dt * redh - 273.15  # temperture
    # print(tem, tem0, dt, redh, hgt)
    Tv = tem0 * (1 + 0.6077 * Q)  # virtual temperature in Kelvin
    cc = gm*dMtr/(Rg*Tv)
    P = p0 * np.exp(-cc*redh) / 100
    e0 = 0.01 * Q * p0 / (0.622 + 0.378 * Q)
    e = e0 * (100 * P / p0) ** (lam + 1)
    return tem, P, e, lam, tm, Hs



def get_gpt2w_ztd_fast(dmjd, lat, lon, hgt, xr_gpt2w):
    tem, p, e, lbd, Tm, Hs = _get_wdd_gpt2w_fast(dmjd, lat, lon, hgt)
    # Hs = gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, 0, dmjd, "Hs")
    # T = gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "T")
    # e = gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "e")
    # p = gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "p")
    # Tm = gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "Tm")
    # lbd = gnss_trop.get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "lam")
    zhd = saasthyd(p, np.deg2rad(lat), Hs)
    zwd = asknewet(e, Tm, lbd)
    # print("Hs:", Hs, "T:", tem, "e:", e, "p:", p, "Tm:", Tm, "lam:", lbd)
    return zhd, zwd, Tm, lbd


def get_gpt2w_ztd(lat, lon, hgt, dmjd, xr_gpt2w):
    Hs = get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, 0, dmjd, "Hs")
    T = get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "T")
    e = get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "e")
    p = get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "p")
    Tm = get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "Tm")
    lbd = get_gpt2w_interpolation_var(xr_gpt2w, lat, lon, hgt, dmjd, "lam")
    zhd = saasthyd(p, np.deg2rad(lat), hgt)
    zwd = asknewet(e, Tm, lbd)
    # print(lat, lon, hgt, p, e)
    print("gpt2w: hgt=%.1f, e=%.3f, p=%.3f, temp=%.2f" % (hgt,  e, p, T))
    return zhd, zwd, Tm, lbd


def get_std_atmosphere_bernese(hgt):
    """
    return standard atmosphere.

    :param hgt:
    :return: temp(degC), press(mbar), e(mbar)
    """

    temp0 = 18.
    humi0 = 0.5
    pr = 1013.25 # mbar
    pres = pr * ((1.0 - 2.226E-5 * hgt) ** 5.225)
    temp = temp0 - 6.5E-3 * hgt
    tempK = temp + 273.16
    humi = humi0*np.exp(-0.0006396*(hgt))
    # es = mc.saturation_vapor_pressure(temp*units.degC)
    es = 6.112*np.exp(17.62*temp/(243.12+temp)) # saturation vapor pressure
    # e = (es*humi).to(units.mbar).m
    e = es*humi
    e1 = 6.108*humi0*np.exp((17.15*tempK-4684.0)/(tempK-38.45))
    return temp, pres, e


def get_std_ztd(lat, hgt):
    temp_std, pres_std, e_std = get_std_atmosphere_bernese(hgt)
    tempK = temp_std + 273.16
    zhd = saasthyd(pres_std, np.deg2rad(lat), hgt)
    zwd = 0.002277 * (1255.0 / tempK + 0.05) * e_std
    return zhd, zwd
