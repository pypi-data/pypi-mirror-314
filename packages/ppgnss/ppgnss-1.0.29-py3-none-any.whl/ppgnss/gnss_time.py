# -*- coding: utf-8 -*-
"""
   gnss_time
   ------------------

   Time module of ppgnss.
"""
import math
import string
import datetime


def datetime2jd(obj_datetime):
    """
    Convert datetime to Julian Date.

    :param obj_datetime: datetime object for converted.
    :type obj_datetime: datetime.datetime
    :returns: Julian Date.
    :rtype: float

    Example usage::

        >> datetime2jd(the_dt)
        >> 2457823.5

    """

    year = obj_datetime.year
    mon = obj_datetime.month
    day = obj_datetime.day
    hour = obj_datetime.hour
    minute = obj_datetime.minute
    second = obj_datetime.second
    msec = obj_datetime.microsecond
    decdy = day + hour / 24. + minute / (24 * 60.) + second / \
        (24 * 3600.) + msec / (24 * 3600 * 1000000.)
    return ymd2jd(year, mon, decdy)


def total_days(year):
    """
    Return total days in the year.

    :param year: year
    :type year: int
    :returns: totoal days in the year.
    :rtype: int

    Example usage::

        >> total_days(1700)
        >> 365
        >> total_days(2000)
        >> 366
        >> total_days(2006)
        >> 366

    """

    if 'int' not in type(year).__name__:
        raise TypeError("integer argument expected.")
    iyr = int(math.floor(year))
    diy = 365

    # diy = 365 if not iyr % 4 or (iyr % 100 and not iyr % 400) else 366

    if iyr % 4 == 0 and iyr % 100 != 0:
        # 1996 : 366
        # 1700 : 365
        diy = 366

    if iyr % 100 == 0 and iyr % 400 == 0:
        # 2000 : 366
        diy = 366

    return diy


def ymd2jd(year, month, f_day):
    """
    Convert year, month, day to Julian Date.

    More detail please see `gpstk-manual`_  Page:20.

    :param year: year
    :type year: int
    :param month: month
    :type month: int
    :param f_dom: day of month.
    :type f_dom: float
    :returns: Julian Date
    :rtype: float

    Example usage::

        >> ymd2jd(2017, 3, 11)
        >> 2455631.5

    """

    if month <= 2:
        month += 12
        year -= 1
    julian_date = int(math.floor(365.25 * year)) + \
        int(math.floor(30.6001 * (month + 1))) + f_day + 1720981.5
    return julian_date


def jd2mjd(julian_date):
    """
    Convert Julian Date to Modified Julian Date.
    Relatiion between MJD and JD is :math:`MJD = JD - 2400000.5`.


    :param julian_date: Julian Date.
    :type julian_date: float
    :returns: Modified Julian Date
    :rtype: float

    Example usage::

      >> jd2mjd(2455631.5)
      >> 55631.0

    """
    return julian_date - 2400000.5


def jd2ymd(julian_date):
    """
    Convert Julian Date to year, month and day.

    See `gpstk-manual`_ Page 21.

    :param julian_date: Julian Date
    :type julian_date: float
    :returns: (year, month, day)
    :rtype: dict

    Example usage::

        >> jd2ymd(2455631.5)
        >> (2011, 3, 11.0)

    """

    a_julian = int(julian_date + .5)
    b_julian = a_julian + 1537
    c_julian = int((b_julian - 122.1) / 365.25)
    d_julian = int(365.25 * c_julian)
    e_julian = int((b_julian - d_julian) / 30.6001)
    tjd = julian_date + .5
    decdy = b_julian - d_julian - \
        int(30.6001 * e_julian) + tjd - int(tjd)
    month = e_julian - 1 - 12 * int(e_julian / 14)
    year = c_julian - 4715 - int((7 + month) / 10)
    return year, month, decdy


def ymd2doy(year, month, f_dom):
    """
    Convert year, month, day to year, doy.


    :param year: year
    :type year: int
    :param month: month
    :type month: int
    :param f_dom: day of the month
    :type f_dom: float
    :returns: day of the year.
    :rtype: float

    You can use like this::

        >> ymd2doy(2017, 3, 11.)
        >> (2017, 70.0)

    or::

        >> ymd2doy(2017, 3, 11.5)
        >> (2017, 70.5)

    """

    if ('int' not in type(year).__name__) or 'int' not in type(month).__name__:
        raise TypeError("integer argument expected.")

    if type(f_dom).__name__ != 'float':
        try:
            f_dom = float(f_dom)
        except ValueError as exception:
            raise ValueError("Cannot convert f_dom to float: "
                             + str(exception))

    i_dom = int(f_dom)
    frac = f_dom - i_dom
    dtime = datetime.datetime(year=year, month=month, day=i_dom) \
        + datetime.timedelta(days=frac)
    struct_time = dtime.timetuple()
    year = struct_time.tm_year
    idoy = struct_time.tm_yday
    return year, idoy + frac


