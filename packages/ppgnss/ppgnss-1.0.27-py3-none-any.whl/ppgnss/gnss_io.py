# -*- coding: utf-8 -*-
"""
   gnss_io
   ------------------

   I/O module of ppgnss. Including reading and writting rinex file,
   sp3 file, ssr file and others files.
"""
import sys
import math
from os import path
from io import BytesIO
import operator
from collections import defaultdict
import datetime
from enum import Enum

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


class ListTooShortError(Exception):
    """Raised when string length is too short for use.
    """


class RecordsNotInOrder(Exception):
    """Raised when records are not in time order in clock file.
    """
    pass


class DELTA_DAY(Enum):
    IS_PREDAY = -1
    IS_CURDAY = 0
    IS_NXTDAY = 1


def read_ssr_file(filename):
    """
    .. todo::

      Read ssr file and save to xarray.DataArray.

    :param ssr_filename: filename of SSR file.
    :type ssr_filename: string
    :return: dataset of SSR file
    :rtype: xarray.DataArray

    Example usage::

      # The usage should be like follow.
      >> ssr_filename = "tests/data/CLK912740.17C"
      >> clock_ssr, orbit_ssr = read_ssr(ssr_filename)
      >> print clock_ssr.loc['2017-09-30 23:59:50.000', 'G32', 'IODE']
      34
      >> print clock_ssr.loc['2017-09-30 23:59:50.000', 'G32', 'C0']
      0.5062
      >> print clock_ssr.dims
      ('time', 'prn', 'data')
      >> print clock_ssr.coords['data']
      <xarray.DataArray 'data' (data: 4)>
      array(['IODE', 'C0', 'C1', 'C2'],
          dtype='|S5')
      Coordinates:
      * data     (data) |S5 'IODE' 'C0' 'C1' 'C2'
    """

    if not path.isfile(filename):
        raise IOError("file not exists. %s" % filename)

    with open(filename, 'rb') as fread:
        clock_ssr, orbit_ssr = _parse_ssr_block(fread)
        return clock_ssr, orbit_ssr


def save_clock_file(filename, xr_clock, prns=None, fast=True):
    """Save xr_clock to CLK file.

    :param filename: filename of CLK file will save to.
    :type file: string
    :param xr_clock: clock for saving
    :type xr_clock: xarray.DataArray
    :return: None
    :rtype: None
    """
    header = [
        ("     3.00           C                                       " +
         "RINEX VERSION / TYPE \n"),
        ("                                                            " +
         "END OF HEADER        \n")]
    # print(header)
    # sys.exit(0)

    if prns:
        prns = [tmp for tmp in prns if tmp in xr_clock.coords['prn'].values]
        xr_select_clock = xr_clock.loc[:, prns]
    else:
        xr_select_clock = xr_clock

    if fast:
        lines = _xr_clock2listsCython(xr_select_clock)
    else:
        lines = _xr_clock2lines(xr_select_clock, prns)
    lines = header + lines

    with open(filename, 'w') as fwrite:
        fwrite.writelines(lines)


def _xr_clock2listsCython(xr_clock):
    """

    :param xr_clock: xArray type clock data. See :`gnss_io.read_clock_file()`.
    :return: 3 elements list.

    list[0]: date time of first epoch, [year, month, day, hour, minute, second]
    list[1]: time delta to the first epoch. unit: s
    list[2]: clock data. 2d-numpy.array, size is :`(len(epochs), len(prns))`
    """
    data = xr_clock.values
    coord_time = xr_clock.coords["time"].values
    prns = xr_clock.coords["prn"].values
    first_epoch = pd.to_datetime(coord_time[0])
    secs = (coord_time - coord_time[0]) / np.timedelta64(1, "s")
    lines = cython_extend.clock2strlist(data, list(secs), list(prns), first_epoch)
    return lines

def _xr_clock2lines(xr_clock, prns=None):
    """Convert xr_clock to lines for writting.
    """

    lines = [
        'AS %s  %s  2   %19.12e  %18.12e\n' % (
            sat_record.coords['prn'].values,
            pd.to_datetime(
                str(sat_record.coords['time'].values
                    )).strftime('%Y %m %d %H %M %S.000000'),
            float(sat_record.values),
            0)
        for epoch_record in xr_clock
        for sat_record in epoch_record
        if not np.isnan(sat_record.values)]
    return lines


def read_clock_file2(filename):
    read_clock_file(filename)


def read_clock_file(filename):
    """Reading CLK file.

    :param filename: filename of CLK file.
    :type filename: string
    :return: all clock in file
    :rtype: xarray.DataArray

    Example usage::

        >>> filename = 'tests/data/igs19544.clk_30s'
        >>> xr_data = read_clock_file(filename)
        >>> print xr_data.loc["2017-06-22 00:13:30.000000", 'G01']
        <xarray.DataArray ()>
        array(5.612718564585e-05)
        Coordinates:
            time     datetime64[ns] 2017-06-22T00:13:30
            prn      |S4 'G01'

    """

    if not path.isfile(filename):
        raise IOError("file not exists. %s" % filename)

    with open(filename, 'rb') as fread:
        line = fread.readline().decode()
        if line.startswith('AR ') or line.startswith('AS '):
            fread.seek(-len(line), 1)
            xr_data = parse_clock_block(fread)
        else:
            for line in fread:
                line = line.decode()
                if 'END OF HEADER' in line:
                    xr_data = parse_clock_block(fread)
                    break
        return xr_data


def parse_clock_block(block_stream):
    """Parse data from file stream.

    :param data_block: file object that opened.
    :type data_block: open file object
    :return: All stations' clocks and satellites' clock
    :rtype: xarray.DataArray

    Example usage::

        >>> filename = 'tests/data/clock_block.dat'
        >>> with open(filename, 'r') as fread:
        ...     xr_data = gnss_io.parse_clock_block(fread)
        ...
        >>> print xr_data.loc["2017-06-22 00:13:30.000000", 'G01']
        <xarray.DataArray ()>
        array(5.612718564585e-05)
        Coordinates:
            time     datetime64[ns] 2017-06-22T00:13:30
            prn      |S4 'G01'
    """

    block_dtype = {
        'names': ('type', 'prn', 'year', 'month', 'day', 'hour', 'minute',
                  'second', 'flag', 'clock', 'sigma'),
        'formats': ('S2', 'S4', 'int', 'int', 'int', 'int', 'int',
                    'float32', 'int', 'float32', 'float32'),
    }

    data = np.loadtxt(block_stream, dtype=block_dtype)
    strtime_list = ["%04d-%02d-%02d %02d:%02d:%06.3f" %
                    (year, month, day, hour, minute, second)
                    for year, month, day, hour, minute, second in
                    zip(data['year'], data['month'], data['day'],
                        data['hour'], data['minute'], data['second'])]

    objtime_list = [pd.to_datetime(t) for t in strtime_list]
    objtime_set = set(objtime_list)
    prn_set = set(data['prn'].astype(str))

    ndata = np.zeros((len(objtime_set), len(prn_set)),
                     dtype=np.float64) + np.nan

    coord_prn = sorted(list(prn_set))
    coord_time = sorted(list(objtime_set))

    objtime_append_list = []

    for clock, prn, objtime in zip(data['clock'], data['prn'].astype(str),
                                   objtime_list):
        if not objtime_append_list:
            # If list is empty, append the time record.
            objtime_append_list.append(objtime)

        if objtime_append_list[-1] < objtime:
            # If time record is not in list, append it.
            objtime_append_list.append(objtime)

        elif objtime_append_list[-1] > objtime:
            # check whether records are in order
            raise RecordsNotInOrder("The last record is not newest")

        itime = len(objtime_append_list) - 1
        iprn = coord_prn.index(prn)
        ndata[itime, iprn] = clock

    xr_data = xr.DataArray(ndata, coords=[coord_time, coord_prn],
                           dims=['time', 'prn'])

    return xr_data


def read_brdc_file(filename):
    """
    Read brdc file and save to xarray.DataArray. The dims are
    ``'time'``, ``'prn'``, and ``'data'``, which ``'data'`` contains
    brdc items. See example usage.

    :param filename: filename of brdc file.
    :type file: string
    :return: brdc data
    :rtype: xarray.DataArray

    Example usage::

      >>> filename = 'tests/data/brdc1070.17n'
      >>> xr_brdc = gnss_io.read_brdc_file()
      >>> print xr_brdc.dims
      ('time', 'prn', 'data')
      >>> print xr_brdc.coords['data']
      <xarray.DataArray 'data' (data: 29)>
      array(['SVclockBias', 'SVclockDrift', 'SVclockDriftRate', 'IODE', 'Crs',
       'DeltaN', 'M0', 'Cuc', 'Eccentricity', 'Cus', 'sqrtA', 'TimeEph', 'Cic',
       'OMEGA', 'CIS', 'Io', 'Crc', 'omega', 'OMEGA DOT', 'IDOT', 'CodesL2',
       'GPSWeek', 'L2Pflag', 'SVacc', 'SVhealth', 'TGD', 'IODC', 'TransTime',
       'FitIntvl'],
      dtype='|S16')
      Coordinates:
        * data     (data) |S16 'SVclockBias' 'SVclockDrift'  ...
    """
    xr_brdc = None
    if not path.isfile(filename):
        raise IOError("No such file. %s" % filename)
    with open(filename, 'rb') as fread:
        while True:
            line = fread.readline()
            line = line.decode()
            if not line:
                break
            if "END OF HEADER" in line:
                xr_brdc = parse_brdc_block(fread)
        return xr_brdc


def parse_brdc_block(fstream):
    """
    Parse brdc stream to xarray.DataArray. The `fstream` is file
    stream that omited the file header.

    :param fstream: File object that opened.
    :type fstream: file
    :return: brdc data
    :rtype: xarray.DataArray

    Example usage::

        >>> fn = "tests/data/brdc_block.dat"
        >>> with open(fn, 'r') as fstream:
        ...    xr_brdc = gnss_io.parse_brdc_block(fstream)
        ...
        >>> print xr_brdc.loc['2017-04-17 00:00:00.0', 'G01', 'Crc']
        217.125000000

    """
    n_valid_items = 29
    objtime_list, prn_list, items_list = _brdc_stream2list(fstream)
    prn_set = set(prn_list)
    pd_time_list = [pd.to_datetime(t) for t in objtime_list]
    pd_time_set = set(pd_time_list)

    ndata = np.zeros((len(pd_time_set), len(prn_set),
                      n_valid_items), dtype=np.float64) + np.nan

    coords_prn = sorted(list(prn_set))
    coords_pd_time = sorted(list(pd_time_set))

    for prn, pd_time, items in zip(prn_list, pd_time_list, items_list):
        # prn = 'G%02d' % iprn
        idx_time = coords_pd_time.index(pd_time)
        idx_prn = coords_prn.index(prn)
        ndata[idx_time, idx_prn, :] = items

    coords = {'time': coords_pd_time,
              'prn': coords_prn,
              'data': ['SVclockBias', 'SVclockDrift', 'SVclockDriftRate',
                       'IODE', 'Crs', 'DeltaN', 'M0',
                       'Cuc', 'Eccentricity', 'Cus', 'sqrtA',
                       'TimeEph', 'Cic', 'OMEGA', 'CIS',
                       'Io', 'Crc', 'omega', 'OMEGA DOT',
                       'IDOT', 'CodesL2', 'GPSWeek', 'L2Pflag',
                       'SVacc', 'SVhealth', 'TGD', 'IODC',
                       'TransTime', 'FitIntvl']}
    dims = ['time', 'prn', 'data']
    xr_brdc = xr.DataArray(ndata, coords=coords, dims=dims)

    return xr_brdc


