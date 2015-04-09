import math

from django.contrib.gis.geos import LineString

from fitparse import FitFile

from utils.helpers import point_distance
from activities.models import Activity


class Track(object):

    def __init__(self):
        self.__cache = {}

        self.created_at = None

        self.size = 0
        self.distance_total = 0
        self.avg = {}
        self.max_ = {}
        self.laps_at = []
        self.paused_at = []

        self.position = []
        self.time = []  # JSON as delta
        self.distance = []  # JSON as delta
        self.altitude = []  # JSON as delta
        self.heart_rate = []
        self.cadence = []
        self.temperature = []  # JSON as delta

        # grade, velocity are calculated at client-side

    def lap(self):
        if len(self.laps_at) and (self.laps_at[-1] == self.size):
            return

        self.laps_at.append(self.size)

    def save_entry(self, position, time, distance, altitude, heart_rate=None, cadence=None, temperature=None):
        self.size += 1

        self.position.append(self._to_degrees(position))
        self.time.append(time)
        self.distance.append(distance)
        self.altitude.append(altitude)

        self.heart_rate.append(heart_rate)
        self.cadence.append(cadence)
        self.temperature.append(temperature)

    def stop(self, time):
        self.paused_at.append(time)

    def elapsed_time(self):
        if 'elapsed' not in self.__cache:
            self.__cache['elapsed'] = (self.time[-1] - self.time[0]).seconds

        return self.__cache['elapsed']

    def moving_time(self):
        if 'moving' not in self.__cache:
            time = 0
            for i in range(1, len(self.position)):
                if point_distance(self.position[i], self.position[i - 1]) > 0.5:
                    time += 1

            self.__cache['elapsed'] = time

        return self.__cache['elapsed']

    def total_distance(self):
        if 'distance' not in self.__cache:
            self.__cache['distance'] = self.distance[-1]

        return self.__cache['distance']

    def elevation_gain(self):
        if 'elevation_gain' not in self.__cache:
            total_gain = 0
            for i in range(1, len(self.altitude)):
                gain = self.altitude[i] - self.altitude[i - 1]
                total_gain += gain if gain > 0 else 0

            self.__cache['elevation_gain'] = total_gain

        return self.__cache['elevation_gain']

    def average_speed(self):
        if 'average_speed' not in self.__cache:
            self.__cache['average_speed'] = round(self.total_distance() / float(self.moving_time()) * 3.6, 2) * 100

        return self.__cache['average_speed']

    def max_speed(self):
        if 'max_speed' not in self.__cache:
            distances = map(lambda x: x[0] - x[1], zip(self.distance, [0] + self.distance))
            times = map(lambda x: (x[0] - x[1]).seconds, zip(self.time, [self.time[0]] + self.time))
            assert len(distances) == len(times)

            speeds = map(lambda x: x[0] / x[1] if x[1] != 0 else 0, zip(distances, times))
            speeds = filter(lambda x: x < 35, speeds)
            self.__cache['max_speed'] = round(max(speeds) * 3.6, 2) * 100

        return self.__cache['max_speed']

    def average_heart_rate(self):
        if 'average_hr' not in self.__cache:
            valid_hr = [hr for hr in self.heart_rate if hr is not None]
            self.__cache['average_hr'] = int(round(sum(valid_hr) / float(len(valid_hr)), 0)) if len(valid_hr) else 0

        return self.__cache['average_hr']

    def max_heart_rate(self):
        if 'max_hr' not in self.__cache:
            self.__cache['max_hr'] = max(self.heart_rate)

        return self.__cache['max_hr']

    def elevation_zones(self):
        data = {}
        for altitude in self.altitude:
            idx = int(round(altitude, 0))
            try:
                data[idx] += 1
            except KeyError:
                data[idx] = 1

        return data

    def speed_zones(self):
        distances = map(lambda x: x[0] - x[1], zip(self.distance, [0] + self.distance))
        times = map(lambda x: (x[0] - x[1]).seconds, zip(self.time, [self.time[0]] + self.time))
        assert len(distances) == len(times)

        speeds = map(lambda x: x[0] / x[1] * 3.6 if x[1] != 0 else 0, zip(distances, times))

        data = {}
        for speed in speeds:
            idx = int(round(speed, 0))
            try:
                data[idx] += 1
            except KeyError:
                data[idx] = 1

        return data

    def heart_rate_zones(self):
        valid_hr = [hr for hr in self.heart_rate if hr is not None]

        data = {}
        for hr in valid_hr:
            try:
                data[hr] += 1
            except KeyError:
                data[hr] = 1

        return data

    def grade_zones(self):
        distances = map(lambda x: x[0] - x[1], zip(self.distance, [0] + self.distance))
        elevation_gains = map(lambda x: x[0] - x[1], zip(self.altitude, [self.altitude[-1]] + self.altitude))
        assert len(distances) == len(elevation_gains)

        data = {}
        for change in zip(elevation_gains, distances):
            if change[1] < 0.5 or change[1] < abs(change[0]):  # not moving or huge elevation difference
                continue

            grade = int(round(math.degrees(math.atan2(*change)), 0))
            try:
                data[grade] += 1
            except KeyError:
                data[grade] = 1

        return data

    def track(self):
        assert len(self.altitude) == len(self.position) and len(self.time) == len(self.position)

        return [self.position[i] + [int(round(self.altitude[i], 0))] for i in range(len(self.position))]

    def distance_entries(self):
        return (list(map(lambda x: (x[0] - x[1]) * 100, zip(self.distance, [0] + self.distance))) if
                (len([e for e in self.distance if e]) * 10 > len(self.distance)) else None)

    def heart_rate_entries(self):
        return self.heart_rate if (len([e for e in self.heart_rate if e]) * 10 > len(self.heart_rate)) else None

    def cadence_entries(self):
        return self.cadence if (len([e for e in self.cadence if e]) * 10 > len(self.cadence)) else None

    def temperature_entries(self):
        return self.temperature if (len([e for e in self.temperature if e]) * 10 > len(self.temperature)) else None

    def time_entries(self):
        return map(lambda x: (x[0] - x[1]).seconds, zip(self.time, [self.time[0]] + self.time))

    def _to_degrees(self, position):
        return [round(s * (180 / float(2 ** 31)), 9) for s in position]

    def __len__(self):
        return self.size