def strtime2datetime(strtime):
    """
    Convert string like ``"2016  10  0  0  0  0.00000"`` to datetime.

    :param strtime: time string like ``"2016  10  0  0  0  0.00000"``
    :type strtime: string
    :returns: datetime
    :rtype: datetime.datetime

    Use it like::

      >> strtime2datetime("2016  10  0  0  0  0.00000")
      >> datetime.datetime(2016, 10, 0, 0, 0)

    """
    strtime = strtime.replace('-', " ").replace(':', " ").replace("/", " ").replace("T", " ")
    fields = strtime.split()
    if len(fields) != 6:
        raise ValueError("invalid parameters")
    try:
        # year = string.atoi(fields[0])
        # month = string.atoi(fields[1])
        # day = string.atoi(fields[2])
        # hour = string.atoi(fields[3])
        # minute = string.atoi(fields[4])
        # second = string.atof(fields[5])
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])
        hour = int(fields[3])
        minute = int(fields[4])
        second = float(fields[5])
    except ValueError as exception:
        raise ValueError(str(exception))

    if year < 100:
        year = year_two2four(year)
    this_datetime = ymd2datetime(year, month, day, hour, minute, second)
    return this_datetime

# def doy2ymd(year, f_doy):
#     """
#     Convert doy to utc time.

#     :param year: year
#     :type year: int
#     :param f_doy: day of year
#     :type f_doy: float
#     :returns: (year, month, day)
#     :rtype: (int, int, float)
#     """
#     year, month, f_dom = doy2ymdecd(year, f_doy)
#     return year, month, f_dom


def doy2ymd(year, f_doy):
    """
    Convert doy to utc time.

    :param year: year
    :type year: int
    :param f_doy: day of year
    :type f_doy: float
    :returns: (year, month, day)
    :rtype: (int, int, float)

    Example usage::

        >> doy2ymd(2017, 70.)
        >> (2017, 3, 11.0)

    """

    if f_doy <= 0:
        raise ValueError(
            "postive number is expected for the f_doy parameter")

    if 'int' not in type(year).__name__:
        raise TypeError(
            "integer parameter is expected for the year parameter")

    dtime = datetime.datetime(year, 1, 1) + \
        datetime.timedelta(f_doy - 1)
    struct_time = dtime.timetuple()
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    frac = get_frac(f_doy)
    return year, month, day + frac


def doy2gpsw(year, f_doy):
    """
    Convert DOY to GPS Week.

    :param year: year
    :type year: integer
    :param f_doy: day of year
    :type f_doy: float
    :return: (gpsw, f_dow)
    :rtype: (int, float)

    """

    julian_date = doy2jd(year, f_doy)
    gpsw, f_dow = jd2gpsw(julian_date)
    return gpsw, f_dow


def jd2gpsw(julian_date):  # , decimalday=False):
    """
    Convert Julian date to GPS week and GPS Day. More detical can refer to `gpstk-manual`_ P21

    :param julian_date: Julian Date for converted.
    :type julian_date: float
    :return: (gpsw, gpsd), GPS week and day of GPS week.
    :rtype: (int, float)

    Example usage::

        >> jd2gpsw(2455631.5)
        >> (1626, 5.0)

    """

    # f_gpsw = (julian_date - 2444244.5) / 7
    gpsw = int((julian_date - 2444244.5) / 7)
    # sow = (f_gpsw - gpsw) * 604800
    # print jd,jd+.5,int(jd+.5),int(jd+.5)%7
    dow = julian_date - 2444244.5 - gpsw * 7

    # sod = get_frac(dow) * 86400
    return gpsw, dow
    # if decimalday:
    #     return gw, dow
    # else:
    #     return gw, int(math.ceil(dow))


def doy2decyear(year, f_doy):
    """
    Convert doy to decimal year.

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: float
    :returns: decimal year
    :rtype: float

    Example usage::

        >> doy2decyear(2017, 70.)
        >> 2017.1890410958904

    """

    diy = total_days(year)
    return year + (f_doy - 1) * 1.0 / diy


def doy2jd(year, f_doy):
    """
    Convert doy to Julian Date.

    :param year: year.
    :type year: int
    :param doy: day of year.
    :type doy: float
    :return: Julian Date
    :rtype: float

    Example usage::

        >> doy2jd(2017, 70.)
        >> 2457823.5

    """

    year, month, dec_doy = doy2ymd(year, f_doy)
    julian_date = ymd2jd(year, month, dec_doy)
    return julian_date


def toe2datetime(gpsw, toe):
    """Convert TOE to datetime.

    :param gpsw: GPS Week
    :type gpsw: int
    :param toe: Time of Ephermeris
    :type toe: float
    :returns: datetime
    :rtype: datetime.datetime

    Example Usage::

      >> toe2datetime(1939, )
    """
    f_dow = toe / (3600. * 24)
    year, month, f_day = gpsw2ymd(gpsw, f_dow)
    iday = int(f_day)
    idow = int(f_dow)

    sod = toe - idow * 24 * 3600
    hour, minute, second = seconds2hms(sod)

    isecond = int(second)
    mill_sec = int(get_frac(second) * 1000)
    the_datetime = datetime.datetime(year, month, iday, hour, minute,
                                     isecond, microsecond=mill_sec)
    return the_datetime