def _brdc_stream2list(fstream):
    """
    Get brdc block from file and parse block then append prn, time and
    all items to lists.
    """

    # In this context, one record means one satellite's parameters
    # in one epoch.

    ncount = 19  # How many digits of each number.
    # nitems = 31  # How many items in each record
    n_valid_items = 29   # How many valid items in each record.
    nline_each_block = 8   # How many lines of each record
    objtime_list = []  # list to save all records' time
    prn_list = []   # list to save PRNs of all records.
    items_list = []  # list to save items of all records

    # objtime_list, prn_list and items_list are same length with records.

    block_flag = {'nlines': nline_each_block}
    while True:
        brdc_block_list = derive_lines(fstream, block_flag)

        if len(brdc_block_list) != nline_each_block:
            break
        line_combine = ''.join([line[3:].rstrip()
                                for line in brdc_block_list[1:]])

        all_in_line = brdc_block_list[0].rstrip() + line_combine
        all_in_line = all_in_line.replace('D', 'E')
        strio = BytesIO(all_in_line[22:].encode())
        items = np.genfromtxt(strio, delimiter=ncount)

        try:
            iprn = int(all_in_line[:2])
        except ValueError as exception:
            raise ValueError("Cannot convert satellite prn to int "
                             + str(exception))

        if len(items) < n_valid_items - 1:
            raise ValueError("Items in each record is not %s" % n_valid_items)
        valid_items = np.zeros(n_valid_items)
        n_valid_exists = len(items) if len(
            items) < n_valid_items else n_valid_items
        valid_items[:n_valid_exists] = items[:n_valid_exists]
        items_list.append(valid_items)
        objtime = gnss_time.strtime2datetime(all_in_line[2:22])
        objtime_list.append(objtime)
        prn_list.append('G%02d' % iprn)
    return objtime_list, prn_list, items_list


def derive_lines(fstream, block_flag, fallback_last_line=False):
    """
    Derive several lines from file stream. ``block_flag`` is a dictionary
    that tell program how to identity data block. Four key-value pairs are
    contained, which are::

         {
          "start_cond": operator1_list,
          "stop_cond": operator2_list,
          "comment": operator3_list,
          "nlines": n
          }

    ``operator1_list`` and ``operator2_list`` are ``list`` type. Each list
    contains  operator tuples that can judge whether the line matchs
    conditions.
    Each tuple has two item, ``operator`` and ``parameter``. And The
    ``operator`` should be one of three items ::

        operator.__contains__, str.startswith, str.endswith

    The operator dictionary can be constructed like
    ``(str.endswith, 'BLOK END)``
    So ``operator1_list``  and ``operator1_list`` can be::

        op_contains_tuple = (operator.__contains__, 'CONTAINS')
        op_endswith_tuple = (str.endswith, "BLOCK END")
        op_endswith_zero_tuple = (str.endswith, "0.00000000")
        op_startswith_tuple = (str.startswith, "START OF")
        op_startswith_star_tuple = (str.startswith, "*")

        op_blockstart_list = [op_startswith_star_tuple, ]
        op_blockstop_list = [op_endswith_tuple, ]

    So if you derive block from ``derive_block.dat`` like::

      >>> block_flag = {"start_cond": op_blockstart_list, }
      >>> with open("tests/data/derive_block.dat", 'r') as fs:
      ...     gnss_io.derive_lines(fs, block_flag)
      ...     fs.close()

    If the parameter ``fallback_last_line`` is True, the cursor will seek
    to beginning of last line.

    :param fstream: file object where want to derive content.
    :type fstream: file
    :param block_flag: see code example.
    :type block_flag: dictionary
    :param fallback_last_line: fallback cursor or not
    :type fallback_last_line: bool
    :return: lines derived from file
    :rtype: list
    """
    bool_start_stop_exists = block_flag.get('start_cond') \
        or block_flag.get('stop_cond')
    bool_nline_exists = bool(block_flag.get('nlines'))
    if bool_start_stop_exists == bool_nline_exists:
        raise ValueError("nlines should be None if start_cond \
 or stop_cond is not empty and should not be None if start_flag\
 and stop_flag are empty")

    start_cond_list = block_flag.get('start_cond') \
        if block_flag.get('start_cond') else []

    stop_cond_list = block_flag.get('stop_cond') \
        if block_flag.get('stop_cond') else []

    comment_cond_list = block_flag.get("comment") \
        if block_flag.get("comment") else []

    nlines = block_flag.get('nlines') \
        if block_flag.get('nlines') else None

    # status of derive mode. True means turn on and False means off
    # Turn on derive mode when start_cond_list is empty
    derive_mode_status = False if start_cond_list else True

    # Whether last line is derived
    last_line_derived = False

    outlines = []  # list of line for return
    iline = 0  # How many lines in the variable outlines
    while True:
        line = fstream.readline()
        line = line.decode()  # unicode
        comment_flag_occur = any([op(line, para)
                                  for op, para in comment_cond_list])

        if comment_flag_occur:
            continue

        last_line_derived = derive_mode_status
        # judge line match block started conditions or not
        start_flag_occur = any([op(line, para)
                                for op, para in start_cond_list])
        # judge line match block end conditions or not
        stop_flag_occur = any([op(line, para)
                               for op, para in stop_cond_list])

        # If line match block started condition, seek to the beginning
        # of this line, and exit the loop
        if derive_mode_status and start_flag_occur:
            fstream.seek(-len(line), 1)
            derive_mode_status = False
            break

        # Turn on derive mode if start_flag_occur
        if start_flag_occur:
            derive_mode_status = True

        # Turn off derive mode if stop_flag_occur derive mode
        if derive_mode_status and stop_flag_occur:
            derive_mode_status = False

        # print start_flag_occur, stop_flag_occur, derive_mode_status, line,
        # If line is invalid(when end of file), exit a loop
        if not line:
            break

        if derive_mode_status:
            iline += 1
            outlines.append(line)

        # exit the loop when lines number are equal to assigned
        if nlines and iline >= nlines:
            break

        # Exit the loop when derive mode turn off.
        if last_line_derived and stop_flag_occur and not derive_mode_status:
            iline += 1
            outlines.append(line)
            break

    if fallback_last_line and outlines:
        fstream.seek(-len(outlines[-1]), 1)
    return outlines


def read_sp3_file(filename):
    """ Read sp3 file.

    :param filename: filename of sp3 file.
    :type filename: string
    :return: data of sp3 file
    :rtyep: xarray.DataArray

    Example Usage::

      >>> sp3_filename = "tests/data/igs19531.sp3"
      >>> xr_sp3 = gnss_io.read_sp3_file(sp3_filename)
      >>> print xr_sp3.loc['2017-05-22 23:45:00.000', 'G32', 'clock']
      <xarray.DataArray ()>
      array(-420914.752)
      Coordinates:
        prn      |S3 'G32'
        data     |S5 'clock'
        time     datetime64[ns] 2017-05-22T23:45:00

    """

    head_flag = {
        'start_cond': [],
        'stop_cond': [(str.startswith, "*")],
        'nlines': None
    }
    with open(filename, 'rb') as fread:
        head_lines = derive_lines(fread, head_flag,
                                  fallback_last_line=True)
        header = _parse_sp3_header(head_lines)
        xr_sp3 = _parse_sp3_blocks(fread, header)
        return xr_sp3


def _parse_orbits_clocks_line(line):
    """Parse one line in Orbits/Clocks file.

    Example Usage::

      >>> line = ('1060 2 1954  259200.0 G01    42      2.839    0.525'
      ... '    0.772    1.006      0.00000    0.00001    0.00006    0.00001'
      ... '      0.00000')
      >>> dt, prn, orb, clk = gnss_io._parse_orbits_clocks_line(line)
      >>> print(dt)

    """
    if len(line.strip('\n')) < 128:
        raise ListTooShortError("Len is too shord: %d" % len(line))
    try:
        gpsw, sow = int(line[7:11]), float(line[13:21])

        iode = int(line[27:31])
        prn = line[22:25]
        orb_data = [iode,
                    float(line[43:51]),
                    float(line[52:60]),
                    float(line[61:69]),
                    float(line[83:93]),
                    float(line[94:104]),
                    float(line[105:115])]
        clk_data = [iode,
                    float(line[32:42]),
                    float(line[72:82]),
                    float(line[117:128])]
    except TypeError as exception:
        raise TypeError(
            "cannot convert string to number :%s" % str(exception))
    dt = gnss_time.toe2datetime(gpsw, sow)
    return dt, prn, orb_data, clk_data



