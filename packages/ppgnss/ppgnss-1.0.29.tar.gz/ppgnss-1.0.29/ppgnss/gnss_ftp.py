# -*- coding: utf-8 -*-
"""
   gnss_ftp
   ------------------

   Downloading module of ppgnss. Including downloading rinex nav file,
   rinex obs file, IGS final products of orbits and clocks, and other files.
"""
import ftplib
from os import path

import ppgnss.gnss_time as gt

KEY_URL = "url"
KEY_USER = "login"
KEY_PASSWD = "passwd"
KEY_SP3_DIR = "sp3dir"
KEY_PROD_DIR = "proddir"
KEY_BRDC_DIR = "brdcdir"
KEY_BRDC_COMPRESS_TO = "brdc_compress_to"
KEY_SP3_COMPRESS_TO = "sp3_compress_to"
KEY_PROD_COMPRESS_TO = "prod_compress_to"
KEY_BRDC_STARTS_WITH = "brdc_starts_with"
KEY_PRODS = 'products'
BRDC_STARTS_WITH = "brdc"

YEAR4REPLACE = "YYYY"
YEAR24REPLACE = "YY"
DOY4REPLACE = "DDD"
GPSW4REPLACE = "GPSW"

FTPINFO = {
    'mit':
        {
            KEY_URL: "everest.mit.edu",
            KEY_USER: "anonymous",
            KEY_PASSWD: "",
            KEY_SP3_DIR: "/pub/MIT_SP3",
            KEY_SP3_COMPRESS_TO: ".Z",
            KEY_PROD_DIR: "/pub/MIT_SP3",
            KEY_PROD_COMPRESS_TO: ".Z",
            KEY_PRODS: ["sp3"]
        },
    'sopac':
        {
            KEY_URL: "garner.ucsd.edu",
            KEY_USER: "anonymous",
            KEY_PASSWD: "",
            KEY_SP3_DIR: "/pub/products/GPSW",
            KEY_SP3_COMPRESS_TO: ".Z",
            KEY_PROD_DIR: "/pub/products/GPSW",
            KEY_PROD_COMPRESS_TO: ".Z",
            KEY_BRDC_DIR: "/pub/rinex/YYYY/DDD",   # autodoy0.17n.Z
            KEY_BRDC_COMPRESS_TO: '.Z',
            KEY_BRDC_STARTS_WITH: "auto",
            KEY_PRODS: ["sp3", "clk", "clk_30s"]
        },
    'cddis':
        {
            KEY_URL: 'cddis.gsfc.nasa.gov',
            KEY_USER: 'anonymous',
            KEY_PASSWD: '',
            KEY_SP3_DIR: '/pub/gps/products/GPSW',
            KEY_SP3_COMPRESS_TO: ".Z",
            KEY_PROD_DIR: "/pub/gps/products/GPSW",
            KEY_PROD_COMPRESS_TO: ".Z",
            KEY_BRDC_DIR: '/pub/gps/data/daily/YYYY/DDD/YYn',
            KEY_BRDC_COMPRESS_TO: '.Z',
            KEY_BRDC_STARTS_WITH: "brdc",
            KEY_PRODS: ["sp3", "clk", "clk_30s"]
        },
    'igscb':
        {
            KEY_URL: 'igscb.jpl.nasa.gov',
            KEY_USER: 'anonymous',
            KEY_PASSWD: "",
            KEY_SP3_DIR: '/igscb/product/GPSW',
            KEY_SP3_COMPRESS_TO: ".Z",
            KEY_PROD_DIR: "/igscb/product/GPSW",
            KEY_PROD_COMPRESS_TO: ".Z",
            KEY_PRODS: ["sp3", "clk", "clk_30s"]
        },
    'whu':
        {
            KEY_URL: 'igs.gnsswhu.cn',
            KEY_USER: 'anonymous',
            KEY_PASSWD: '',
            KEY_SP3_DIR: '/pub/gps/products/GPSW',
            KEY_SP3_COMPRESS_TO: ".Z",
            KEY_PROD_DIR: "/pub/gps/products/GPSW",
            KEY_PROD_COMPRESS_TO: ".Z",
            KEY_BRDC_DIR: '/pub/gps/data/daily/YYYY/DDD/YYn/',
            KEY_BRDC_COMPRESS_TO: '.Z',
            KEY_BRDC_STARTS_WITH: "brdc",
            KEY_PRODS: ["sp3", "clk", "clk_30s"]
        }
}


