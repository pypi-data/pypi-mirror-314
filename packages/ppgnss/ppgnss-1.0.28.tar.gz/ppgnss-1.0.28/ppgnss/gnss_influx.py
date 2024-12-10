# -*- coding: utf-8 -*-
"""
   gnss_influx.py
   ------------------

   Influx module of ppgnss. The module include reading and writting
   data from/to  Influx.

   Tables
   ^^^^^^^^^^^^^^^^^^

   RTS CLOCK
   ****************

   RTS_CLOCK_SSR
   =====   ======  =======
   Field   Type    Description
   =====   ======  =======
   C0      Double
   C1      Double
   C2      Double
   IODE    String  Tag
   Mount   String  Tag
   PRN     String  Tag
   =====   ======  =======

   RTS Orbit
   ******************

   RTS_ORBIT_SSR
   ======  ======  ===========
   Field   Type    Description
   ======  ======  ===========
   Radial  Double
   VEL_R   Double
   Along   Double
   VEL_A   Double
   Out     Double
   VEL_O   Double
   IODE    String   Tag
   MOUNT   String   Tag
   PRN     String   Tag
   ======  ======  ===========

   RTS Station
   *******************

   ======  ======  ============
   Field   Type    Description
   ======  ======  ============
   C1      Double
   P1      Double
   P2      Double
   L1      Double
   L2      Double
   MOUNT    String  TAG
   LAT     Double
   LON     Double
   ======  ======  ============
"""
import numpy as np
from influxdb import InfluxDBClient

from ppgnss import gnss_io

# >>> json_body = [
#     {
#         "measurement": "cpu_load_short",
#         "tags": {
#             "host": "server01",
#             "region": "us-west"
#         },
#         "time": "2009-11-10T23:00:00Z",
#         "fields": {
#             "value": 0.64
#         }
#     }
# ]


def ssr2influx(client, ssr_file, mount="IGS03", measurement="RTS_CLOCK_SSR"):
    """Read SSR file and write to influx database.
    """
    xr_clk_ssr, xr_orb_ssr = gnss_io.read_ssr_file(ssr_file)

    for xr_clk_epoch in xr_clk_ssr:
        timestamp = xr_clk_epoch.coords["time"].values
        jdata = []
        print(timestamp)
        for prn in xr_clk_epoch.coords["prn"].values:
            if np.isnan(xr_clk_epoch.loc[prn, "IODE"].values):
                # print(timestamp, prn, "no iode")
                continue
            json_prn = {
                "time": str(timestamp),
                "measurement": measurement,
                "fields": {
                    "C0": float(xr_clk_epoch.loc[prn, "C0"].values),
                    "C1": float(xr_clk_epoch.loc[prn, "C1"].values),
                    "C2": float(xr_clk_epoch.loc[prn, "C2"].values),
                },
                "tags": {
                    "IODE": int(xr_clk_epoch.loc[prn, "IODE"].values),
                    "MOUNT": mount,
                    "PRN": prn,
                }
            }
            jdata.append(json_prn)
        client.write_points(jdata)
    return True


def insertSSR(client, fields, measurement, mount, timestamp, prn, IODE):
    """
    Insert JSON record to influx.
    """
    json_prn = {
        "time": timestamp,
        "measurement": measurement,
        "fields": fields,
        "tags": {
            "IODE": IODE,
            "MOUNT": mount,
            "PRN": prn,
        }
    }
    jdata = [json_prn]
    client.write_points(jdata)


def querySSR(client, measurement, tags):
    """Qurey record from Influx Client.
    """
    rs = client.query("select * from %s" % measurement)
    return rs.get_points(tags=tags)


def deleteSSR(client, measurement="RTS_CLOCK_SSR", tags=None):
    """Delete measurements from Influx Client
    """
    client.delete_series(measurement=measurement, tags=tags)
