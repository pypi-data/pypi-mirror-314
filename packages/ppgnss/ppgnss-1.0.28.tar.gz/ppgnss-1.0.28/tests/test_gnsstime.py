# -*- coding: utf-8 -*-
"""
   unit test of gnss time module.
"""
import unittest
import datetime
from ppgnss import gnss_time


class TestTime(unittest.TestCase):
    '''
    Unit test of ppgnss.gnss_time
    '''

    test_data = {
        'year': 2017,
        'month': 3,
        'day': 11,
        'hour': 0,
        'minute': 0,
        'second': 0.,
        'jd': 2457823.5,
        'mjd': 57823.0,
        'strtime': '2017 03 11 00 00 00.00000',
        'doy': 70,
        'gpsw': 1939,
        'dow': 6,
        'dec_year': 2017.189041096,
    }

    def test_ymd2doy(self):
        '''
        Test function :func:`gnss_time.ymd2doy()`

        '''

        year, doy = gnss_time.ymd2doy(self.test_data['year'],
                                      self.test_data['month'],
                                      self.test_data['day'])
        self.assertEqual(year, 2017)
        self.assertEqual(doy, 70)

        year, doy = gnss_time.ymd2doy(self.test_data['year'],
                                      self.test_data['month'],
                                      self.test_data['day'] * 1.)
        self.assertEqual(year, 2017)
        self.assertEqual(doy, 70.)

        try:
            year, doy = gnss_time.ymd2doy(self.test_data['year'],
                                          self.test_data['month'],
                                          "hello")
        except ValueError as exception:
            self.assertIn("Cannot convert f_dom to float",
                          str(exception))

    def test_datetime2jd(self):
        '''
        Test function :func:`gnss_time.datetime2jd()`
        '''
        obj_datetime = datetime.datetime(self.test_data['year'],
                                         self.test_data['month'],
                                         self.test_data['day'])
        self.assertEqual(type(obj_datetime).__name__, 'datetime')
        julian_day = gnss_time.datetime2jd(obj_datetime)
        self.assertEqual(julian_day, self.test_data['jd'])

    def test_totaldays(self):
        '''
        Test function :func:`gnss_time.total_days()`
        '''
        year = 2000
        total_days1 = gnss_time.total_days(year)
        self.assertEqual(total_days1, 366)

        year = 1700
        total_days1 = gnss_time.total_days(year)
        self.assertEqual(total_days1, 365)

        year = 1996
        total_days1 = gnss_time.total_days(year)
        self.assertEqual(total_days1, 366)

        year = 1999
        total_days1 = gnss_time.total_days(year)
        self.assertEqual(total_days1, 365)

    def test_ymd2jd(self):
        '''
        Test function :func:`gnss_time.ymd2jd()`
        '''

        julian_day = gnss_time.ymd2jd(self.test_data['year'],
                                      self.test_data['month'],
                                      self.test_data['day'])
        self.assertEqual(julian_day, self.test_data['jd'])
        julian_day1 = gnss_time.ymd2jd(2000, 1, 1)
        self.assertEqual(julian_day1, 2451544.5)

    def test_jd2mjd(self):
        '''
        Test function :func:`gnss_time.jd2mjd()`
        '''
        mjd = gnss_time.jd2mjd(self.test_data['jd'])
        self.assertEqual(mjd, self.test_data['mjd'])

    def test_utc2datetime(self):
        '''
        Test function :func:`gnss_time.utc2datetime()`
        '''

        the_datetime = gnss_time.ymd2datetime(self.test_data['year'],
                                              self.test_data['month'],
                                              self.test_data['day'],
                                              self.test_data['hour'],
                                              self.test_data['minute'],
                                              self.test_data['second'])
        self.assertEqual(the_datetime.year, self.test_data['year'])
        self.assertEqual(the_datetime.month, self.test_data['month'])
        self.assertEqual(the_datetime.day, self.test_data['day'])
        self.assertEqual(the_datetime.hour, self.test_data['hour'])
        self.assertEqual(the_datetime.minute, self.test_data['minute'])
        self.assertEqual(the_datetime.second, self.test_data['second'])

    def test_get_frac(self):
        '''
        Test function :func:`gnss_time.get_frac()`
        '''
        decimal_digtal = 1.1
        frac = gnss_time.get_frac(decimal_digtal)
        self.assertAlmostEqual(frac, .1, places=9)

    def test_strtime2datetime(self):
        '''
        Test function :func:`gnss_time.strtime2datetime()`

        '''
        the_datetime = gnss_time.strtime2datetime(
            self.test_data['strtime'])
        self.assertEqual(the_datetime.year, self.test_data['year'])
        self.assertEqual(the_datetime.month, self.test_data['month'])
        self.assertEqual(the_datetime.day, self.test_data['day'])
        self.assertEqual(the_datetime.hour, self.test_data['hour'])
        self.assertEqual(the_datetime.minute, self.test_data['minute'])
        self.assertEqual(the_datetime.second, self.test_data['second'])
        try:
            the_datetime = gnss_time.strtime2datetime(
                "2017 03 11 0 0.0")
        except ValueError as exception:
            self.assertEqual(str(exception), "invalid parameters")

    def test_doy2ymd(self):
        '''
        Test function :func:`gnss_time.doy2ymd()`
        '''
        year, month, day = gnss_time.doy2ymd(
            self.test_data['year'], self.test_data['doy'])
        self.assertEqual(year, self.test_data['year'])
        self.assertEqual(month, self.test_data['month'])
        self.assertEqual(day, self.test_data['day'])
        try:
            gnss_time.doy2ymd(2017, 0.)
        except ValueError as exception:
            self.assertTrue(
                "postive number is expected" in str(exception))

        try:
            gnss_time.doy2ymd(2017., 1)
        except TypeError as exception:
            self.assertTrue(
                "integer parameter is expecte" in str(exception))

    def test_jd2gps2(self):
        '''
        Test function :func:`gnss_time.jd2gps2()`
        '''
        gpsw, dow = gnss_time.jd2gpsw(self.test_data['jd'])
        self.assertEqual(gpsw, self.test_data['gpsw'])
        self.assertEqual(dow, self.test_data['dow'])

    def test_doy2decyear(self):
        """
        Test function :func:`gnss_time.doy2decyear()`
        """
        dec_year = gnss_time.doy2decyear(self.test_data['year'],
                                         self.test_data['doy'])
        self.assertAlmostEqual(
            dec_year, self.test_data['dec_year'], places=9)

    def test_doy2jd(self):
        '''
        Test function :func:`gnss_time.doy2jd()`.
        '''
        julian_date = gnss_time.doy2jd(
            self.test_data['year'], self.test_data['doy'])
        self.assertAlmostEqual(
            julian_date, self.test_data['jd'], places=9)

    def test_gpsw2jd(self):
        '''
        Test function :func:`gnss_time.gps2jd()`.
        '''
        julian_date = gnss_time.gpsw2jd(
            self.test_data['gpsw'], self.test_data['dow'])
        self.assertAlmostEqual(
            julian_date, self.test_data['jd'], places=9)

    def test_yeartwo2four(self):
        """
        Test function :func:`gnss_time.year_two2four`.
        """
        year2 = 11
        year4 = gnss_time.year_two2four(year2)
        self.assertEqual(year4, 2011)
        year2 = 99
        year4 = gnss_time.year_two2four(year2)
        self.assertEqual(year4, 1999)

    def test_yearfour2two(self):
        '''
        Test function :func:`gnss_time.year_four2two()`.
        '''
        year4 = 2017
        year2 = gnss_time.year_four2two(year4)
        self.assertEqual(year2, 17)
        try:
            gnss_time.year_four2two(1980)
        except ValueError as exception:
            self.assertIn("Wrong 4 digital year", str(exception))

    def test_doy2gps2(self):
        '''
        Test function :func:`gnss_time.doy2gps2()`.
        '''

        year = 2017
        f_doy = 2.
        gpsw, dow = gnss_time.doy2gpsw(year, f_doy)
        self.assertEqual(gpsw, 1930)
        self.assertEqual(dow, 1)

    def test_jd2doy(self):
        '''
        Test function :func:`gnss_time.jd2doy()`.
        '''
        jd = 2457755.5
        year, doy = gnss_time.jd2doy(jd)
        self.assertEqual(year, 2017)
        self.assertEqual(doy, 2)

    def test_gpsw2doy(self):
        '''
        Test function :func:`gnss_time.gpsw2doy()`.
        '''
        gpsw = 1930
        dow = 1.
        year, doy = gnss_time.gpsw2doy(gpsw, dow)
        self.assertEqual(year, 2017)
        self.assertEqual(doy, 2.)

    def test_seconds2hms(self):
        """
        Test function :func:`gnss_time.sec2hms`.
        """
        t1 = {
            'seconds': 3600.,
            'hour': 1,
            'minute': 0,
            'second': 0.,
        }

        hour, minute, second = gnss_time.seconds2hms(t1['seconds'])
        self.assertEqual(hour, t1['hour'])
        self.assertEqual(minute, t1['minute'])
        self.assertEqual(second, t1['second'])

    def test_gpsw2ymd(self):
        """Test function :func:`gnss_time.gpsw2ymd`
        """
        year, month, day = gnss_time.gpsw2ymd(self.test_data['gpsw'],
                                              self.test_data['dow'])
        self.assertEqual(year, self.test_data['year'])
        self.assertEqual(month, self.test_data['month'])
        self.assertEqual(day, self.test_data['day'])

    def test_toe2datetime(self):
        """Test function :func:`gnss_time.toe2datetime`
        """
        toe = 3600 * 24 * 3 + 3600 * 3 + 57
        obj_datetime = gnss_time.toe2datetime(self.test_data['gpsw'], toe)
        self.assertEqual(obj_datetime.year, self.test_data['year'])
        self.assertEqual(obj_datetime.month, self.test_data['month'])
        self.assertEqual(obj_datetime.day, 8)
        self.assertEqual(obj_datetime.hour, 3)
        self.assertEqual(obj_datetime.minute, 0)
        self.assertEqual(obj_datetime.second, 57)