def _parse_ssr_block(fread):
    NSAT_GPS = 32
    NSAT_GLO = 24
    NSAT = NSAT_GPS + NSAT_GLO
    N_ITEMS_CLOCK = 4
    N_ITEMS_ORBIT = 7

    prn_list = ['G%02d' % gprn for gprn in range(1, NSAT_GPS + 1)] \
        + ['R%02d' % rprn for rprn in range(1, NSAT_GLO + 1)]
    prn_order_dict = dict([(prn, idx)
                           for idx, prn in enumerate(prn_list)])
    clock_srr = []
    orbit_srr = []
    clk_time_list = []
    orb_time_list = []
    block_flag = {
        "start_cond": [(str.startswith, ">"),
                       (str.startswith, "!")]}
    while True:
        block = derive_lines(fread, block_flag, True)
        if not block:
            break
        ssr_head = block[0]

        if "! Orbits/Clocks" in ssr_head:

            ssr_lines = block[1:]
            clk_data = np.zeros((NSAT, N_ITEMS_CLOCK),
                                dtype=np.float64) + np.nan
            orb_data = np.zeros((NSAT, N_ITEMS_ORBIT),
                                dtype=np.float64) + np.nan
            # one_record = ssr_lines[0]
            for item in ssr_lines:
                dt, prn, orb_epoch, clk_epoch = _parse_orbits_clocks_line(item)
                iprn = iprn = prn_order_dict[prn]
                clk_data[iprn] = clk_epoch
                orb_data[iprn] = orb_epoch
            clk_time_list.append(dt)
            orb_time_list.append(dt)
            clock_srr.append(clk_data)
            orbit_srr.append(orb_data)
        elif "CLOCK" in ssr_head:
            # clk_time_list.append(gnss_time.arrtime2datetime(temp[2:]))
            clk_time_list.append(gnss_time.strtime2datetime(ssr_head[8:29]))
            clk_data = block[1:]
            ndata = np.zeros((NSAT, N_ITEMS_CLOCK),
                             dtype=np.float64) + np.nan
            for item in clk_data:
                if item[0:3] not in prn_list:
                    continue
                iprn = prn_order_dict[item[0:3]]
                try:
                    ndata[iprn] = [int(item[3:15]), float(item[15:26]),
                                   float(item[26:37]), float(item[37:48])]
                except TypeError as exception:
                    raise TypeError(
                        "Cannot convert string to number: %s" % str(exception))

            clock_srr.append(ndata)

        elif "ORBIT" in ssr_head:
            # orb_time_list.append(gnss_time.arrtime2datetime(temp[2:]))
            orb_time_list.append(gnss_time.strtime2datetime(ssr_head[8:29]))
            orb_data = block[1:]
            ndata = np.zeros((NSAT, N_ITEMS_ORBIT),
                             dtype=np.float64) + np.nan
            for item in orb_data:
                if item[0:3] not in prn_list:
                    continue
                iprn = prn_order_dict[item[0:3]]
                try:
                    ndata[iprn] = [int(item[3:15]), float(item[15:26]),
                                   float(item[26:37]),  float(item[37:48]),
                                   float(item[48:62]), float(item[62:73]),
                                   float(item[73:84])]
                except TypeError as exception:
                    raise TypeError(
                        "Cannot convert string to number: %s" % str(exception))

            orbit_srr.append(ndata)
        else:
            pass

    # parse list to xarray
    clk_coords = {
        'time': clk_time_list,
        'prn': prn_list,
        'data': ['IODE', 'C0', 'C1', 'C2']
    }
    clk_dims = ['time', 'prn', 'data']
    clk_units = {'IODE': '', 'C0': 'm', 'C1': 'm/s', 'C2': ' m/s^2'}
    clk_np = np.array(clock_srr, dtype=np.float64)
    clk_xr = xr.DataArray(clk_np, coords=clk_coords, dims=clk_dims)
    clk_xr.attrs['units'] = clk_units

    orb_coords = {
        'time': orb_time_list,
        'prn': prn_list,
        'data': ['IODE', 'Radial', 'Along', 'Out-of-plane', 'vel_radial',
                 'vel_along', 'vel_out']
    }
    orb_dims = ['time', 'prn', 'data']
    orb_units = {'IODE': '', 'Radial': 'm', 'Along': 'm', 'Out-of-plane': 'm',
                 'vel_radial': 'm', 'vel_along': 'm', 'vel_out': 'm'}
    orb_np = np.array(orbit_srr, dtype=np.float64)
    orb_xr = xr.DataArray(orb_np, coords=orb_coords, dims=orb_dims)
    orb_xr.attrs['units'] = orb_units
    return clk_xr, orb_xr


def _parse_sp3_blocks(fstream, header):
    """Parse sp3 blocks
    """
    block_flag = {
        'start_cond': [(str.startswith, "*")],
        'stop_cond': [],
        'comment': [(str.startswith, "EOF")],
        'nlines': None
    }
    prn_set = set(header['prn_list'])
    prn_list = sorted(list(prn_set))
    prn_order_dict = dict([(prn, idx)
                           for idx, prn in enumerate(prn_list)])
    epochs_data = []
    obj_time_list = []
    while True:
        epoch_block = derive_lines(fstream, block_flag, True)
        if not epoch_block:
            break

        epoch_time, epoch_data = _parse_sp3_block(
            epoch_block, prn_order_dict)
        obj_time_list.append(epoch_time)
        epochs_data.append(epoch_data)

        # break

    ndata = np.array(epochs_data, dtype=np.float64)

    coords = {'time': obj_time_list,
              'prn': prn_list,
              'data':  ['x', 'y', 'z', 'clock']}
    dims = ['time', 'prn', 'data']
    units = {'x': 'meter', 'y': 'meter', 'z': 'meter', 'clock': 'ns'}
    xr_sp3 = xr.DataArray(ndata, coords=coords,
                          dims=dims)
    xr_sp3.attrs['units'] = units
    return xr_sp3


def _parse_sp3_block(block_lines, prn_order_dict):
    """ Parse a block of a epoch.
    """
    if len(block_lines) < 2:
        raise ListTooShortError("block contains less then 2 line")
    epoch_header_line = block_lines[0]
    objtime = gnss_time.strtime2datetime(epoch_header_line[1:])

    block_byte = BytesIO("".join(block_lines[1:]).encode())
    names = ['type', 'prn', 'x', 'y', 'z', 'clock',
             'xsigma', 'ysigma', 'zsigma', 'clksigma']
    delimiter = [1, 3, 14, 14, 14, 14, 3, 3, 3, 4]
    block_data = np.genfromtxt(block_byte, dtype=None, names=names,
                               delimiter=delimiter,)
    epoch_data = np.zeros((len(prn_order_dict), 4),
                          dtype=np.float64) + np.nan
    if block_data['prn'].ndim != 0:
        idx_arr = [prn_order_dict[prn]
                   for prn in block_data['prn'].astype(str)]
        epoch_data[idx_arr] = np.transpose([block_data['x'] * 1e3,
                                            block_data['y'] * 1e3,
                                            block_data['z'] * 1e3,
                                            block_data['clock'] * 1e3])
    else:
        # 0-array ndarray. can only get data by this way
        # Maybe there will be other ways. But by now I can only do like this.
        prn = str(block_data['prn'].astype(str))
        idx_prn = prn_order_dict[prn]
        epoch_data[idx_prn] = [block_data['x'] * 1e3,
                               block_data['y'] * 1e3,
                               block_data['z'] * 1e3,
                               block_data['clock'] * 1e3]
    return objtime, epoch_data


def _parse_sp3_header(head_lines):
    """ Parse sp3 header. Will return a dictionary contains keys::

        'nepoch', 'frame', 'orbit_type', 'agency', 'time', 'nast'
        'prn_list', 'gpsw', 'sow', 'interval', 'mjd', 'frac_day'

    """

    if len(head_lines) < 3:
        raise ListTooShortError("sp3 file header too short")
    first_line = head_lines[0]
    header = _parse_sp3_first_line(first_line)

    second_line = head_lines[1]
    header4update = _parse_sp3_second_line(second_line)
    header.update(header4update)

    third_line = head_lines[2]
    try:
        nsat = int(third_line[4:6])
    except TypeError as exception:
        raise TypeError("Cannot convert satelite number to number: " +
                        str(exception))
    header['nsat'] = nsat

    # Because there are 17 satellites PRN in each line.
    nline_of_sats = int(math.ceil(nsat / 17.))

    # And from third line to enumerate satellites PRNs
    prn_list = _parse_sp3_prnlist(
        head_lines[2:2 + nline_of_sats])
    header['prn_list'] = prn_list
    return header


def _parse_sp3_prnlist(lines):
    """Parse satellites list.
    """
    strprns = ''.join([line[9:60] for line in lines])
    prn_list = [strprns[i * 3: (i + 1) * 3]
                for i in range(int(len(strprns) / 3))
                if not strprns[i * 3: (i + 1) * 3].startswith(' ')]
    return prn_list


def _parse_sp3_second_line(second_line):
    """Parse the second line of sp3 file.
    """

    try:
        gw = int(second_line[3:7])
        sow = float(second_line[8:23])
        interval = float(second_line[25:38])
        mjd = int(second_line[39:44])
        fracdy = float(second_line[45:60])
    except TypeError as exception:
        raise TypeError("Cannot convert to number: " + str(exception))
    header = defaultdict(None)
    header['gpsw'] = gw
    header['sow'] = sow
    header['interval'] = interval
    header['mjd'] = mjd
    header['frac_day'] = fracdy
    return header


def _parse_sp3_first_line(first_line):
    """Parse the first line of sp3 file.
    """
    if len(first_line) < 60:
        raise ListTooShortError("string too short")

    header = defaultdict(None)
    strtime = first_line[3:31]

    obj_head_time = gnss_time.strtime2datetime(strtime)
    header['type'] = first_line[2]
    try:
        nepoch = int(first_line[32:39])
    except TypeError as exception:
        raise TypeError("cannot convert epochs number to number: "
                        + str(exception))
    header['nepoch'] = nepoch

    header['frame'] = first_line[46:51]
    header['orbit_type'] = first_line[52:55]
    header['agency'] = first_line[57:60]
    header['time'] = obj_head_time
    return header


def read_rnx2_file(filename):
    """Read rinex2.x file.

    :param filename: filename of rinex2.x
    :type filename: string
    :return: data in rinex2.x file
    :rtype: xarray.DataArray
    """
    pass


# def read_rnx3_file(filename):
#     if not path.isfile(filename):
#         raise IOError("file not exists. %s" % filename)

#     with open(filename, 'rb') as fread:
#         line = fread.readline().decode()
#         if line.startswith('>') or line.startswith('>'):
#             fread.seek(-len(line), 1)
#             # xr_data = parse_clock_block(fread)
#         else:
#             for line in fread:
#                 line = line.decode()
#                 if 'END OF HEADER' in line:
#                     xr_data = parse_rnx3_block(fread)
#                     break
#         return xr_data


def parse_rnx3_block(fread):
    pass


def read_soltab_file(filename):
    """Read solar tabluar.

    :param filename: filename of soltab
    :type filename: string
    :return: data contained in soltab file
    :rtype: xarray.DataArray
    """
    sol_data = np.loadtxt(filename, dtype={'names': ("mjd", "x", "y", "z"),
                                           "formats": ("i", "i", "i", "i")},
                          skiprows=2)

    coords = {'time': sol_data['mjd'],
              'data':  ['x', 'y', 'z']}
    dims = ['time', 'data']
    units = {'time': 'Modified Julian Date', 'x': 'meter',
             'y': 'meter', 'z': 'meter'}
    data = np.transpose(np.array([sol_data['x'],
                                  sol_data['y'],
                                  sol_data['z']]))

    xr_sol = xr.DataArray(data, coords=coords,
                          dims=dims)
    xr_sol.attrs['units'] = units
    return xr_sol


def read_south_csv(filename):
    """Read solution of South RTK CSV file
    """
    with open(filename, "rb") as fr:
        xyz_list = []
        obj_time_list = []
        lines = fr.readlines()
        for line in lines:
            line = str(line)  # .decode("utf-8")
            fields = line.split(",")
            time_field = fields[8].replace(":", " ").replace("-", " ")
            # print(time_field)
            delta = datetime.timedelta(hours=8)
            obj_time = gnss_time.strtime2datetime(
                time_field) - delta + datetime.timedelta(seconds=18)
            str_lat_dms = fields[5]
            str_lon_dms = fields[6]
            lat = str_dms2dd(str_lat_dms)
            lon = str_dms2dd(str_lon_dms)
            hgt = float(fields[7])
            x, y, z = gnss_geodesy.blh2xyz(lat, lon, hgt)
            xyz = [x, y, z]
            if obj_time in obj_time_list:
                continue
            xyz_list.append(xyz)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_pos