def get_ftpfile(remote_url, remote_path, remote_filename, local_path,
                local_filename, username="anonymous",
                passwd="qgzhliang@gmail.com"):
    """
    Get remote file from ftp.

    :param remote_url: FTP server address like ``"cddis.gsfc.nasa.gov"``
    :type remote_url: string
    :param remote_path: Remote dir like ``"/gps/data/daily/2017/002/17o/"``
    :type remote_path: string
    :param remote_filename: filename of remote file like ``"algo0020.17o.Z"``
    :type remote_filename: string
    :local_path: local directory where save the file like ``"./"``
    :type local_path: string
    :local_filename: local filename like ``"algo0020.17o.Z"``
    :param username: username of ftp like ``"anonymous"``
    :type username: string
    :param passwd: password of ftp like ``"passwd"``
    :type passwd: string
    :return: None

    Example usage::

        >> remote_url = "cddis.gsfc.nasa.gov"
        >> remote_path = "/gps/data/daily/2017/002/17o/"
        >> remote_filename = "algo0020.17o.Z"
        >> local_path = "./"
        >> local_filename = "algo0020.17o.Z"
        >> local_fullname = path.join(local_path, local_filename)
        >> gnss_ftp.get_url(remote_url, remote_path, remote_filename,
                            local_path, local_filename)
    """

    # remote_fullname = path.join(remote_path, remote_filename)
    local_fullname = path.join(local_path, local_filename)
    ftp = ftplib.FTP(remote_url)
    try:
        ftp.login(username, passwd)
        ftp.cwd(remote_path)
        with open(local_fullname, "wb") as fwrite:
            ftp.retrbinary("RETR " + remote_filename,
                           fwrite.write)
    except ftplib.error_reply as exception:
        raise ftplib.error_reply(
            "FTP error reply with " + str(exception))
    except IOError as exception:
        raise IOError(str(exception))
    except ftplib.error_perm as exception:
        raise ftplib.error_perm(str(exception) + ":" + local_filename)
    finally:
        ftp.quit()


def derive_sp3_path_by_doy(year, doy, product="igs", data_center="cddis"):
    """
    Return directory and filename of  IGS SP3 file.

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: int
    :param product: IGS product like ``"igs"``, ``"igu"`` or ``"igr"``
    :type product: string
    :param data_center: Data Center like ``"cddis"``, ``"sopac"``
    :type data_center: string
    :return: (sp3_directory, sp3_filename)
    :rtype: (string, string)

    Example usage::

      >> derive_sp3_path_by_doy(2017, 10, product="igs", data_center="cddis")
      ("/pub/gps/products/1931", "igs19312.sp3.Z")

    """
    gpsw, dow = gt.doy2gpsw(year, doy)
    idow = int(dow)
    sp3_directory, sp3_filename = derive_sp3_path_by_gw(
        gpsw, idow, product=product, data_center=data_center)
    return sp3_directory, sp3_filename


def derive_prod_path_by_doy(year, doy,
                            product="igs", data_center="cddis", ptype="sp3"):
    """
    Return directory and filename of  IGS products file.

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: int
    :param product: IGS product like ``"igs"``, ``"igu"`` or ``"igr"``
    :type product: string
    :param data_center: Data Center like ``"cddis"``, ``"sopac"``
    :type data_center: string
    :param ptype: "sp3", "clk", "clk_30s"
    :type ptype: string
    :return: (prod_directory, prod_filename)
    :rtype: (string, string)

    Example usage::

      >> derive_prod_path_by_doy(2017, 10, product="igs", data_center="cddis")
      ("/pub/gps/products/1931", "igs19312.sp3.Z")

    """
    gpsw, dow = gt.doy2gpsw(year, doy)
    idow = int(dow)
    prod_directory, prod_filename = derive_prod_path_by_gw(
        gpsw, idow, product=product, data_center=data_center, ptype=ptype)
    return prod_directory, prod_filename


