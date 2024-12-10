import numpy as np
import xarray as xr
from scipy import special

from ppgnss import gnss_geodesy



def calculate_xr_ipp(xr_orbit, site):
    """
    Calculate IPP.
    :param xr_orbit: satellite coordinates
    :param site: site coordinates
    :return:
    """
    site_coord = np.array([site["x"], site["y"], site["z"]]).reshape(-1, 3)
    sat_coords = xr_orbit.values.reshape(-1, 3)
    site_coords = np.repeat(site_coord, len(sat_coords), axis=0)
    lat_ipps, lon_ipps, factors = arr_calculate_ipp(sat_coords,
                                                     site_coords,
                                                     506700)
    nsat = len(xr_orbit.coords['prn'])
    lat_ipps = lat_ipps.reshape(-1, nsat)
    lon_ipps = lon_ipps.reshape(-1, nsat)
    factors = factors.reshape(-1, nsat)
    dims = ["time", "prn", "data"]
    coords = {'time': xr_orbit.coords["time"].values,
               'prn': xr_orbit.coords["prn"].values,
               'data': ["lat", "lon", "factor"]}
    data = np.zeros_like(xr_orbit.values)
    xr_ipp = xr.DataArray(data, coords=coords, dims=dims)
    xr_ipp.loc[:, :, "lat"] = lat_ipps
    xr_ipp.loc[:, :, "lon"] = lon_ipps
    xr_ipp.loc[:, :, "factor"] = factors
    return xr_ipp


def calculate_xr_intersect(xr_orbit, site, radius_earth=6371000, hgt=450000):
    radius = radius_earth + hgt
    site_coord = np.array([site["x"], site["y"], site["z"]]).reshape(-1, 3)
    sat_coords = xr_orbit.values.reshape(-1, 3)
    site_coords = np.repeat(site_coord, len(sat_coords), axis=0)

    az, el = gnss_geodesy.arr_xyz2az_el(sat_coords, site_coords)
    rp = gnss_geodesy.GEO_RE/(gnss_geodesy.GEO_RE+hgt)*np.cos(el)
    # rp2 = gnss_geodesy.GEO_RE/(gnss_geodesy.GEO_RE+hgt)*np.sin(alpha*(gnss_geodesy.GEO_PI/2 - el))
    ap = gnss_geodesy.GEO_PI/2 - np.arcsin(rp)

    x2, y2, z2 = sat_coords[:, 0], sat_coords[:, 1], sat_coords[:, 2]
    x1, y1, z1 = site_coords[:, 0], site_coords[:, 1], site_coords[:, 2]

    A = (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1)
    B = 2*(x1*(x2-x1) + y1*(y2-y1) + z1*(z2-z1))
    C = x1*x1 + y1*y1 + z1*z1 - radius*radius

    k = (-B + np.sqrt(np.power(B, 2) - 4*A*C))/(2*A)
    x = k*(x2-x1) + x1
    y = k*(y2-y1) + y1
    z = k*(z2-z1) + z1
    lat_ipps, lon_ipps = gnss_geodesy.xyz2geoblh(x, y, z)
    b_ipp, l_ipp, h_ipp = gnss_geodesy.xyz2blh(x, y, z)
    nsat = len(xr_orbit.coords['prn'])
    lat_ipps = lat_ipps.reshape(-1, nsat)
    lon_ipps = lon_ipps.reshape(-1, nsat)
    factor = np.sin(ap).reshape(-1, nsat)
    # el_ipps = el.reshape(-1, nsat)

    # factors = factors.reshape(-1, nsat)
    dims = ["time", "prn", "data"]
    coords = {'time': xr_orbit.coords["time"].values,
               'prn': xr_orbit.coords["prn"].values,
               'data': ["lat", "lon", "factor"]}
    data = np.zeros_like(xr_orbit.values)
    xr_ipp = xr.DataArray(data, coords=coords, dims=dims)
    xr_ipp.loc[:, :, "lat"] = lat_ipps
    xr_ipp.loc[:, :, "lon"] = lon_ipps
    xr_ipp.loc[:, :, "factor"] = factor
    return xr_ipp

