"""
    gnss_utils
    =====================

    Utils module contains some useful utils module.

    1. Everett Interpolation
    2. SSR to Clock

"""

import pickle
from collections import defaultdict

import numpy as np
import xarray as xr
import pandas as pd

from ppgnss import gnss_time
from ppgnss import gnss_geodesy

# Everett Interpolation, see slade1971.
EVCF = [1.7873015873015873E0, -0.4960317460317460E0, 0.1206349206349206E0,
        -0.1984126984126984E-1, 0.1587301587301587E-2, -0.9359567901234568E0,
        0.6057098765432098E0, -0.1632716049382716E0, 0.2779982363315696E-01,
        -0.2259700176366843E-02, 0.1582175925925926E0, -0.1171296296296296E0,
        0.4606481481481481E-1, -0.8796296296296296E-2, 0.7523148148148148E-3,
        -0.9755291005291005E-2, 0.7605820105820106E-2, -0.3505291005291005E-2,
        0.8597883597883598E-3, -0.8267195767195767E-4, 0.1929012345679012E-3,
        -0.1543209876543210E-3, 0.7716049382716048E-4, -0.2204585537918871E-4,
        0.2755731922398589E-5]

EVCF_MAT = np.array([EVCF[i * 5:(i + 1) * 5][::-1]
                     + EVCF[i * 5 + 1: (i + 1) * 5]
                     for i in range(0, 5)])


def get_xr_rms(xr_neu, str_start_time=None, str_stop_time=None):
    """
    :param xr_neu:
    :param str_start_time:
    :param str_stop_time:
    :return: rms of n, e ,u
    """
    if str_start_time is None:
        str_start_time = str(xr_neu.coords["time"].values[0])
    if str_stop_time is None:
        str_stop_time = str(xr_neu.coords["time"].values[-1])
    xr_neu_new = xr_neu.loc[str_start_time:str_stop_time, :]
    rms_neu = np.sqrt(np.nanmean(xr_neu_new * xr_neu_new, axis=0))
    return rms_neu[0], rms_neu[1], rms_neu[2], np.sqrt(rms_neu[0] ** 2 + rms_neu[1] ** 2)


def everett_interp_order8(ti_list, fi_list, t4interp):
    """
    Everett Interpolation using 8th difference. ``ti_list`` and ``fi_list``
    are time series with same interval. ``ti_list`` should be in time order.
    ``t`` is the time for interplotion. ``t`` should be greater then the
    first value of ``ti_list`` and less then the last value ``ti_list``.

    :param ti_list: time list in time order, Modified Julian Date
    :type ti_list: float list
    :param fi_list: function value list
    :type fi_list: float list
    :return: float
    :rtype: float
    """
    if len(ti_list) != 9:
        raise ValueError("list length is not 9: " + str(ti_list))
    dti_list = [t0 - t1 for t0, t1 in zip(ti_list[:-1], ti_list[1:])]
    if not all([dt0 == dt1 for dt0, dt1 in zip(dti_list[:-1], dti_list[1:])]):
        raise ValueError("Time intervals are not in order")

    if t4interp < ti_list[0] or t4interp > ti_list[-1]:
        raise ValueError("time for interplotion is not in time range.")
    boundary = filter(lambda t0, t1: t0 < t4interp < t1,
                      zip(ti_list[:-1], ti_list[1:]))
    if not boundary:
        raise ValueError("time for interplotion is not in time range.")
    t_front, t_behind = boundary[0]
    h_step = ti_list[1] - ti_list[0]
    p_factor = (t4interp - t_front) / h_step
    q_factor = 1 - p_factor
    print(q_factor)
    y_vec = np.dot(EVCF_MAT, fi_list)
    print(y_vec)


def saveobject(obj0, filename):
    """Save python object to file.

    :param obj0: object in python
    :type obj0: object
    :param filename: Output filename for saving file.
    :type filename: string
    """
    with open(filename, 'wb') as fwrite:
        pickle.dump(obj0, fwrite)
        return True
    return False