def str_dms2dd(str_dms, split=":"):
    """Convert dms to dd
    """
    fields = str_dms.split(split)
    d0 = int(fields[0])
    d1 = int(fields[1])
    d2 = float("%s.%s" % (fields[2][:2], fields[2][2:]))
    return d0 + d1 / 60. + d2 / 3600.


def read_feng_pos(filename):
    with open(filename, "r") as fread:
        xyz_list = []
        obj_time_list = []
        lines = fread.readlines()
        for line in lines[1:]:
            fields = line[23:].split()
            str_time = line[:19].replace("-", " ").replace(":", " ")
            # print(str_time)
            obj_time = gnss_time.strtime2datetime(
                str_time) + datetime.timedelta(seconds=1)
            try:
                x = float(fields[0])
                y = float(fields[1])
                z = float(fields[2])
            except TypeError as e:
                print(str(e))
                continue
            except IndexError as e:
                print(str(e))
                continue
            if obj_time in obj_time_list:
                continue
            xyz_list.append([x, y, z])
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_pos


def ppi2shaper(filename, outfile, str_start_time, str_stop_time):
    xr_ppi = read_ppi_shaper(filename)
    xr_ppi = xr_ppi.loc[str_start_time:str_stop_time, :]
    with open(outfile, "w") as fwrite:
        for record in xr_ppi:
            strtime = str(record.coords['time'].values).replace(
                '-', ',').replace('T', ',').replace(':', ',')
            x = record.loc['x'].values
            y = record.loc['y'].values
            z = record.loc['z'].values
            outline = "#PPISOL,%s,%2d,%3d,%8.4f,%8.4f,%8.4f,\
%.4f,%.4f,%.4f\n" % (
                strtime[:23], 0, 0, 0, 0, 0, x, y, z)
            fwrite.writelines(outline)
    return xr_ppi


def read_ppi_v3(filename):
    """

    :param filename:
    :return:
    """
    with open(filename) as fread:
        lines = fread.readlines()
        lines = [line.replace('#PPISOL,', '').replace(',', ' ').rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith("%"):
                continue
            if len(line) < 80:
                raise ListTooShortError(
                    "Line length: %d, line too short %s" % (len(line), line))
            str_time = line[:23]
            obj_time = gnss_time.strtime2datetime(str_time)
            items = line[24:].split()
            try:
                blh = [float(tmp) for tmp in items[5:8]]
                x, y, z = gnss_geodesy.blh2xyz(blh[0], blh[1], blh[2])
                xyz = [x, y, z]
                ns = int(items[1])
                pdop = float(items[3])
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))
            xyzn = xyz + [ns] + [pdop]
            if obj_time in obj_time_list:
                continue
            xyz_list.append(xyzn)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z', 'ns', 'pdop']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_pos


def read_ppi_shaper(filename):
    """Read ppi shaper file solution file.
    """
    with open(filename) as fread:
        lines = fread.readlines()
        lines = [line.replace('#PPISOL,', '').replace(',', ' ').rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith("%"):
                continue
            if len(line) < 80:
                raise ListTooShortError(
                    "Line length: %d, line too short %s" % (len(line), line))
            str_time = line[:23]
            obj_time = gnss_time.strtime2datetime(str_time)
            items = line[24:].split()
            try:
                status = int(line[26])
                xyz = [float(tmp) for tmp in items[5:8]]
                ns = int(items[1])
                pdop = float(items[3])
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))
            xyzn = xyz + [ns] + [pdop] + [status]
            if obj_time in obj_time_list:
                continue
            xyz_list.append(xyzn)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z', 'ns', 'pdop', 'status']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_pos


def read_trimble_solution(filename, delta=None):
    """Read trimple RTK solution file.
    """
    with open(filename, 'r') as fread:
        xyz_list = []
        obj_time_list = []
        lines = fread.readlines()
        # lines = [line.replace(',', ' ').replace('d', ' ').replace("'", ' ')
        #          .replace('"', ' ').replace(':', ' ').replace('/', ' ')
        #          .rstrip('\n')
        #          for line in lines]
        lines = [line.replace(',"', ",").replace('""', "").rstrip('\n')
                 for line in lines]
        for line in lines:
            items = line.split(',')
            str_lat = items[1]
            str_lon = items[2]
            str_hgt = items[3]
            str_time1 = items[5]
            lat = dms2dd(str_lat)
            lon = dms2dd(str_lon)
            hgt = float(str_hgt)
            x, y, z = gnss_geodesy.blh2xyz(lat, lon, hgt)
            xyz = [x, y, z, 0, 0]
            # str_time = "%s %s" % (strdate, str_time1.split()[
            #                       1].replace(":", " "))
            str_time = str_time1.replace(":", " ").replace("/", " ")
            obj_time = gnss_time.strtime2datetime(
                str_time)
            # jd1 = gnss_time.ymd2jd(2018, 6, 10)
            # jd0 = gnss_time.ymd2jd(1882, 5, 6)
            # deltadays = jd1 - jd0
            # delta = datetime.timedelta(days=deltadays, hours=22,
            #                            minutes=27, seconds=58 + 18)
            if delta:
                obj_time = obj_time + delta
            else:
                pass
                # datetime.timedelta(days=deltadays, hours=22,
                #                    minutes=27, seconds=58 + 18)

            # print(obj_time, x, y, z)
            # break
            if obj_time in obj_time_list:
                continue
            xyz_list.append(xyz)
            obj_time_list.append(obj_time)

        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z', 'ns', 'pdop']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
    return xr_pos


def south2ppishaper(filename, outfile,
                    str_start_time, str_stop_time, delta_xyz):
    xr_south = read_south_csv(filename)
    xr_south = xr_south.loc[str_start_time:str_stop_time]
    with open(outfile, "w") as fwrite:
        for record in xr_south:
            strtime = str(record.coords['time'].values).replace(
                '-', ',').replace('T', ',').replace(':', ',')
            x = record.loc['x'].values + delta_xyz[0]
            y = record.loc['y'].values + delta_xyz[1]
            z = record.loc['z'].values + delta_xyz[2]
            outline = "#PPISOL,%s,%2d,%3d,%8.4f,%8.4f,%8.4f,\
%.4f,%.4f,%.4f\n" % (
                strtime[:23], 0, 0, 0, 0, 0, x, y, z)
            fwrite.writelines(outline)
    return xr_south


def trimble2ppishaper(filename, outfile,
                      str_start_time, str_stop_time, delta_time, delta_xyz):
    """
    Convert Trimble solution to PPI shaper file.
    """
    xr_tr = read_trimble_solution(filename, delta_time)
    # print(xr_tr.coords['time'].values[0], xr_tr.coords['time'].values[-1])
    xr_tr = xr_tr.loc[str_start_time:str_stop_time]
    with open(outfile, "w") as fwrite:
        for record in xr_tr:
            strtime = str(record.coords['time'].values).replace(
                '-', ',').replace('T', ',').replace(':', ',')
            x = record.loc['x'].values + delta_xyz[0]
            y = record.loc['y'].values + delta_xyz[1]
            z = record.loc['z'].values + delta_xyz[2]
            outline = "#PPISOL,%s,%2d,%3d,%8.4f,%8.4f,%8.4f,\
%.4f,%.4f,%.4f\n" % (
                strtime[:23], 0, 0, 0, 0, 0, x, y, z)
            fwrite.writelines(outline)
    return xr_tr


def delta_trimble(str_utc, str_tr):
    time_utc = gnss_time.strtime2datetime(
        str_utc) + datetime.timedelta(seconds=18)
    time_tr = gnss_time.strtime2datetime(str_tr)
    return time_utc - time_tr


def dms2dd(strdms):
    """Convert dms to dd.
    22d43'25.99823"
    """
    degree = int(strdms.split('d')[0])
    mi = int(strdms.split("'")[0].split('d')[1])
    sec = float(strdms.split("'")[1].split('"')[0])
    return degree + mi / 60. + sec / 3600.


def read_peng_solution(filename):
    with open(filename) as fread:
        lines = fread.readlines()
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith("%"):
                continue
            if len(line) < 80:
                raise ListTooShortError(
                    "Line length: %d, line too short %s" % (len(line), line))
            str_time = line[:23].replace("/", " ").replace(":", " ")

            obj_time = gnss_time.strtime2datetime(str_time)
            items = line[24:].split()
            try:
                xyz = [float(tmp) for tmp in items[:3]]
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))

            if obj_time in obj_time_list:
                continue
            xyz_list.append(xyz)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_pos
    pass

def read_hmx_solution(filename):
    with open(filename, "r") as fread:
        lines = fread.readlines()
        lines = [line.rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith('%'):
                continue
            items = line.split()
            str_time = line[:11]
            str_time = "%s %s" % ("2020 01 08", str_time)
            obj_time = gnss_time.strtime2datetime(str_time)
            try:
                xyz = [float(tmp) for tmp in items[9:12]]
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))
            xyzn = xyz
            xyz_list.append(xyzn)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z']}
        dims = ['time', 'data']
        # ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(xyz_list, coords=coords, dims=dims)
        return xr_pos


def read_meteo(filename):
    """
    气象参数文件格式：

    示例数据

        站名, 时间, 大气湿度, 温度, 大气压
         N1__,2020-01-07 00:00:00,37.20,17.40,892.20

    :param filename:
    :return:
    """
    time_list = list()
    data = list()
    with open(filename, 'r') as fread:
        lines = fread.readlines()
        for line in lines:
            if len(line) == 0:
                continue
            fields = line.rstrip().split(',')
            time_field = fields[1]
            humidity = float(fields[2])
            temperature = float(fields[3])
            atmo_press = float(fields[4])
            time_list.append(gnss_time.strtime2datetime(time_field)+datetime.timedelta(hours=-8))
            data.append([humidity, temperature, atmo_press])

    coords = {'time': time_list,
              'data': ['humidity', 'temperature', 'atmo_press']}
    dims = ['time', 'data']
    ndata = np.array(data, dtype=np.float64)
    xr_data = xr.DataArray(ndata, coords=coords, dims=dims)
    return xr_data