def calculate_intersect(sat_coor, site_coor, radius=6821000):
    """
    sat: (x2, y2, z1)
    site: (x1, y1, z1)

    x^2+y^2+z^2 = 6821000^2, (1)

     x-x1       y-y1      z-z1
    -------  = ------- = ------- = k, (2)
     x2-x1      y2-y1     z2-z1
     (1) and (2) =>
     A = (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2, A>0
     B = 2[x1(x2-x1) + y1(y2-y1) + z1(z2-z1)],
     C = x1^2 + y1^2 + z1^2 - R^2
          -B + sqrt(B^2-4AC)
     k =  ---------------
              2A
     x = (x2-x1)k+x1
     y = (y2-y1)k+y1
     z = (z2-z1)k+z1
    :param sat_coor:
    :param site_coor:
    :param radius:
    :return:
    """
    # lat_sat, lon_sat = gnss_geodesy.xyz2geoblh(sat_coor["x"], sat_coor["y"], sat_coor["z"])
    # lat_site, lon_site = gnss_geodesy.xyz2geoblh(site_coor["x"], site_coor["y"], site_coor["z"])
    # b_sat, l_sat, h_sat = gnss_geodesy.xyz2blh(sat_coor["x"], sat_coor["y"], sat_coor["z"])
    # b_site, l_site, h_site = gnss_geodesy.xyz2blh(site_coor["x"], site_coor["y"], site_coor["z"])
    x2, y2, z2 = sat_coor["x"], sat_coor["y"], sat_coor["z"]
    # x2, y2, z2 = xr_sat
    x1, y1, z1 = site_coor["x"], site_coor["y"], site_coor["z"]
    A = (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
    B = 2*(x1*(x2-x1) + y1*(y2-y1) + z1*(z2-z1))
    C = x1**2 + y1**2 + z1**2 - radius**2
    k = (-B + np.sqrt(B**2 - 4*A*C))/(2*A)
    x = k*(x2-x1) + x1
    y = k*(y2-y1) + y1
    z = k*(z2-z1) + z1
    lat_ipp, lon_ipp = gnss_geodesy.xyz2geoblh(x, y, z)
    b_ipp, l_ipp, h_ipp = gnss_geodesy.xyz2blh(x, y, z)
    print(x, y, z)
    return lat_ipp, lon_ipp

def calculate_ipp(site, sat, hgt=506700, alpha=0.9782):
    """
    site['x'], site['y'], site['z'], sat['x'], sat['y'], sat['z']

    :param site: coordinates of site.
    :param sat: coordinate of satellite.
    :param hgt: ionospheric layer height.
    :return: IPP coordinate (lat, lon), and factor transfer VTEC to STEC
    """
    arr_sat = np.array([sat['x'], sat['y'], sat['z']]).reshape(-1, 3)
    arr_site = np.array([site['x'], site['y'], site['z']]).reshape(-1, 3)
    lat_ipps, lon_ipps, fac_v_to_s = arr_calculate_ipp(arr_sat, arr_site, hgt)
    return lat_ipps, lon_ipps, fac_v_to_s


def arr_calculate_ipp(arr_sat, arr_site, hgt=450000, alpha=0.9782):
    az, el = gnss_geodesy.arr_xyz2az_el(arr_sat, arr_site)

    rp = gnss_geodesy.GEO_RE/(gnss_geodesy.GEO_RE+hgt)*np.cos(el)
    rp2 = gnss_geodesy.GEO_RE/(gnss_geodesy.GEO_RE+hgt)*np.sin(alpha*(gnss_geodesy.GEO_PI/2 - el))
    ap = gnss_geodesy.GEO_PI/2 - el - np.arcsin(rp)

    lat, lon = gnss_geodesy.xyz2geoblh(arr_site[:, 0], arr_site[:, 1],
                                       arr_site[:, 2])
    lat_sat, lon_sat = gnss_geodesy.xyz2geoblh(arr_sat[:, 0], arr_sat[:, 1],
                                               arr_sat[:, 2])
    print("sat:", lat_sat, lon_sat)
    print("site", lat, lon)
    lat_rad = gnss_geodesy.degree2radian(lat)
    lon_rad = gnss_geodesy.degree2radian(lon)
    # print(lat_rad, lon_rad)
    # print(az, el)
    lat_ipp = np.arcsin(np.sin(lat_rad)*np.cos(ap) + np.cos(lat_rad)*np.sin(ap)*np.cos(az))
    tmp0 = np.arcsin(np.sin(ap)*np.sin(az)/np.cos(lat_ipp))
    lon_ipp = lon_rad + tmp0  # np.sin(ap)*np.sin(az)/np.cos(lat_ipp))

    tmp1 = np.tan(lat_ipp)*np.cos(az)
    idx = np.logical_or(np.logical_and(lat_rad > 0,
                                       tmp1 > np.tan(gnss_geodesy.GEO_PI/2-lat_rad)),
                        np.logical_and(lat_rad < 0,
                                       -tmp1 > np.tan(gnss_geodesy.GEO_PI/2+lat_rad)))
    lon_ipp[idx] = lon_rad[idx] + gnss_geodesy.GEO_PI - tmp0[idx]


    lat_ipp_deg = gnss_geodesy.radian2degree(lat_ipp)
    lon_ipp_deg = gnss_geodesy.radian2degree(lon_ipp)
    print("ipp:", lat_ipp_deg, lon_ipp_deg)
    re = gnss_geodesy.GEO_RE
    # print(1/np.cos(el))
    return lat_ipp, lon_ipp, 1/np.sqrt(1-np.power(rp2, 2))  # np.cos(np.arcsin(
        # np.sin(alpha*(gnss_geodesy.GEO_PI/2-el))*re/(hgt+re)))


def norm_legendre(n, m, theta):
    """
    return the normalize associated Legendre functions.
    which expressed by \bar{P_{n,m}} = N_{n,m}P_{n,m}. Normally n == m.
    :param n:
    :param m:
    :param theta:
    :return:
    """
    norm_nm = normalize_mat(n, m)
    p_nm, p_d_nm = special.lpmn(m, n, np.sin(theta))
    p_nm = p_nm.transpose()
    return p_nm, norm_nm, p_nm*norm_nm


def normalize_mat(n, m):
    """
    \bar{P_{n,m}} = N_{n,m}P_{n,m} are the normalized associated Legendre functions
    where N_{n,m} = \sqrt{\frac{(n-m)!(2n+1)(2-\delta_{0,m})}{(n+m)!}}, \delta_{0,m} == 1 if m == 0
    this function return the normalize factor N_{n,m}.

    :param n: degree
    :param m: order, where m <= n
    :return:
    """
    nMat = np.zeros((n+1, m+1), dtype=np.float64)
    for iN in range(0, n+1):
        for iM in range(0, iN+1):
            nMat[iN, iM] = normalize(iN, iM)
    return nMat


def normalize(iN, iM):
    delta = 0
    if iM == 0:
        delta = 1
    return np.sqrt(np.math.factorial(iN-iM)*(2*iN+1)*(2-delta)\
                   /np.math.factorial(iN+iM))


def get_cos_sin_mat(n, s):
    """
    :param n:
    :param s:
    :return:
    """
    vec_col = np.arange(0, n+1).reshape(1, -1)
    mat = np.tile(vec_col, (len(vec_col[0]), 1))
    return np.cos(mat*s), np.sin(mat*s)


def create_design_vec(n, beta, s):
    p_nm, n_nm, p_norm = norm_legendre(n, n, beta)
    # cosms, sinms = get_cos_sin_mat(n, s)
    n_para_cos = int((n+1)*(n+2)/2)
    n_para_sin = int(n*(n+1)/2)
    n_para = n_para_cos + n_para_sin
    design_vec = np.zeros(n_para)
    i_para = 0
    for iN in range(0, n+1):
        for iM in range(0, iN+1):
            design_vec[i_para] = p_norm[iN, iM]*np.cos(iM*s)

            if iM !=0:
                design_vec[(i_para-iN-1)+n_para_cos] = p_norm[iN, iM]*np.sin(iM*s)
            #sin part
            i_para += 1
    return design_vec


def create_desiga_mtrx(n, betas, ss):
    if len(betas) != len(ss):
        raise Exception("Error: length are not equal")
    n_obs = len(betas)
    n_para = (n+1)*(n+1)
    design_mtrx = np.zeros((n_obs, n_para))
    for irow, (beta, s) in enumerate(zip(betas, ss)):
        design_mtrx[irow] = create_design_vec(n, beta, s)

    return design_mtrx


def xr_coef2grid(xr_coef, nrows=35, ncols=36, xllcenter=-180,
                 yllcenter=-87.5, xcellsize=10, ycellsize=5):
    beta_deg = np.arange(yllcenter, yllcenter+nrows*ycellsize, ycellsize)
    ss_deg = np.arange(xllcenter, xllcenter+ncols*xcellsize, xcellsize)
    betas = gnss_geodesy.degree2radian(beta_deg)
    sss = gnss_geodesy.degree2radian(ss_deg)
    data = np.zeros((len(xr_coef.coords["time"].values), nrows, ncols))
    coord_time = list()
    coord_lat = beta_deg
    coord_lon = ss_deg
    ss_grid, beta_grid = np.meshgrid(sss, betas)
    betas_rshp = beta_grid.reshape(-1)
    sss_rshp = ss_grid.reshape(-1)
    n_degree = 15
    design_vec = create_desiga_mtrx(n_degree, betas_rshp, sss_rshp)
    n_para_a = (n_degree+1)*(n_degree+2)/2
    n_para_b = (n_degree+1)*(n_degree+2)/2
    for iepoch, epoch_time in enumerate(xr_coef.coords["time"].values):
        coord_time.append(epoch_time)
        aMat = xr_coef.loc[epoch_time, :, :, "a"]
        bMat = xr_coef.loc[epoch_time, :, :, "b"]
        a_list = list()
        b_list = list()
        for idegree in range(0, n_degree+1):
            for iorder in range(0, idegree+1):
                a_list.append(aMat[idegree, iorder])
                if iorder !=0:
                    b_list.append(bMat[idegree, iorder])
        ab_para = np.array(a_list+b_list)
        ab_para[np.isnan(ab_para)] = 0.
        values = np.dot(design_vec, ab_para)
        val_mat = values.reshape(len(betas), len(sss))
        data[iepoch, :, :] = val_mat
    xr_gim = xr.DataArray(data, coords=[coord_time, coord_lat,
                                        coord_lon],
                          dims=["time", "lat", "lon"])
    return xr_gim