class Parser(object):
    track = None

    def __init__(self, path):
        self.fitfile = FitFile(path)

    def convert(self):
        if self.track:
            return self.track

        self.track = Track()
        map(self._parse_entry, self.fitfile.get_messages())

        return self.track

    def _parse_entry(self, point_data):
        if point_data.get_value('time_created'):
            self.track.created_at = point_data.get_value('time_created')
        elif len(self.track) == 0 and point_data.get_value('event_type') == 'start':
            self.track.lap()
        elif point_data.get_value('event') == 'lap':
            self.track.lap()
        elif point_data.get_value('event_type') == 'stop_all':
            self.track.stop(point_data.get_value('timestamp'))
        elif point_data.get_value('event_type') == 'start':
            # Track resumes when a normal point is recived.
            pass
        elif point_data.get_value('position_lat'):  # regular point
            self.track.save_entry([point_data.get_value('position_lat'), point_data.get_value('position_long')],
                                  point_data.get_value('timestamp'), point_data.get_value('distance'),
                                  point_data.get_value('altitude'), point_data.get_value('heart_rate'),
                                  point_data.get_value('cadence'), point_data.get_value('temperature'))


class TrackSerializer(object):
    @classmethod
    def serialize(self, o, **kwargs):
        if not isinstance(o, Track):
            raise TypeError('Object should be of type {}, is {}'.format(type(Track), type(o)))

        a = Activity()
        a.date = o.created_at

        a.elapsed = o.elapsed_time()
        a.moving = o.moving_time()
        a.total_distance = o.total_distance()
        a.elevation_gain = o.elevation_gain()

        a.speed_avg = o.average_speed()
        a.speed_max = o.max_speed()
        a.hr_avg = o.average_heart_rate()
        a.hr_max = o.max_heart_rate()

        a.zones_elevation = o.elevation_zones()
        a.zones_speed = o.speed_zones()
        a.zones_hr = o.heart_rate_zones()
        a.zones_grade = o.grade_zones()

        a.track = LineString(o.track())
        a.time = o.time_entries()
        a.distance = o.distance_entries()

        hr = o.heart_rate_entries()
        a.heart_rate = [e if e else -1 for e in hr] if hr else None

        cad = o.cadence_entries()
        a.cadence = [e if e else -1 for e in cad] if cad else None

        temp = o.temperature_entries()
        a.temperature = [e if e else -1 for e in temp] if temp else None

        # User, activity type, objectives, etc.
        for key, value in kwargs.iteritems():
            if key not in ['user', 'sport', 'description', 'comments', 'equipment', 'primary_objective',
                           'secondary_objective', 'rating']:
                continue

            setattr(a, key, value)

        return a