def loadobject(binfilename):
    """Load object from file. File should be saved by
    :func:`gnss_utils.saveobject`.

    :param binfilename: filename for loading
    :type binfilename: string

    """
    with open(binfilename, 'rb') as fread:
        obj = pickle.load(fread)
        return obj
    return None


def xr_ssr2clock_norm(xr_clock_ssr, xr_brdc):
    """
    Convert correction and brdc to satellite clock. If different interval and
    latency is required, use `gnss_utils.xr_ssr2clock2`.
    """
    coord_prns = [prn for prn in xr_clock_ssr.coords['prn'].values
                  if prn.startswith("G") and len(prn) == 3]
    coord_time = xr_clock_ssr.coords['time'].values
    ndata = np.zeros((len(coord_time), len(coord_prns)),
                     dtype=np.float64) + np.nan

    xr_clock = xr.DataArray(ndata,
                            coords=[coord_time, coord_prns],
                            dims=['time', 'prn'])
    for prn in coord_prns:
        if prn not in xr_brdc.coords['prn'].values:
            continue
        xr_brdc_prn = xr_brdc.loc[:, prn]
        xr_ssr_prn = xr_clock_ssr.loc[:, prn]

        idx_valid_brdc = np.logical_not(
            np.isnan(xr_brdc_prn.loc[:, "IODE"].values))
        xr_valid_brdc_prn = xr_brdc_prn[idx_valid_brdc]

        for iode, clock_bias, clock_drift, toe, gpsw in \
                xr_valid_brdc_prn.loc[:, ["IODE",
                                          "SVclockBias",
                                          "SVclockDrift",
                                          "TimeEph",
                                          "GPSWeek",
                                          ]]:
            idx_iode_equal = xr_ssr_prn.loc[:, "IODE"] == iode
            # print idx_iode_equal
            xr_c0_prn_iode = xr_ssr_prn[idx_iode_equal.values].loc[:, "C0"]
            xr_a0_prn_iode = clock_bias
            xr_a1_prn_iode = clock_drift

            obj_reference_time = gnss_time.toe2datetime(
                gpsw.values, toe.values)
            dt64_reference_time = np.datetime64(obj_reference_time)

            delta_time = xr_c0_prn_iode.coords['time'] - \
                         dt64_reference_time
            delta_seconds = delta_time / np.timedelta64(1, 's')
            # relativ_corr = 0.
            xr_clock_prn = xr_a0_prn_iode \
                           + xr_c0_prn_iode / gnss_geodesy.GPS_LIGHT_SPEED \
                           + xr_a1_prn_iode.values * delta_seconds.values
            xr_clock.loc[idx_iode_equal, prn] = xr_clock_prn.values
    return xr_clock


def time_arr_gen(time_from, time_to, interval):
    """ Generate equal-interval time array.

    :time_from: startting time, like "2017-10-10 10:10:10.000"
    :type time_start: string
    :time_to: End time. like "2017-10-11 10:10:10.000"
    :type time_to: string
    :interval: interval (second)
    :type interval: int

    Usage example::

      >>> time_from='2017-10-10 00:00:00.00'
      >>> time_to = '2017-10-10 00:00:20.00'
      >>> interval = 5
      >>> time_arr_gen(time_from, time_to, 5)
      DatetimeIndex(['2017-10-10 00:00:00', '2017-10-10 00:00:05',
                     '2017-10-10 00:00:10', '2017-10-10 00:00:15',
                     '2017-10-10 00:00:20'],
                    dtype='datetime64[ns]', freq='5S')
.
      ----------------------------------------------------------------------
      Ran 1 test in 0.001s


    """
    str_freq = '%02dS' % interval
    # pd_time_list = pd.date_range(time_from, time_to,
    #                              freq=str_freq).to_datetime()
    pd_time_list = pd.to_datetime(pd.date_range(time_from, time_to,
                                                freq=str_freq))
    return pd_time_list