def read_real_ztd(filename):
    """
    读取实测气象参数对流层延迟模型。

    格式：

    N5, 2020-01-06T16:09:00.000000000,  2.064, 0.054

    :param filename:
    :return:
    """
    with open(filename, "r") as fread:
        lines = fread.readlines()
        lines = [line.replace('/', ' ').replace(':', ' ').replace('-', ' ').replace('T', ' ').rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith('%'):
                continue
            if len(line) < 20:
                raise ValueError("line too short %s" % line)
            items = line.split(",")
            site = items[0]
            # print(line)
            obj_time = gnss_time.strtime2datetime(items[1]) + datetime.timedelta(hours=-0)
            zhd = float(items[2])
            zwd = float(items[3])
            ztd = zhd + zwd
            data = [ztd, 0, zhd, zwd]
            xyz_list.append(data)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['ztd', 'rms', 'zhd', 'zwd']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_trop = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_trop

def read_peng_trop(filename):
    """
    Read Peng Wenjie's trop file.

    Example data::

      time                       ztd       rms       zhd       zwd
      2020/01/08 00:00:00.000    2.0632    0.0900    1.9893    0.0739

    :param filename:
    :return:
    """

    with open(filename, 'r') as fread:
        lines = fread.readlines()
        lines = [line.replace('/', ' ').replace(':', ' ').rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith('%') or line.startswith("$"):
                continue
            if len(line) < 30:
                raise ListTooShortError("line too short %s" % line)
            str_time = line[:23]
            obj_time = gnss_time.strtime2datetime(str_time)

            items = line[24:].split()
            try:
                data = [float(tmp) for tmp in items]
                ztd, rms, zhd, zwd = data[0], data[1], data[2], data[3]
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))
            xyzn = [ztd, rms, zhd, zwd]
            xyz_list.append(xyzn)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['ztd', 'rms', 'zhd', 'zwd']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_trop = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_trop

def read_rtklib_solution(filename, type="blh"):
    """Read rtklib solution and return xarray.DataArray.


    Example usage::

      >> xr_pos = gnss_io.read_rtklib_solution("tests/data/kine1640_rtk.pos")
      >> print xr_pos
      <xarray.DataArray (time: 7468, data: 3)>
      array([[-1642547.8851, -3664702.5664,  4939861.1645],
         [-1642547.8827, -3664702.5666,  4939861.1602],
         [-1642547.8839, -3664702.5717,  4939861.16  ],
          ...,
         [-1641904.6557, -3664831.5337,  4939972.6708],
         [-1641904.6562, -3664831.5322,  4939972.6617],
         [-1641904.6609, -3664831.5333,  4939972.668 ]])
      Coordinates:
      * data     (data) |S1 'x' 'y' 'z'
      * time     (time) datetime64[ns] 2017-06-13T16:19:59 ...

    """
    with open(filename, 'r') as fread:
        lines = fread.readlines()
        lines = [line.replace('/', ' ').replace(':', ' ').rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith('%'):
                continue
            if len(line) < 69:
                raise ListTooShortError("line too short %s" % line)
            str_time = line[:23]
            obj_time = gnss_time.strtime2datetime(str_time)
            items = line[24:].split()
            try:
                xyz = [float(tmp) for tmp in items[:3]]
                if type == "blh":
                    lat, lon, hgt = xyz[0], xyz[1], xyz[2]
                    x, y, z = gnss_geodesy.blh2xyz(lat, lon, hgt)
                    xyz[:3] = [x, y, z]
                status = int(items[3])
                ns = int(items[4])
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))
            xyzn = xyz + [ns] + [status]
            xyz_list.append(xyzn)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z', 'ns', "status"]}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)
        return xr_pos


def read_solution(filename):
    """Read generic solution and return xarray.DataArray.

    """
    with open(filename, 'r') as fread:
        lines = fread.readlines()
        lines = [line.rstrip('\n')
                 for line in lines]
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith('%'):
                continue
            items = line.split()
            str_time = "%s %s" % (items[0], items[1])
            obj_time = gnss_time.strtime2datetime(str_time)
            try:
                xyz = [float(tmp) for tmp in items[2:6]]
            except Exception as exception:
                raise TypeError("cannot convert to number %s" % str(line))
            xyzn = xyz
            xyz_list.append(xyzn)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z', 'status']}
        dims = ['time', 'data']
        # ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(xyz_list, coords=coords, dims=dims)
        return xr_pos

def read_iono_file(filename):
    nsat = 32
    with open(filename) as fread:
        lines = fread.readlines()
        lines = [line.rstrip('\n')
                 for line in lines]
        data = list()
        obj_time_list = list()
        prn_list = lines[0].split()[2:]
        nsat = len(prn_list)
        for line in lines[1:]:
            if line.startswith("$"): continue
            str_time = line[:24].replace("/", "-")
            obj_time = gnss_time.strtime2datetime(str_time)
            items = line[25:].split()
            if len(items) != nsat:
                raise Exception("Error: items is not %d" % nsat)
            stec_list = [float(tmp) for tmp in items]
            data.append(stec_list)
            obj_time_list.append(obj_time)
        data = np.array(data)
        data[data==0] = np.nan
        coords = {'time': obj_time_list,
                  'prn': prn_list}
        dims = ['time', 'prn']
        # ndata = np.array(xyz_list, dtype=np.float64)
        xr_iono = xr.DataArray(data, coords=coords, dims=dims)
        return xr_iono



def read_orbit_file(filename, interval=30):
    nsat = 32
    nepoch = 86400/interval
    with open(filename) as fread:
        lines = fread.readlines()
        prn_list = ["G%02d" % tmp for tmp in range(1, nsat+1)]
        data = list()
        obj_time_list = list()
        for line in lines[1:]:
            if line.startswith("$"): continue
            str_time = line[:24].replace("/", "-")
            obj_time = gnss_time.strtime2datetime(str_time)
            items = line[25:].split()
            if len(items) != nsat*3:
                raise Exception("Error: items is not %d * %d" % (nsat, 3))
            data_prn = list(np.reshape(np.array([float(tmp) for tmp in items]),
                                (-1, 3)))
            # data_prn[data_prn==0] = np.nan
            data.append(data_prn)
            obj_time_list.append(obj_time)
        ndata = np.array(data, dtype=np.float64)
        ndata[ndata==0] = np.nan
        coords = {'time': obj_time_list,
                'prn': prn_list,
                'data':  ['x', 'y', 'z']}
        dims = ['time', 'prn', 'data']
        xr_orbit = xr.DataArray(ndata, coords=coords,
                            dims=dims)
        return xr_orbit


def read_dcb_liu(filename):
    dcb = defaultdict()
    with open(filename) as fread:
        lines = fread.readlines()
        for line_tmp in lines:
            line = line_tmp.strip()
            items = line.split()
            dcb[items[0]] = float(items[1])
    return dcb

def _parse_ionex_header(lines):
    """
    parse the header lines in IONEX file. return a dict, which contains keys
    ["start_epoch", "stop_epoch", "interval", ]
    :param lines:
    :return:
    """
    header = defaultdict()
    # header["start_epoch"] =
    for line in lines:
        line = line.rstrip()
        if "EPOCH OF FIRST MAP" in line:
            header["start_epoch"] = gnss_time.strtime2datetime(line[2:37])
        elif "EPOCH OF LAST MAP" in line:
            header["stop_epoch"] = gnss_time.strtime2datetime(line[2:37])
        elif "INTERVAL" in line:
            header["interval"] = int(line[2:6])
        elif "ELEVATION CUTOFF" in line:
            header["cutoff"] = float(line[3:8])
        elif "BASE RADIUS" in line:
            header["radius"] = float(line[2:8])
        elif "HGT1 / HGT2 / DHGT" in line:
            items = line.split()
            header["hgt0"] = float(items[0])
            header["hgt1"] = float(items[1])
            header["dhgt"] = float(items[2])
        elif "LAT1 / LAT2 / DLAT" in line:
            items = line.split()
            header["lat0"] = float(items[0])
            header["lat1"] = float(items[1])
            header["dlat"] = float(items[2])
        elif "LON1 / LON2 / DLON" in line:
            items = line.split()
            header["lon0"] = float(items[0])
            header["lon1"] = float(items[1])
            header["dlon"] = float(items[2])
    return header


def read_iri_web(filename, lat_min=-87.5, lat_max=87.5, lat_step=2.5):
    nlats = int((lat_max - lat_min)/lat_step)+1
    head_flag = {
        'start_cond': [(str.startswith,"yyyy/mmdd(or -ddd)/hh.h):")],
        'stop_cond': [(str.startswith, "-")],
        'nlines': None
    }

    content_flag = {
        'start_cond': [(str.__contains__, "  LATI ELECTRON DENSITY")],
        'stop_cond': [],
        'nlines': nlats+2
    }
    with open(filename, "rb") as fread:
        lons = list()
        profiles = list()
        while True:
            header = derive_lines(fread, head_flag, fallback_last_line=False)
            if not header:
                break
            year, doy, hour, lon = _parse_iri_header(header)
            if lon > 180:
                lon -= 360
            block = derive_lines(fread, content_flag, fallback_last_line=False)
            lats, tecs = _parse_iri_content(block)
            lons.append(lon)
            profiles.append(tecs)
        _, mo, dy = gnss_time.doy2ymd(year, doy)
        nrows = len(profiles[0])
        ncols = len(profiles)
        data1 = np.transpose(np.array(profiles))
        data = np.zeros((nrows, ncols), np.float64)
        data[:, 37:] = data1[:, 1:37]
        data[:, :37] = data1[:, 36:]
        lons1 = [-180] + lons[37:-1] + lons[:37]
        time = gnss_time.strtime2datetime("%04d-%02d-%02d %02d:00:00.00" % (year, mo, dy, hour))
        xr_iri = xr.DataArray([data], coords=[[time], lats, lons1],
                              dims=["time", "lat", "lon"])
        return xr_iri

def _parse_iri_header(header_lines):
    line = header_lines[0].replace("= ", "/").replace(":", "/").rstrip()
    fields = line.split("/")
    # print(fields)
    year = int(fields[3])
    doy = -int(fields[4])
    hour = float(fields[5][:4]) - 25
    lon = float(fields[-2])
    return year, doy, hour, lon


def _parse_iri_content(content_lines, nlats=71):
    idx_tec = str.find(content_lines[1], "TEC")
    lats = list()
    tecs = list()
    for line in content_lines[2:]:
        lat = float(line[:7])
        tec = float(line[idx_tec-3:idx_tec+3])
        lats.append(lat)
        tecs.append(tec)
    return lats, tecs


def read_dst(filename):
    with open(filename, "r") as fread:
        lines = fread.readlines()

        time_list = list()
        values = list()

        for line in lines:
            newline = line.rstrip()
            if newline.endswith("|"):
                continue
            dst = int(newline[-4:])
            time_list.append(gnss_time.strtime2datetime( line[:24]))
            values.append(dst)

        xr_dst = xr.DataArray(values, coords=[time_list], dims=["time"])
        return xr_dst

def _code2prn(char3):
    """
          4->G04
         14->G14
        114->R14
        214->E14
        314->C14
    """
    chars = f"{char3:>3}"
    sysid = chars[0].replace(
        " ", "G").replace(
        "1", "R").replace(
        "2", "E").replace(
        "3", "C")
    satid = chars[1:3].replace(" ", "0")
    prn = f"{sysid}{satid}"
    return prn