def derive_prod_path_by_gw(gps_week, dow,
                           product="igs", data_center="cddis", ptype="sp3"):
    """
    Return directory and filename of products file.

    :param gps_week: GPS Week
    :type gps_week: integer
    :param dow: day of GPS Week
    :type dow: integer
    :param product: product name liek ``"igs"``, ``"igu"`` and ``"igr"``
    :type product: string
    :param data_center: Data Center like ``"cddis"`` and ``"sopac"``.
    :type data_center: string
    :param ptype: string
    :type ptype: "sp3", "clk_30s" or "clk".
    :return: (prod_directory, prod_filename)
    :rtype: (string, string)

    Example usage::

      >>> derive_prod_path_by_gw(1931, 2, product="igs", data_center="cddis")
      ('/pub/gps/products/1931', 'igs19312.sp3.Z')

    """
    if data_center not in FTPINFO.keys():
        raise ValueError("data center error.")
    # if KEY_PROD_DIR not in FTPINFO[data_center].keys():
    #     raise ValueError("no sp3 data in data center")
    if ptype not in FTPINFO[data_center][KEY_PRODS]:
        raise ValueError("no %s data in data center %s" % (ptype, data_center))
    str_gpsw = '%04d' % gps_week
    prod_directory = FTPINFO[data_center][KEY_PROD_DIR].replace(
        GPSW4REPLACE, str_gpsw)
    prod_filename = "%s%s%01d.%s%s" % (
        product, str_gpsw, dow, ptype,
        FTPINFO[data_center][KEY_PROD_COMPRESS_TO])
    return prod_directory, prod_filename


def derive_sp3_path_by_gw(gps_week, dow, product="igs", data_center="cddis"):
    """
    Return directory and filename of IGS SP3 file.

    :param gps_week: GPS Week
    :type gps_week: integer
    :param dow: day of GPS Week
    :type dow: integer
    :param product: product name liek ``"igs"``, ``"igu"`` and ``"igr"``
    :type product: string
    :param data_center: Data Center like ``"cddis"`` and ``"sopac"``.
    :type data_center: string
    :return: (sp3_directory, sp3_filename)
    :rtype: (string, string)

    Example usage::

      >>> derive_sp3_path_by_gw(1931, 2, product="igs", data_center="cddis")
      ('/pub/gps/products/1931', 'igs19312.sp3.Z')

    """
    if data_center not in FTPINFO.keys():
        raise ValueError("data center error.")
    if KEY_SP3_DIR not in FTPINFO[data_center].keys():
        raise ValueError("no sp3 data in data center")
    str_gpsw = '%04d' % gps_week
    sp3_directory = FTPINFO[data_center][KEY_SP3_DIR].replace(
        GPSW4REPLACE, str_gpsw)
    sp3_filename = "%s%s%01d.sp3%s" % (
        product, str_gpsw, dow, FTPINFO[data_center][KEY_SP3_COMPRESS_TO])
    return sp3_directory, sp3_filename