def xr_ssr2clock(xr_clock_ssr, xr_brdc, latency=0, interval=None,
                 valid_seconds=None):
    """
    Convert correction and brdc to satellite clock.

    :xr_clock_ssr: SSR. Obtain from `gnss_io.read_ssr_file`
    :xr_brdc: brdc. Obtain from `gnss_io.read_brdc_file`
    :latency: latency of RTS
    :type latency: int
    :interval: interval of out clock, seconds
    :type interval: int
    :valid_seconds: how many seconds are valid when using SSR
    :type valid_seconds: int
    :repair: Whether repair datum jumps or not
    :type repair: bool
    :return: clock
    :rtype: xr_clock
    """
    coord_prns = [prn for prn in xr_clock_ssr.coords['prn'].values
                  if prn.startswith("G") and len(prn) == 3]

    time_from_obj64 = xr_clock_ssr.coords['time'].values[0]
    time_to_obj64 = xr_clock_ssr.coords['time'].values[-1]
    update_rate = (xr_clock_ssr.coords['time'].values[1]
                   - xr_clock_ssr.coords['time'].values[0]) \
                  / np.timedelta64(1, 's')
    if not interval:
        interval = update_rate
    if not valid_seconds:
        valid_seconds = update_rate - 1
    str_freq = '%02dS' % interval

    coord_time = pd.to_datetime(pd.date_range(
        time_from_obj64,
        time_to_obj64 + np.timedelta64(int(latency + valid_seconds), 's'),
        freq=str_freq))
    # coord_time = pd.date_range(
    #     time_from_obj64,
    #     time_to_obj64 + np.timedelta64(int(latency + valid_seconds), 's'),
    #     freq=str_freq).to_datetime()
    ndata = np.zeros((len(coord_time), len(coord_prns)),
                     dtype=np.float64) + np.nan

    xr_clock = xr.DataArray(ndata,
                            coords=[coord_time, coord_prns],
                            dims=['time', 'prn'])

    for prn in coord_prns:
        if prn not in xr_brdc.coords['prn'].values:
            continue
        xr_brdc_prn = xr_brdc.loc[:, prn]
        xr_ssr_prn = xr_clock_ssr.loc[:, prn]

        idx_valid_brdc = np.logical_not(
            np.isnan(xr_brdc_prn.loc[:, "IODE"].values))
        xr_valid_brdc_prn = xr_brdc_prn[idx_valid_brdc]

        for iode, clock_bias, clock_drift, toe, gpsw in \
                xr_valid_brdc_prn.loc[:, ["IODE",
                                          "SVclockBias",
                                          "SVclockDrift",
                                          "TimeEph",
                                          "GPSWeek",
                                          ]]:

            idx_iode_equal = xr_ssr_prn.loc[:, "IODE"] == iode
            if not idx_iode_equal.values.any():
                continue
            rts_reftime_from = xr_ssr_prn[
                idx_iode_equal.values].coords['time'].values[0]
            rts_reftime_to = xr_ssr_prn[
                idx_iode_equal.values].coords['time'].values[-1]

            # coord_time_extra = pd.date_range(
            #     rts_reftime_from + np.timedelta64(latency, 's'),
            #     rts_reftime_to +
            #     np.timedelta64(int(latency + valid_seconds), 's'),
            #     freq=str_freq).to_datetime()
            coord_time_extra = pd.to_datetime(pd.date_range(
                rts_reftime_from + np.timedelta64(latency, 's'),
                rts_reftime_to +
                np.timedelta64(int(latency + valid_seconds), 's'),
                freq=str_freq))

            xr_c0_prn_iode = xr_ssr_prn[idx_iode_equal.values].sel(
                time=coord_time_extra,
                method='ffill').loc[:, "C0"]
            xr_c1_prn_iode = xr_ssr_prn[idx_iode_equal.values].sel(
                time=coord_time_extra,
                method='ffill').loc[:, "C1"]

            xr_a0_prn_iode = clock_bias
            xr_a1_prn_iode = clock_drift

            brdc_ref_time_dt64 = np.datetime64(
                gnss_time.toe2datetime(gpsw.values, toe.values))

            extra_seconds = np.array([
                (curr_time - brdc_ref_time_dt64) / np.timedelta64(1, 's')
                for curr_time in coord_time_extra])

            latency_seconds = \
                np.array([(t1 - t2) / np.timedelta64(1, 's')
                          for t1, t2 in
                          zip(coord_time_extra,
                              xr_c0_prn_iode.coords['time'].values)])

            idx_invalid = latency_seconds > valid_seconds

            xr_clock_prn = xr_a0_prn_iode.values \
                           + xr_c0_prn_iode.values / gnss_geodesy.GPS_LIGHT_SPEED \
                           + xr_a1_prn_iode.values * extra_seconds

            if idx_invalid.any():
                xr_clock_prn[idx_invalid] = np.nan
            xr_clock.loc[coord_time_extra, prn] = xr_clock_prn
    # repairing here
    return xr_clock