def _sec2time(sec, date, deltaday=DELTA_DAY.IS_CURDAY):
    return np.datetime64(date,"ns")+np.timedelta64(deltaday.value, "D")+np.timedelta64(int(sec), "s")


def _check_if_cur_day(sec, iline, linecount, lineratio=0.02, max_overflow_min=30, interval=15):
    """
    sec: sec in day
    iline: line number
    max_line: 前后多少行才进入判断
    max_overflow: max overflow (min)
    interval: sample
    """
    seconds_in_day = 86400
    which_day = DELTA_DAY.IS_CURDAY
    ratio = iline/linecount
    if iline/linecount > lineratio and iline/linecount < 1-lineratio:
        pass
    elif ratio < lineratio:
        if sec > seconds_in_day - max_overflow_min*60:
            which_day = DELTA_DAY.IS_PREDAY
        else:
            pass
    elif ratio > lineratio:
        if sec < max_overflow_min*60:
            which_day = DELTA_DAY.IS_NXTDAY
        else:
            pass
    return which_day


def read_refl_snr(filename, time=datetime.datetime.today(), interval=15):
    data = np.loadtxt(filename, dtype=float)
    nrow, ncols = data.shape
    codelist = list(set([int(tmp) for tmp in data[:, 0]]))
    prnlist = [_code2prn(_) for _ in codelist]

    time0 = _sec2time(data[0, 3], time, _check_if_cur_day(data[0, 3], 0, len(data[:, 3])))
    time1 = _sec2time(data[-1, 3], time, _check_if_cur_day(data[-1, 3], len(data[:, 3]), len(data[:, 3])))
    nepoch = int((time1-time0)/np.timedelta64(interval, "s")) + 1
    time_list = [time0+np.timedelta64(_*interval, "s") for _ in range(nepoch)]
    snr_data = np.zeros((len(time_list), len(prnlist), ncols-3))
    for iline, linedata in enumerate(data):
        prn = _code2prn(f"{int(linedata[0]):3d}")
        iprn = prnlist.index(prn)
        time_epoch = _sec2time(linedata[3], time, _check_if_cur_day(linedata[3], iline, len(data[:, 3])))
        itime = int((time_epoch - time0) / np.timedelta64(interval, "s"))
        snr_data[itime, iprn] = np.concatenate((linedata[1:3], linedata[5:]))
    snr_data[snr_data == 0] = np.nan

    xr_snr = xr.DataArray(snr_data, dims=["time", "prn", "data"],
                              coords=[time_list, prnlist, ["ele", "azi"] + ["S6", "S1", "S2", "S5", "S7", "S8"][:ncols-5]])
    return xr_snr

    # for iline, (code, ele, azi, sec, eler, s6, s1, s2, s5, s7, s8) in enumerate(zip(
    #     data["code"], data["ele"], data["azi"], data["sec"], data["eler"],
    #     data["S6"], data["S1"], data["S2"], data["S5"], data["S7"], data["S8"])) :
    #     prn = _code2prn(code)
    #     iprn = prnlist.index(prn)
    #     time_epoch = _sec2time(sec, time, _check_if_cur_day(sec, iline, len(data["sec"])))
    #     itime = int((time_epoch-time0)/np.timedelta64(interval, "s"))
    #     snr_data[itime, iprn] = np.array([ele, azi, s6, s1, s2, s5, s7, s8])
    # snr_data[snr_data==0]=np.nan
    # xr_snr = xr.DataArray(snr_data, dims=["time", "prn", "data"],
    #                       coords=[time_list, prnlist, ["ele", "azi", "S6", "S1", "S2", "S5", "S7", "S8"]])
    # return xr_snr


def read_refl_snr1(filename, time=datetime.datetime.today(), interval=15):
    data = np.loadtxt(filename, dtype={"names": ("code", "ele", "azi", "sec", "eler", "S6", "S1", "S2", "S5", "S7", "S8"),
                                       "formats":("U3", "f", "f", "f", "f", "f", "f", "f", "f", "f", "f")})
    codelist = list(set(data["code"]))
    prnlist = [_code2prn(_) for _ in codelist]

    time0 = _sec2time(data["sec"][0], time, _check_if_cur_day(data["sec"][0], 0, len(data["sec"])))
    time1 = _sec2time(data["sec"][-1], time, _check_if_cur_day(data["sec"][-1], len(data["sec"]), len(data["sec"])))
    nepoch = int((time1-time0)/np.timedelta64(interval, "s")) + 1
    time_list = [time0+np.timedelta64(_*interval, "s") for _ in range(nepoch)]
    snr_data = np.zeros((len(time_list), len(prnlist), 8))
    for iline, (code, ele, azi, sec, eler, s6, s1, s2, s5, s7, s8) in enumerate(zip(
        data["code"], data["ele"], data["azi"], data["sec"], data["eler"],
        data["S6"], data["S1"], data["S2"], data["S5"], data["S7"], data["S8"])) :
        prn = _code2prn(code)
        iprn = prnlist.index(prn)
        time_epoch = _sec2time(sec, time, _check_if_cur_day(sec, iline, len(data["sec"])))
        itime = int((time_epoch-time0)/np.timedelta64(interval, "s"))
        snr_data[itime, iprn] = np.array([ele, azi, s6, s1, s2, s5, s7, s8])
    snr_data[snr_data==0]=np.nan
    xr_snr = xr.DataArray(snr_data, dims=["time", "prn", "data"],
                          coords=[time_list, prnlist, ["ele", "azi", "S6", "S1", "S2", "S5", "S7", "S8"]])
    return xr_snr


def read_f107(filename):
    with open(filename, "r") as fread:
        lines = fread.readlines()

        times_list = list()
        values = list()
        for line in lines:
            fields = line.rstrip().split()
            year = int(fields[0])
            doy = int(fields[1])
            hour = int(fields[2])
            f107 = float(fields[3])
            _, mo, day = gnss_time.doy2ymd(year, doy)
            times_list.append(gnss_time.strtime2datetime("%04d %02d %02d %02d 00 00" %(year, mo, day, hour)))
            values.append(f107)
        xr_f107 = xr.DataArray(values, coords=[times_list], dims=["time"])
        return xr_f107


def read_anubis(filename):
    with open(filename, "rb") as fread:
        _ = fread.readline()
        _ = fread.readline()
        line = fread.readline()
        first_epoch = np.datetime64(gnss_time.strtime2datetime(line[8:27].decode("utf-8")), "ns")
        last_epoch = np.datetime64(gnss_time.strtime2datetime(line[28:47].decode("utf-8")), "ns")
        sample = float(line[56:61])
        satsyss = list()
        while True:
            line = fread.readline()
            strline = line.decode("utf-8")
            if "#====== Header information" in strline:
                break
            if strline.startswith("=") and "SUM" in strline:
                satsyss.append(strline[1:4])
        xr_eles = _derive_eles(fread, satsyss, first_epoch, last_epoch, sample)
        xr_azis = _derive_azis(fread, satsyss, first_epoch, last_epoch, sample)
        xr_snrs = _derive_snrs(fread, satsyss, first_epoch, last_epoch, sample)
        return xr_eles, xr_azis, xr_snrs


def _derive_snrs(fread, satsyss, first_epoch, last_epoch, sample):
    header_flag = {
        "start_cond": [(operator.__contains__, "#====== Signal to noise ratio")],
        "stop_cond": [(str.startswith, "\n")],
        "nlines": None
    }
    nepoch = int((last_epoch - first_epoch) / (sample * np.timedelta64(1, "s")))
    time_list = [first_epoch + sample * np.timedelta64(1, "s") * _ for _ in range(nepoch + 1)]
    header_lines = derive_lines(fread, header_flag)
    bands = [_[1:7] for _ in header_lines[2:-1]]
    gnss_snrs_list = list()
    sats = list()
    for band in bands:
        band_block_flag = {
            "start_cond": [(operator.__contains__, "%s %s" % (band, str(first_epoch).replace("T", " ")[:19]))],
            "stop_cond": [(operator.__contains__, "%s %s" % (band, str(last_epoch).replace("T", " ")[:19]))],
            "nlines": None
        }
        lines = derive_lines(fread, band_block_flag)
        snrs_list = list()
        for line in lines:
            myline = line.rstrip()
            fields = myline[28:].replace(" -", "-1").split()
            snrs = [int(tmp) for tmp in fields[1:]]
            snrs_list.append(snrs)
            satellites = ["%02d" % (_+1) for _ in range(len(fields[1:]))]
            sats = satellites
        gnss_snrs_list.append(snrs_list)
    xr_snrs = xr.DataArray(gnss_snrs_list, coords=[bands, time_list, sats], dims=["band", "time", "prn"])
    return xr_snrs

def _derive_azis(fread, satsyss, first_epoch, last_epoch, sample):
    header_flag = {
        "start_cond": [],
        "stop_cond": [(operator.__contains__, "#GNSAZI")],
        "nlines": None
    }
    nepoch = int((last_epoch - first_epoch) / (sample * np.timedelta64(1, "s")))
    time_list = [first_epoch + sample * np.timedelta64(1, "s") * _ for _ in range(nepoch + 1)]
    _ = derive_lines(fread, header_flag)
    gnss_eles_list = list()
    sats = list()
    for satsys in satsyss:
        gps_azis_flag = {
            "start_cond": [(operator.__contains__, "%sAZI %s" % (satsys, str(first_epoch).replace("T", " ")[:19]))],
            "stop_cond": [(operator.__contains__, "%sAZI %s" % (satsys, str(last_epoch).replace("T", " ")[:19]))],
            "nlines": None
        }
        lines = derive_lines(fread, gps_azis_flag)
        eles_list = list()
        for line in lines:
            myline = line.rstrip()
            fields = myline[28:].replace(" -", "-1").split()
            azis = [int(tmp) for tmp in fields[1:]]
            eles_list.append(azis)
            satellites = ["%02d" % (_+1) for _ in range(len(fields[1:]))]
            sats = satellites
        gnss_eles_list.append(eles_list)
    xr_azis = xr.DataArray(gnss_eles_list, coords=[satsyss, time_list, sats], dims=["gnss", "time", "prn"])
    return xr_azis


def _derive_eles(fread, satsyss, first_epoch, last_epoch, sample):
    header_flag = {
        "start_cond": [],
        "stop_cond": [(operator.__contains__, "#GNSELE")],
        "nlines": None
    }
    nepoch = int((last_epoch - first_epoch) / (sample * np.timedelta64(1, "s")))
    time_list = [first_epoch + sample * np.timedelta64(1, "s") * _ for _ in range(nepoch + 1)]
    _ = derive_lines(fread, header_flag)
    gnss_eles_list = list()
    sats = list()
    for satsys in satsyss:
        gps_ele_flag = {
            "start_cond": [(operator.__contains__, "%sELE %s" % (satsys, str(first_epoch).replace("T", " ")[:19]))],
            "stop_cond": [(operator.__contains__, "%sELE %s" % (satsys, str(last_epoch).replace("T", " ")[:19]))],
            "nlines": None
        }
        lines = derive_lines(fread, gps_ele_flag)
        eles_list = list()
        for line in lines:
            myline = line.rstrip()+" "
            fields = myline[28:].replace(" - ", "-1 ").split()
            eles = [int(tmp) for tmp in fields[1:]]
            eles_list.append(eles)
            satellites = ["%02d" % (_+1) for _ in range(len(fields[1:]))]
            sats = satellites
        gnss_eles_list.append(eles_list)
    xr_eles = xr.DataArray(gnss_eles_list, coords=[satsyss, time_list, sats], dims=["gnss", "time", "prn"])
    return xr_eles