def derive_brdc_path(year, doy, data_center='cddis'):
    """
    Derive BRDC file url according different data center directory structure.

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: int
    :param data_center: name of data center, like ``"cddis"``, ``"mit"``, ``"whu"`` and ``"sopac"``.
    :return: directory of the file, filename of the file
    :rtype: (string, string)

    Example Usage::

      >> year = 2017
      >> doy = 10
      >> data_center = "cddis"
      >> derive_brdc_path(year, doy, data_center=data_center)
      ('/pub/gps/data/daily/2017/010/17n', 'brdc0100.17n.Z')

    """
    # 'brdcdir': '/pub/rinex/YYYY/DDD'
    if data_center not in FTPINFO.keys():
        raise ValueError("data center error.")
    if KEY_BRDC_DIR not in FTPINFO[data_center].keys():
        raise ValueError("no brdc data in the data center")
    brdcdir = FTPINFO[data_center][KEY_BRDC_DIR]
    strdoy = "%03d" % doy
    if year < 100:
        year = gt.year_two2four(year)
    stryear = "%04d" % year

    year2 = gt.year_four2two(year)
    stryear2 = "%02d" % year2
    special_brdc_dir = brdcdir.replace(YEAR4REPLACE, stryear).replace(
        DOY4REPLACE, strdoy).replace(YEAR24REPLACE, stryear2)

    filename = "%s%s0.%02dn" % (
        FTPINFO[data_center][KEY_BRDC_STARTS_WITH], strdoy, year2)
    if FTPINFO[data_center][KEY_BRDC_COMPRESS_TO]:
        filename = filename + FTPINFO[data_center][KEY_BRDC_COMPRESS_TO]

    return special_brdc_dir, filename


def download_brdc(year, doy, local_path="./", local_filename="",
                  data_center="cddis"):
    """
    Download RINEX NAV file from IGS data center. , IGS Center key word should
    be like ``"whu"``, See :func:`ppgnss.gnss_ftp.FTPINFO.keys()`

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: int
    :param local_path: local directory of RINEX NAV file
    :type local_path: string
    :param local_filename: local filename of RINEX NAV file.
    :param data_center: IGS data center
    :type data_center: string
    :return: Successful or not
    :rtype: bool

    Example usage::

      >> year = 2017
      >> doy = 10
      >> data_center = "cddis"
      >> download_brdc(year, doy, data_center=data_center)
      True

    """
    try:
        brdc_path, brdc_filename = derive_brdc_path(
            year, doy, data_center)
        # print brdc_path, brdc_filename
    except ValueError as exception:
        raise ValueError(str(exception))

    if not local_filename:
        local_filename = brdc_filename
    get_ftpfile(FTPINFO[data_center][KEY_URL], brdc_path, brdc_filename,
                local_path, local_filename, FTPINFO[data_center][KEY_USER],
                FTPINFO[data_center][KEY_PASSWD])
    return True


def download_sp3_by_doy(year, doy, local_path="./", local_filename="",
                        product="igs", data_center="cddis"):
    """
    Download SP3 file from IGS data center.

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: int
    :param local_path: local directory of SP3 file
    :type local_path: string
    :param local_filename: local filename of SP3 file.
    :type local_filename: string
    :param product: whick product is requested. ``"igs"``, ``"igu"`` or ``"igr"``.
    :param data_center: IGS data center, like ``"whu"``, See :func:`ppgnss.gnss_ftp.FTPINFO.keys()`
    :type data_center: string
    :return: Successful or not
    :rtype: bool

    Example usage::

      >> year = 2017
      >> doy = 10
      >> data_center = "cddis"
      >> download_sp3_by_doy(year, doy, data_center=data_center)
      True

    """
    try:
        # sp3_directory, sp3_filename = derive_sp3_path_by_doy(
        #     year, doy, product=product, data_center=data_center)
        sp3_directory, sp3_filename = derive_prod_path_by_doy(
            year, doy,
            product=product,
            data_center=data_center,
            ptype="sp3")
    except ValueError as exception:
        raise ValueError(str(exception))
    if not local_filename:
        local_filename = sp3_filename
    get_ftpfile(FTPINFO[data_center][KEY_URL], sp3_directory,
                sp3_filename, local_path=local_path,
                local_filename=local_filename,
                username=FTPINFO[data_center][KEY_USER],
                passwd=FTPINFO[data_center][KEY_PASSWD])
    return True