def _remove_drift(xr_clock, xr_brdc):
    """Removing Clock drift from clock first order difference.
    """
    xr_clock_firstorder = xr_clock.diff('time', label="upper")
    coord_prns = [prn for prn in xr_clock.coords['prn'].values
                  if prn.startswith("G") and len(prn) == 3]
    coord_times = xr_clock.coords['time']
    intervals = (coord_times.diff(
        'time', label="lower") / np.timedelta64(1, 's')).values

    clock_drift = np.nanmean(
        xr_brdc.loc[:, coord_prns, "SVclockDrift"].values, axis=0)
    nepochs, nsat = xr_clock_firstorder.shape

    intervals.shape = (-1, 1)
    clock_drift.shape = (1, -1)
    xr_clock_removed_drift = xr_clock_firstorder \
                             - intervals * clock_drift
    return xr_clock_removed_drift


def clock_extrapolation(xr_clock, xr_brdc, interval=None, valid_seconds=None):
    """Extrapolating Satellite Clock using Clock drift from BRDC.
    """
    coord_prns = [prn for prn in xr_clock.coords['prn'].values
                  if prn.startswith("G") and len(prn) == 3]

    update_rate = (xr_clock.coords['time'].values[1]
                   - xr_clock.coords['time'].values[0]) \
                  / np.timedelta64(1, 's')
    if not interval:
        interval = update_rate
    if not valid_seconds:
        valid_seconds = update_rate - 1

    str_freq = '%02dS' % interval
    clock_reftime_from = xr_clock.coords['time'].values[0]
    clock_reftime_to = xr_clock.coords['time'].values[-1]

    coord_time_extra = pd.date_range(
        clock_reftime_from,
        clock_reftime_to + np.timedelta64(int(valid_seconds), 's'),
        freq=str_freq).to_datetime()

    ndata = np.zeros((len(coord_time_extra), len(coord_prns)),
                     dtype=np.float64) + np.nan
    xr_clock_extra = xr.DataArray(ndata,
                                  coords=[coord_time_extra, coord_prns],
                                  dims=['time', 'prn'])
    for prn in coord_prns:
        idx_clock_nan = np.logical_not(np.isnan(xr_clock.loc[:, prn]))
        if not idx_clock_nan.any():
            continue
        xr_clock_prn = xr_clock.loc[:, prn]

        xr_clock_prn_droped = xr_clock_prn[idx_clock_nan]

        clock_reftime_prn_from = xr_clock_prn_droped.coords['time'].values[0]
        clock_reftime_prn_to = xr_clock_prn_droped.coords['time'].values[-1] \
                               + np.timedelta64(int(valid_seconds), 's')
        coord_time_prn_extra = pd.date_range(
            clock_reftime_prn_from,
            clock_reftime_prn_to,
            freq=str_freq).to_datetime()

        xr_reftime_prn = xr_clock_prn_droped.coords['time'].sel(
            time=coord_time_prn_extra,
            method='ffill')

        xr_clock_prn_extra = xr_clock_prn_droped.sel(time=coord_time_prn_extra,
                                                     method='ffill')
        # print(xr_reftime_prn.loc["2017-06-21 01:02:10.00"])
        latency_seconds = np.array([(t1 - t2) / np.timedelta64(1, 's')
                                    for t1, t2 in
                                    zip(coord_time_prn_extra,
                                        xr_reftime_prn['time'].values)])
        clock_drift_prn = np.nanmean(
            xr_brdc.loc[:, prn, "SVclockDrift"].values,
            axis=0)

        tmp = clock_drift_prn * latency_seconds
        # print(tmp)
        # print(xr_clock_prn_extra.loc["2017-06-21 01:02:10.00"])
        xr_clock_extra.loc[
        str(clock_reftime_prn_from):str(clock_reftime_prn_to),
        prn] = xr_clock_prn_extra.values + tmp
    xr_diff = xr_clock_extra.diff('time')
    idx_outlier = np.abs(xr_diff) > 0.3 * 1e-9
    # plt.plot(xr_diff)
    # plt.show()
    # plt.close()
    ndata = xr_clock_extra[1:].values
    ndata[idx_outlier] = np.nan
    xr_clock_extra[1:] = ndata
    return xr_clock_extra


