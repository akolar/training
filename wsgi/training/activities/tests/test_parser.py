import copy
from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from activities.parser import *


class TrackTest(TestCase):
    _created_at = datetime(2014, 9, 21, 06, 44, 06)
    _started_at = copy.deepcopy(_created_at)
    _paused_at = [datetime(2014, 9, 21, 7, 12, 25), datetime(2014, 9, 21, 7, 37, 18), datetime(2014, 9, 21, 8, 57, 43)]

    def setUp(self):
        parser = Parser('/home/anze/Sports/2014/2014-09-21_11-02-33_4_88.fit')
        self.track = parser.convert()

    def test_created_at(self):
        self.assertEquals(self._created_at, self.track.created_at)

    def test_first_start(self):
        self.assertEquals(self.track.laps_at[0], 0)

    def test_start_stop(self):
        for point in enumerate(self.track.time):
            if point[0] == 0:
                continue

            self.assertLessEqual(point[1] - self.track.time[point[0] - 1], timedelta(seconds=15))

    def test_lap(self):
        self.assertEquals(len(self.track.laps_at), 3)

    def test_point(self):
        self.assertEquals(len(self.track), 7995)

    def test_paused(self):
        self.assertEquals(self.track.paused_at, self._paused_at)

    def test_elapsed(self):
        self.assertEquals(self.track.elapsed_time(), 8017)

    def test_moving(self):
        self.assertEquals(self.track.moving_time(), 7990)

    def test_distance(self):
        self.assertAlmostEquals(self.track.total_distance(), 52700, delta=500)

    def test_elevation_gain(self):
        self.assertAlmostEquals(self.track.elevation_gain(), 482, delta=50)

    def test_average_speed(self):
        self.assertAlmostEquals(self.track.average_speed(), 23.5, places=0)

    def test_max_speed(self):
        self.assertAlmostEquals(self.track.max_speed(), 65.6, places=0)

    def test_average_heart_rate(self):
        self.assertAlmostEquals(self.track.average_heart_rate(), 143, delta=3)

    def test_max_heart_rate(self):
        self.assertAlmostEquals(self.track.max_heart_rate(), 171)

    def test_elevation_zones(self):
        data = self.track.elevation_zones()

        for key in data.keys():
            self.assertLessEqual(key, 2500)
            self.assertGreaterEqual(key, 0)

        self.assertEquals(len(data), 160)

    def test_speed_zones(self):
        data = self.track.speed_zones()

        for key in data.keys():
            self.assertLessEqual(key, 125)
            self.assertGreaterEqual(key, 0)

        self.assertEquals(len(data), 64)

    def test_heart_rate_zones(self):
        data = self.track.heart_rate_zones()

        for key in data.keys():
            self.assertLessEqual(key, 210)
            self.assertGreaterEqual(key, 30)

        self.assertEquals(len(data), 84)

    def test_grade_zones(self):
        data = self.track.grade_zones()

        for key in data.keys():
            self.assertLessEqual(key, 45)
            self.assertGreaterEqual(key, -45)

        self.assertEquals(len(data), 32)

    def test_track(self):
        self.assertEquals(len(self.track.track()), 7995)

    def test_time_entries(self):
        self.assertEquals(len(self.track.time_entries()), 7995)

    def test_distance_entries(self):
        self.assertEquals(len(self.track.distance_entries()), 7995)

    def test_heart_rate_entries(self):
        self.assertEquals(len(self.track.heart_rate_entries()), 7995)

    def test_cadence_entries(self):
        self.assertIsNone(self.track.cadence_entries())

    def test_temperature_entries(self):
        self.assertIsNone(self.track.temperature_entries())

class ParserTest(TestCase):

    def test_init(self):
        Parser('/home/anze/Sports/2014/2014-09-21_11-02-33_4_88.fit')

    def test_convert(self):
        parser = Parser('/home/anze/Sports/2014/2014-09-21_11-02-33_4_88.fit')
        parser.convert()


class TrackSerializerTest(TestCase):

    def setUp(self):
        parser = Parser('/home/anze/Sports/2014/2014-09-21_11-02-33_4_88.fit')
        self.track = parser.convert()

        u = User(username='w')
        u.save()
        self.u = u

    def test_wrong_type(self):
        self.assertRaises(TypeError, TrackSerializer.serialize, 1)

    def test_serialize(self):
        activity = TrackSerializer.serialize(self.track, user=self.u)
        self.assertEquals(activity.user, self.u)

    def test_save(self):
        activity = TrackSerializer.serialize(self.track, user=self.u, sport=1)
        activity.save()