def read_ionex_file(filename):
    head_flag = {
        'start_cond': [],
        'stop_cond': [(operator.__contains__, "END OF HEADER")],
        'nlines': None
    }
    with open(filename, 'rb') as fread:
        head_lines = derive_lines(fread, head_flag,
                                  fallback_last_line=False)
        header = _parse_ionex_header(head_lines)
        xr_iono = _parse_ionex_blocks(fread, header)
        return xr_iono


def _parse_map_block(map_lines, header):
    epoch = gnss_time.strtime2datetime(map_lines[1][2:37])
    nrow = int((header["lat1"] - header["lat0"])/header["dlat"]) + 1
    ncol = int((header["lon1"] - header["lon0"])/header["dlon"]) + 1
    data = np.zeros((nrow, ncol), dtype=float) + np.nan
    nitem_eachlat = int(math.floor(ncol/16)) + 1
    values = list()

    for line in map_lines[2:-1]:
        line = line.rstrip()
        if "LAT/LON1/LON2/DLON/H" in line:
            lat = float(line[3:8])
            values = list()
        else:
            values += [float(tmp) for tmp in line.split()]
            if len(values) > 70:
                irow = int(math.floor((lat - header["lat1"])/-header["dlat"]))
                data[irow] = np.array(values)*0.1 # from 0.1 TECU to TECU.
    map = {"data": data,
           "nrow": nrow,
           "ncol": ncol,
           "xllcorner": header["lon0"],
           "yllcorner": header["lat1"],
           "xcellsize": -header["dlat"],
           "ycellsize": header["dlon"]
           }
    return epoch, map


def _parse_ionex_blocks(fread, header):
    map_flag = {
        "start_cond": [(operator.__contains__, "START OF TEC MAP"),
                       ],
        "stop_cond": [(operator.__contains__, "END OF TEC MAP"),
                      ],
        "nlines": None,
    }
    nepoch = (pd.to_datetime(header["stop_epoch"])
              - pd.to_datetime(header["start_epoch"]))/np.timedelta64(
        header["interval"], 's') + 1
    coord_time = list()
    map_list = list()
    coord_lat = np.arange(header["lat1"], header["lat0"]+1, -header["dlat"])
    coord_lon = np.arange(header["lon0"], header["lon1"]+1, header["dlon"])
    while True:
        one_map_lines = derive_lines(fread, map_flag,
                                     fallback_last_line=False)
        if not one_map_lines:
            break
        epoch, epoch_map = _parse_map_block(one_map_lines, header)
        coord_time.append(epoch)
        map_list.append(epoch_map["data"])
    xr_iono = xr.DataArray(map_list, coords=[coord_time, coord_lat, coord_lon],
                         dims=["time", "lat", "lon"])
    return xr_iono


def read_ION_file(filename):
    in_data = False
    max_deg = 15
    degree = 0
    order = 0
    coord_time = list()
    coffnm_list = list()
    coord_degree = range(0, 16)
    coord_order = range(0, 16)
    with open(filename) as fread:
        lines = fread.readlines()
        for line in lines:
            line = line.rstrip()
            if "FROM EPOCH / REFERENCE EPOCH (Y,M,D,H,M,S)" in line:
                epoch = gnss_time.strtime2datetime(line[49:69])
            if "DEGREE  ORDER    VALUE (TECU)   RMS (TECU)" in line:
                in_data = True
                coff_nm = np.zeros((max_deg+1, max_deg+1, 2)) + np.nan
            if degree==15 and order == -15:
                in_data = False
                degree = 0
                order = 0
                coord_time.append(epoch)
                # print(epoch)
                coffnm_list.append(coff_nm)
            if in_data:
                # print(line)
                items = line.split()
                if len(items) != 4:
                    continue
                degree = int(items[0])
                order = int(items[1])
                value = float(items[2])

                if order >= 0:
                    coff_nm[degree][order][0] = value
                else:
                    coff_nm[degree][-order][1] = value
    xr_spheric = xr.DataArray(coffnm_list, coords=[coord_time,
                                                   coord_degree,
                                                   coord_order,
                                                   ["a", "b"]],
                              dims=["time", "degree", "order", "data"])
    return xr_spheric

def read_gga_shaper(filename):
    """Read gga shaper file solution file.
    """
    with open(filename) as fread:
        lines = fread.readlines()
        lines = [line.replace('#PPISOL,', '').replace(',', ' ').rstrip('\n')
                 for line in lines]
        print(lines)
        xyz_list = []
        obj_time_list = []
        for line in lines:
            if line.startswith("%"):
                continue
            if len(line) < 80:
                raise ListTooShortError(
                    "Line length: %d, line too short %s" % (len(line), line))
            str_time = line[:23]
            obj_time = gnss_time.strtime2datetime(str_time)+ datetime.timedelta(seconds=18)
            items = line[24:].split()

            str_lat_dms = items[5]
            str_lon_dms = items[6]
            if float(str_lat_dms) == 0:
                lat = 0
            else:
                lat = str_ddmm2dd(str_lat_dms)

            if float(str_lon_dms) == 0:
                lon = 0
            else:
                lon = str_dddmm2dd(str_lon_dms)
            hgt = float(items[7])
            x, y, z = gnss_geodesy.blh2xyz(lat, lon, hgt)
            print(x, y, z)
            xyz = [x, y, z]
            if obj_time in obj_time_list:
                continue
            xyz_list.append(xyz)
            obj_time_list.append(obj_time)
        coords = {'time': obj_time_list,
                  'data': ['x', 'y', 'z']}
        dims = ['time', 'data']
        ndata = np.array(xyz_list, dtype=np.float64)
        xr_pos = xr.DataArray(ndata, coords=coords, dims=dims)

        return xr_pos


def str_ddmm2dd(str_dms):
    """Convert ddmm.mmmmmmm to dd
    """
    d0 = int(str_dms[:2])
    d1 = float(str_dms[2:])
    return d0 + d1 / 60.


def str_dddmm2dd(str_dms):
    """Convert dddmm.mmmmmmm to dd
    """
    d0 = int(str_dms[:3])
    d1 = float(str_dms[3:])
    return d0 + d1 / 60.


def read_ascii_raster(filename):
    """
    read ASCII Raster.

    sample:
    ```
    ncols         2160
    nrows         720
    xllcorner     -180.00833333377
    yllcorner     -59.991666681504
    cellsize      0.16666666666
    NODATA_value  -9999
    ```

    Therr are 6 keys in meta: "ncols", "nrows", "xllcorner", "yllcorner", "cellsize", "nodata".
    :param filename:
    :return: meta, raster
    """
    with open(filename, 'r') as fread:
        lines = fread.readlines()

    for line in lines[:6]:
        fields = line.rstrip().split()
        if "ncols" in line:
            ncols = int(fields[1])
        elif "nrows" in line:
            nrows = int(fields[1])
        elif "xllcorner" in line:
            xllcorner = float(fields[1])
        elif "yllcorner" in line:
            yllcorner = float(fields[1])
        elif "cellsize" in line:
            cellsize = float(fields[1])
        elif "NODATA_value" in line:
            nodata = float(fields[1])
    meta = {
        "ncols": ncols,
        "nrows": nrows,
        "xllcorner": xllcorner,
        "yllcorner": yllcorner,
        "cellsize": cellsize,
        "nodata": nodata
    }
    raster = np.zeros((nrows, ncols))
    for i, line in enumerate( lines[6:]):
        fields = line.rstrip().split()
        data = [float(tmp) for tmp in fields]
        raster[i] = np.asarray(data, dtype=np.float64)
    raster[raster==nodata] = None
    return meta, raster


def read_GGOS_VMFG(fn,lowB,upperB,leftL,rightL):
    # fs = file(fn,'r')
    with open(fn, "r") as fs:
        vmfg_d = np.loadtxt(fs,dtype={'names':('lat','lon','ah','aw','zhd','zwd'),
                             'formats':('float','float','float','float','float','float')},skiprows=7)
        # fs.close()
        ulB = 90
        llB = -90
        ulL = 0
        llL = 0
        Bcell = 2
        Lcell = 2.5
        rows = np.int(np.floor((upperB - lowB)/Bcell))+1
        cols = np.int(np.floor((rightL - leftL) /Lcell))+1
        matZTD = np.zeros((rows,cols),dtype=np.float64)
        for (lat,lon,zhd,zwd) in zip(vmfg_d['lat'],vmfg_d['lon'],vmfg_d['zhd'],vmfg_d['zwd']):
            ztd = zhd+zwd
            if lat > upperB  or lat < lowB :
                continue
            if lon > rightL or lon < leftL:
                continue
            r = int(np.floor((lat - lowB)/Bcell))
            c = int(np.floor((lon - leftL)/Lcell))
            #print r,c,lat,lon
            matZTD[r,c] = ztd
        #return matZTD,llB,llL,Bcell,Lcell,rows,cols
        return matZTD,lowB,leftL,Bcell,Lcell,rows,cols


def read_GGOS_VMFHgt(fn, lowB, upperB, leftL, rightL):
    # fs = file(fn, 'r')
    with open(fn, "r") as fs:
        maxB, minB, minL, maxL, Bcell, Lcell = np.fromfile(fs, dtype='float', count=6, sep=' ')

        d = np.fromfile(fs, dtype='float', count=-1, sep=' ')
        rows = np.int(np.floor((maxB - minB) / Bcell)) + 1
        cols = np.int(np.floor((maxL - minL) / Lcell)) + 1
        r_s = np.int(np.floor(lowB - minB) / Bcell)
        r_e = np.int(np.floor(upperB - minB) / Bcell)
        c_s = np.int(np.floor(leftL - minL) / Lcell)
        c_e = np.int(np.floor(rightL - minL) / Lcell)
        fs.close()
        res = np.flipud(np.reshape(d, (rows, cols)))
        return res[r_s:r_e + 1, c_s:c_e + 1]