def cm2inch(cm):
    return cm / 2.54


def inch2cm(inch):
    return inch * 2.54


def repair_datum(xr_clock, xr_brdc):
    """Repair Datum jump of correction.
    """
    xr_clock_firstorder_zeromean = _remove_drift(xr_clock, xr_brdc)
    xr_clock_firstorder_mean = np.nanmean(xr_clock_firstorder_zeromean, axis=1)

    std_each_prn = np.nanstd(xr_clock_firstorder_zeromean, axis=0)
    std_each_epoch = np.nanstd(xr_clock_firstorder_zeromean, axis=1)
    throldhold = 0.05 * 1E-9  # std_each_prn * 3

    idx_outlier = np.abs(
        xr_clock_firstorder_zeromean) > throldhold  # std_each_prn

    idx_not_outlier = np.logical_not(idx_outlier)
    idx_not_datum_jump = np.all(
        np.abs(xr_clock_firstorder_zeromean) < throldhold, axis=1)
    idx_prob_datum_jump = np.any(
        np.abs(xr_clock_firstorder_zeromean) > throldhold, axis=1)

    xr_clock_firstorder_probjump = xr_clock_firstorder_zeromean * idx_outlier
    ndata = xr_clock_firstorder_probjump.values
    ndata[idx_not_outlier] = np.nan

    xr_clock_firstorder_probjump = ndata
    xr_clock_firstorder_probjump_mean = np.nanmean(
        xr_clock_firstorder_probjump, axis=1)
    xr_clock_firstorder_probjump_std = np.nanstd(
        xr_clock_firstorder_probjump, axis=1)

    xr_clock_firstorder_probjump_range = np.nanmax(
        xr_clock_firstorder_probjump, axis=1) \
                                         - np.nanmin(xr_clock_firstorder_probjump, axis=1)

    xr_clock_firstorder_probjump_nsat = np.sum(idx_outlier, axis=1)

    idx_sure_datum_jump = np.logical_and(
        np.logical_and(
            xr_clock_firstorder_probjump_range < 0.2 * 1E-9,
            xr_clock_firstorder_probjump_nsat >= 1,
        ),
        np.logical_and(
            np.abs(xr_clock_firstorder_mean) > .05 * 1e-9,
            idx_prob_datum_jump,
        )
    )

    idx_sure_outlier = np.logical_and(
        np.logical_and(
            xr_clock_firstorder_probjump_range > 0.5 * 1E-9,
            xr_clock_firstorder_probjump_nsat > 1,
        ),
        np.logical_and(
            np.abs(xr_clock_firstorder_mean) >= 0,
            idx_prob_datum_jump,
        )
    )
    xr_outlier = xr_clock_firstorder_zeromean[idx_sure_outlier]

    idx_nan = np.isnan(xr_clock_firstorder_probjump_mean)
    idx_not_nan_and_jumped = np.logical_and(np.logical_not(idx_nan),
                                            idx_sure_datum_jump)

    jumped_values = np.zeros(
        len(xr_clock_firstorder_probjump_mean), dtype=np.float64)
    jumped_values[idx_not_nan_and_jumped] = xr_clock_firstorder_probjump_mean[
        idx_not_nan_and_jumped]
    cum_jumped_values = np.cumsum(jumped_values)
    cum_jumped_values.shape = (-1, 1)

    xr_clock_repaired = xr_clock.copy(deep=True)
    ndata = xr_clock_repaired.values[1:]
    nsat = len(xr_clock.coords['prn'].values)
    ndata -= np.tile(cum_jumped_values, (1, nsat))
    xr_clock_repaired[1:].values = ndata

    xr_diff = xr_clock_repaired.diff('time')

    idx_outlier = np.abs(xr_diff) > 0.5 * 1E-9
    ndata = xr_clock_repaired[1:].values
    ndata[idx_outlier] = np.nan
    xr_clock_repaired[1:] = ndata

    # xr_clock_repaired[idx_outlier] = np.nan
    xr_jumped = xr.DataArray(cum_jumped_values[:, 0],
                             coords=[xr_clock.coords['time'].values[1:], ],
                             dims=['time', ])

    # return xr_clock_repaired, xr_jumped, idx_not_nan_and_jumped,
    # xr_outlier, xr_clock_firstorder_probjump_nsat
    return xr_clock_repaired, xr_jumped  # , xr_outlier