def gpsw2doy(gpsw, f_dow):
    """
    Convert GPS Week and GPS day to doy.

    :param gpsw: GPS Week
    :type gpsw: integer
    :param f_dow: Day of GPS Week
    :type f_dow: float
    :return: (year, doy)
    :rtype: (int, float)

    Example usage::

      >> gpsw2doy(1930, 1.)
      (2017, 2.)

    """

    julian_date = gpsw2jd(gpsw, f_dow)
    year, f_doy = jd2doy(julian_date)
    return year, f_doy


def jd2doy(judian_date):
    """
    Convert Judian date to doy.

    :param judian_date: Judian Date
    :type judian_date: float
    :return: (year, doy)
    :rtype: (int, float)

    Example usage::

      >> jd2doy(2457755.5)
      (2017, 2.)

    """

    year, month, f_dom = jd2ymd(judian_date)
    year, f_doy = ymd2doy(year, month, f_dom)
    return year, f_doy


def gpsw2ymd(gpsw, f_dow):
    """Convert GPS week and day to year, month, day

    :param gpsw: gps week
    :type gpsw: int
    :param f_dow: day of week
    :type f_dow: float
    :return: year, month, day
    :rtype: (int, int, float)

    Example usage::

      >> gpsw2ymd(1939, 6.)
      (2017, 3, 11.0)

    """
    jd = gpsw2jd(gpsw, f_dow)
    year, month, day = jd2ymd(jd)
    return year, month, day


def gpsw2jd(gpsw, f_dow):
    """
    Convert GPS week and day to Julian Date.

    :param gpsw: gps week
    :type gpsw: int
    :param f_dow: day of week
    :type f_dow: float
    :return: Julian Date
    :rtype: float

    Example usage::

        >> gpsw2jd(1939, 6.)
        >> 2457823.5

    """

    dys = gpsw * 7 + f_dow
    julian_date = dys + 2444244.5
    return julian_date


def year_four2two(year4):
    """
    Convert 4 digital year to 2 digital year. Only number greater than
    1980 but less than 2100 is valid.

    :param year4: 4 digital year like 2017.
    :type year4: int
    :return: year2
    :rtype: int

    Example usage::

    >> year_four2two(2017)
    >> 17

    """

    year2 = year4 - 2000 if year4 >= 2000 else year4 - 1990

    if year4 <= 1980 or year4 > 2100:
        raise ValueError("Wrong 4 digital year")
    return year2


def year_two2four(year2):
    """
    Convert 2 digital year to 4 digital year. If greater than 80,
    return 1900s, otherwise return 2000s. Only number less than 100 is valid.

    :param year2: 2 digital year like 11.
    :type year2: int
    :return: year4
    :rtype: int

    Example usage::

        >> year_two2four(10)
        >> 2010
        >> year_two2four(99)
        >> 1999

    """

    if year2 > 100:
        raise ValueError("not a 2 digital year")

    year4 = 2000 + year2 if year2 < 80 else 1900 + year2

    return year4


def seconds2hms(seconds):
    """Convert seconds in one day to hour, minute and second.

    :param seconds: seconds in one day
    :type seconds: float
    :return: (year, minute, second)
    :rtyep: (int, int, float)

    Example usage::

        >>> gnss_time.seconds2hms(3600)
        (1, 0.)
    """
    if seconds < 0:
        raise ValueError("should not be a negtive value: "
                         + str(seconds))

    hour = int(seconds / 3600.)
    sec_in_hour = seconds - hour * 3600
    minute = int(sec_in_hour / 60.)
    second = seconds - hour * 3600 - minute * 60
    return hour, minute, second


def ymd2datetime(year, month, day,
                 hour=0, minute=0, second=0.0):
    """
    Convert UTC time to python datetime.


    :param year: year
    :type year: int
    :param month: month
    :type month: int
    :param day: day
    :type day: int
    :param hour: hour
    :type hour: int
    :param minute: minute
    :type minute: int
    :param second: second
    :type second: float
    :returns: datetime
    :rtype: datetime.datetime

    Example usage::

        >> ymd2datetime(2017, 3, 11)
        >> datetime.datetime(2017, 3, 11, 0, 0)
    """

    isecond = int(second)
    mill_sec = int(get_frac(second) * 1000)
    the_datetime = datetime.datetime(year, month, day, hour, minute,
                                     isecond, microsecond=mill_sec)
    return the_datetime


def get_frac(f_decimal):
    """
    Get fractional part of decimals.

    :param f_decimal: decimal.
    :type f_decimal: float
    :return: fraction
    :rtype: float

    Use like this::

    >> get_frac(1.1)
    >> 0.10000000000000009

    """
    tfloat = math.fabs(f_decimal)
    return tfloat - int(tfloat)


if __name__ == "__main__":
    pass