def read_ztd_file(filename):
    """

    Read file like bellow:

    # site, time, zhd, zwd, ztd
    # N6__, 2020-01-06 16:00:00, 1.911, 0.000, 0.072

    :param filename:
    :return:
    """
    content = np.loadtxt(filename,
                         dtype={"names": ("site", "time", "zhd", "zwd", "ztd"),
                                "formats": ("S4", "S20", "f", "f", "f"),
                                },
                         comments="#",
                         delimiter=",")

    obj_time_list = list()

    for items in content:
        obj_time = gnss_time.strtime2datetime(items["time"].decode("ascii"))
        obj_time_list.append(obj_time)

    ndata = np.zeros((len(obj_time_list), 3), dtype=np.float64)
    ndata[:, 0] = content["zhd"]
    ndata[:, 1] = content["zwd"]
    ndata[:, 2] = content["ztd"]
    coords = {'time': obj_time_list,
              'data': ['zhd', 'zwd', 'ztd']}
    dims = ['time', 'data']
    units = {'zhd': 'meter', 'zwd': 'meter', 'ztd': "meter"}
    xr_data = xr.DataArray(ndata, coords=coords,
                           dims=dims)
    xr_data.attrs['units'] = units

    return xr_data


def __yeardoysec2time(strtime):
    """
    convert '1987:302:23:45.67' or '19:091:64884' to datetime
    """
    fields = strtime.split(':')
    if len(fields) != 3:
        raise ValueError("yeardoysec2time() expects a string of 3 fields (: delimited)")
    
    yr = int(fields[0])
    if yr < 80:
        yr += 2000
    doy = int(fields[1])
    sec = int(fields[2])
    _, mo, day = gnss_time.doy2ymd(yr, doy)
    return datetime.datetime(yr, mo, int(day)) + datetime.timedelta(seconds=sec)
    

def skip_comments(fstream, start_char):
    """
    Skip comments in a file stream.
    """
    for line in fstream:
        strline = line.decode()
        if strline.startswith(start_char):
            continue
        else:
            fstream.seek(-len(line), 1)
            break
    
    
def read_sinex(filename):
    """
    Read SINEX file. 
    
    Refernece:
    https://ivscc.gsfc.nasa.gov/IVS_AC/files_IVS-AC/sinex_v210.txt
    https://www.iers.org/SharedDocs/Publikationen/EN/IERS/Documents/ac/sinex/sinex_v2_txt.txt
    https://www.iers.org/SharedDocs/Publikationen/EN/IERS/Documents/ac/sinex/sinex_v201_appendix2_pdf.pdf
    https://www.iers.org/SharedDocs/Publikationen/EN/IERS/Documents/ac/sinex/sinex_v202_pdf.pdf
    """
    
    header_flag = {
            "start_cond": [(operator.__contains__, "%=SNX" )],
            "stop_cond": [],
            "nlines": 1
        }
    
    comment_flag = {
        "start_cond": [(str.startswith, "*")],
        "stop_cond": [(str.startswith, "+")],
        "nlines": None
    }
    
    block_flag = {
        "start_cond": [(str.startswith, "+")],
        "stop_cond": [(str.startswith, "-")],
        "comment": [(str.startswith, "*")],
        "nlines": None
    }
    
    with open(filename, 'rb') as fread:
        header_lines= derive_lines(fread, header_flag)
        header = header_lines[0]
        fmt = header[2:5]
        if fmt != 'SNX':
            raise ValueError('File is not a SINEX file.')
        
        snx_version = header[6:10]
        str_start_time = header[32:44]
        str_end_time = header[45:57]
        
        start_time = __yeardoysec2time(str_start_time)
        end_time = __yeardoysec2time(str_end_time)
        
        snx_data = defaultdict()
        while True:
            block = derive_lines(fread, block_flag=block_flag)

            if not block:
                break
            key, block_data = __parse_snx_block(block)
            if key:
                snx_data[key] = block_data
        return snx_data

        
def __parse_snx_block(block_lines):
    if block_lines[0][0] != '+' or block_lines[-1][0] != '-':
        raise ValueError('SNX block must start with + and end with -')
    
    block_header = block_lines[0]
    if "SITE/ID" in block_header:
        data = [line[1:5] for line in block_lines[1:-1]]
        return "SITE/ID", data
    
    
    if "SOLUTION/EPOCHS" in block_header:
        list_start_time, list_end_time, list_mean_epoch = list(), list(), list()
        for line in block_lines[1:-1]:
            str_start_time = line[16:28]
            str_end_time = line[29:41]
            str_mean_epoch = line[42:54]
            list_start_time.append(__yeardoysec2time(str_start_time))   
            list_end_time.append(__yeardoysec2time(str_end_time))
            list_mean_epoch.append(__yeardoysec2time(str_mean_epoch))
        
        data = pd.DataFrame({"start_time": list_start_time, "end_time": list_end_time, "mean_epoch": list_mean_epoch})
        return "SOLUTION/EPOCHS", data


    if "SOLUTION/APRIORI" in block_header \
        or "SOLUTION/ESTIMATE" in block_header \
        or "SOLUTION/NORMAL_EQUATION_VECTOR" in block_header:
            
        key = block_header.strip()[1:]
        list_type, list_code, list_ref_epoch, list_apriori = list(), list(), list(), list()
        for line in block_lines[1:-1]:
            list_type.append(line[7:11])
            list_code.append(line[15:19])
            str_ref_epoch = line[27:40]
            str_apriori = line[47:68]
            list_ref_epoch.append(__yeardoysec2time(str_ref_epoch))
            list_apriori.append(float(str_apriori.replace("D", "E")))
        data = pd.DataFrame({"type": list_type, "code": list_code, "ref_epoch": list_ref_epoch, "value": list_apriori})    
        return key, data

    # if "SOLUTION/ESTIMATE" in block_header:
    #     list_type, list_code, list_ref_epoch, list_estimate = list(), list(), list(), list()
    #     for line in block_lines[1:-1]:
    #         list_type.append(line[7:13])
    #         list_code.append(line[14:19])
    #         str_ref_epoch = line[27:40]
    #         str_estimate = line[47:68]
    #         list_ref_epoch.append(__yeardoysec2time(str_ref_epoch))
    #         list_estimate.append(float(str_estimate.replace("D", "E")))
    #     data = pd.DataFrame({"type": list_type, "code": list_code, "ref_epoch": list_ref_epoch, "value": list_estimate})    
    #     return "SOLUTION/ESTIMATE", data
    
    
    # if "SOLUTION/MATRIX_ESTIMATE L COVA" in block_header:
    #     # solution_matrix_estimate_block_data["type"] = block_header.strip().split()[-1]
    #     fields = block_lines[-2].strip().split()
    #     nrow = int(fields[0])
    #     ncol = int(fields[1])
    #     data = np.zeros((nrow, ncol))
    #     for line in block_lines[1:-1]:
    #         fields = line.strip().split()
    #         ind1 = int(fields[0]) - 1
    #         ind2 = int(fields[1]) - 1
    #         value = float(fields[2].replace("D", "E"))
    #         data[ind1, ind2] = value
    #         data[ind2, ind1] = value
    #     return "SOLUTION/MATRIX_ESTIMATE L COVA", data

    # if "SOLUTION/DECOMPOSED_NORMAL_MATRIX" in block_header:
    #     fields = block_lines[-2].strip().split()
    #     nrow = int(fields[0])
    #     ncol = int(fields[1])
    #     data = np.zeros((nrow, ncol))
    #     for line in block_lines[1:-1]:
    #         fields = line.strip().split()
    #         ind1 = int(fields[0]) - 1
    #         ind2 = int(fields[1]) - 1
    #         value = float(fields[2].replace("D", "E"))
    #         data[ind1, ind2] = value
    #         data[ind2, ind1] = value
    #     return "SOLUTION/DECOMPOSED_NORMAL_MATRIX", data

    if "SOLUTION/DECOMPOSED_NORMAL_VECTOR" in block_header :
        key = block_header.strip()[1:]
        data = list()
        for line in block_lines[1:-1]:
            fields = line.strip().split()
            data.append(float(fields[1].replace("D", "E")))
        return key, data

    if "FILE/REFERENCE" in block_header:
        description = list()
        for line in block_lines[1:-1]:
            description.append(line.strip())
        return "FILE/REFERENCE", description
    
    if "FILE/COMMENT" in block_header:
        comment = list()
        for line in block_lines[1:-1]:
            comment.append(line.strip())
        return "FILE/COMMENT", comment
    
    if "INPUT/ACKNOWLEDGEMENTS" in block_header:
        ack = list()
        for line in block_lines[1:-1]:
            ack.append(line.strip())
        return "INPUT/ACKNOWLEDGEMENTS", ack
    
    if "SOLUTION/STATISTICS" in block_header:
        stati = dict()
        for line in block_lines[1:-1]:
            strline = line.strip()
            
            if "VARIANCE FACTOR" in strline:
                stati["FACTOR"] = float(strline[32:].replace("D", "E")) # s0_c, VARIANCE FACTOR
            if "WEIGHTED SQUARE SUM OF O-C" in strline or "SQUARED SUM OF RESIDUALS" in strline:
                stati["VTPV"] = float(strline[32:].replace("D", "E")) # v'Pv+v_c' P_c V_c, 
            if "NUMBER OF UNKNOWNS" in strline:
                stati["UNKNOWNS"] = int(strline[23:]) # n_unk
            if "NUMBER OF OBSERVATIONS" in strline:
                stati["OBSERVATIONS"] = int(strline[23:]) # n_obs
            if "DEGREES OF FREEDOM" in strline:
                stati["FREEDOM"] = int(strline[32:])
            if "SAMPLING INTERVAL" in strline:
                stati["INTERVAL"] = float(strline[32:].replace("D", "E"))
            if "PHASE MEASUREMENTS SIGMA" in strline:
                stati["PHASE_SIGMA"] = float(strline[32:].replace("D", "E"))
            if "CODE MEASUREMENTS SIGMA" in strline:
                stati["CODE_SIGMA"] = float(strline[32:].replace("D", "E"))
        return "SOLUTION/STATISTICS", stati
    
    if "SOLUTION/MATRIX_APRIORI L CORR" in block_header \
        or "SOLUTION/MATRIX_APRIORI L INFO" in  block_header \
        or "SOLUTION/MATRIX_APRIORI L COVA" in block_header \
        or "SOLUTION/MATRIX_ESTIMATE L CORR" in block_header \
        or "SOLUTION/NORMAL_EQUATION_MATRIX L" in block_header \
        or "SOLUTION/MATRIX_ESTIMATE L COVA" in block_header \
        or "SOLUTION/DECOMPOSED_NORMAL_MATRIX" in block_header:
        key = block_header.strip()[1:]
        fields = block_lines[-2].strip().split()
        nrow = int(fields[0])
        ncol = int(fields[1])
        
        if nrow > ncol: 
            ncol = nrow 
        else: 
            nrow = ncol
        data = np.zeros((nrow, ncol))
        for line in block_lines[1:-1]:
            fields = line.strip().split()
            irow = int(fields[0]) - 1
            icol = int(fields[1]) - 1
            for ifield, field in enumerate(fields[2:]):
                data[irow, icol+ifield] = float(field.replace("D", "E"))
                data[icol+ifield, irow] = float(field.replace("D", "E"))
        return key, data
            
    return None, None