def points2grids(points, llpoint, shape, cellsize):
    """
    points: n*3
    points[0]: x
    points[1]: y
    points[2]: z
    llpoint: (llx, lly) 左下角像元四个角点的左下角坐标
    shape: (ncol, nrow) 列数(x方向）, 行数(y方向）
    cellsize: (xcellsize, ycellsize), x 和 y方向格网大小
    """
    ncol, nrow = shape[0], shape[1]
    xstep, ystep = cellsize[0], cellsize[1]
    xmin, ymin = llpoint[0], llpoint[1]

    xmax = xmin + ncol * xstep
    ymax = ymin + nrow * ystep
    grid_points = [[list() for j in range(ncol)] for i in range(nrow)]
    inds = list()
    for record in points:
        x, y, v = record[0], record[1], record[2]
        # print(x, y, v)
        if (x < xmin) or (x > xmax) or (y < ymin) or (y > ymax):
            continue
        ind_col = int(np.floor((x - xmin) / xstep)) # 列索引
        ind_row = int(np.floor((y - ymin) / ystep)) #
        # print(ind_row, ind_col, llpoint[0], llpoint[1], shape)
        # print(len(grid_points), len(grid_points[0]))
        grid_points[ind_row][ind_col].append(v)
        inds.append((ind_row, ind_col))

    data = defaultdict()
    for key in {"mean", "std", "max", "min", "count"}:
        data[key] = np.full((nrow, ncol), np.nan)
    for ind_row, ind_col in inds:
        data["mean"][ind_row, ind_col] = np.mean(grid_points[ind_row][ind_col])
        data["max"][ind_row, ind_col] = np.max(grid_points[ind_row][ind_col])
        data["min"][ind_row, ind_col] = np.min(grid_points[ind_row][ind_col])
        data["count"][ind_row, ind_col] = len(grid_points[ind_row][ind_col])
        data["std"][ind_row, ind_col] = np.std(grid_points[ind_row][ind_col])

    return data, inds