def download_prod_by_doy(year, doy, local_path="./", local_filename="",
                         product="igs", data_center="cddis", ptype="sp3"):
    """
    Download IGS products from IGS data center.

    :param year: year
    :type year: int
    :param doy: day of year
    :type doy: int
    :param local_path: local directory of SP3 file
    :type local_path: string
    :param local_filename: local filename of SP3 file.
    :type local_filename: string
    :param product: whick product is requested. ``"igs"``, ``"igu"`` or ``"igr"``.
    :param data_center: IGS data center, like ``"whu"``, See :func:`ppgnss.gnss_ftp.FTPINFO.keys()`
    :type data_center: string
    :param ptype: "sp3", "clk_30s", "clk"
    :type ptype: string
    :return: Successful or not
    :rtype: bool

    Example usage::

      >> year = 2017
      >> doy = 10
      >> data_center = "cddis"
      >> download_prod_by_doy(year, doy, data_center=data_center, ptype="sp3")
      True

    """
    try:
        # sp3_directory, sp3_filename = derive_sp3_path_by_doy(
        #     year, doy, product=product, data_center=data_center)
        prod_directory, prod_filename = derive_prod_path_by_doy(
            year, doy,
            product=product,
            data_center=data_center,
            ptype=ptype)
    except ValueError as exception:
        raise ValueError(str(exception))
    if not local_filename:
        local_filename = prod_filename
    get_ftpfile(FTPINFO[data_center][KEY_URL], prod_directory,
                prod_filename, local_path=local_path,
                local_filename=local_filename,
                username=FTPINFO[data_center][KEY_USER],
                passwd=FTPINFO[data_center][KEY_PASSWD])
    return True


def download_sp3_by_gw(gpsw, dow, local_path="./", local_filename="",
                       product="igs", data_center="cddis"):
    """
    Download SP3 file from IGS data center.

    :param gpsw: GPS Week
    :type gpsw: int
    :param dow: day of GPS Week
    :type dow: int
    :param local_path: local directory of SP3 file
    :type local_path: string
    :param local_filename: local filename of SP3 file.
    :type local_filename: string
    :param product: whick product is requested. ``"igs"``, ``"igu"`` or ``"igr"``.
    :param data_center: IGS data center, like ``"whu"``, See :func:`ppgnss.gnss_ftp.FTPINFO.keys()`
    :type data_center: string
    :return: Successful or not
    :rtype: bool

    Example usage::

      >> gpsw = 1931
      >> dow = 2
      >> data_center = "cddis"
      >> download_sp3_by_gw(gpsw, dow, data_center=data_center, ptype=ptype)
      True

    """
    year, doy = gt.gpsw2doy(gpsw, dow)
    download_sp3_by_doy(year, doy, local_path=local_path,
                        local_filename=local_filename, product=product,
                        data_center=data_center)
    return True


def download_prod_by_gw(gpsw, dow, local_path="./", local_filename="",
                        product="igs", data_center="cddis", ptype="sp3"):
    """
    Download IGS products from IGS data center.

    :param gpsw: GPS Week
    :type gpsw: int
    :param dow: day of GPS Week
    :type dow: int
    :param local_path: local directory of SP3 file
    :type local_path: string
    :param local_filename: local filename of SP3 file.
    :type local_filename: string
    :param product: whick product is requested. ``"igs"``, ``"igu"`` or ``"igr"``.
    :param data_center: IGS data center, like ``"whu"``, See :func:`ppgnss.gnss_ftp.FTPINFO.keys()`
    :type data_center: string
    :param ptype: "sp3", "clk_30s", "clk"
    :type ptype: string
    :return: Successful or not
    :rtype: bool

    Example usage::

      >> gpsw = 1931
      >> dow = 2
      >> data_center = "cddis"
      >> download_prod_by_gw(gpsw, dow, data_center=data_center, "sp3")
      True

    """
    year, doy = gt.gpsw2doy(gpsw, dow)
    download_prod_by_doy(year, doy, local_path=local_path,
                         local_filename=local_filename, product=product,
                         data_center=data_center, ptype=ptype)
    return True
