import json
from datetime import time

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import formats

from djorm_pgarray.fields import IntegerArrayField, SmallIntegerArrayField
from jsonfield import JSONField

from activities import ureg, Q_


class Activity(models.Model):
    CORE_SPORTS = (
        (-1, _('Not set')),
        (0, _('Ride')),
        (1, _('Run')),
        (2, _('Swim')),
        (3, _('Hike')),
        (4, _('Walk'))
    )

    SPORTS = (
        (10, _('Alpine Ski')),
        (11, _('Backcountry Ski')),
        (12, _('Canoeing')),
        (13, _('Cross-country Skiing')),
        (14, _('Crossfit')),
        (15, _('Elliptical')),
        (16, _('Ice Skate')),
        (17, _('Inline Skate')),
        (18, _('Kayaking')),
        (19, _('Kitesurf')),
        (20, _('Nordic Ski')),
        (21, _('Rock Climbing')),
        (22, _('Roller Ski')),
        (23, _('Rowing')),
        (24, _('Snowboard')),
        (25, _('Snowshoe')),
        (26, _('Stair-Stepper')),
        (27, _('Stand Up Padding')),
        (28, _('Surfing')),
        (29, _('Weight Training')),
        (30, _('Workout')),
        (31, _('Yoga'))
    )

    TRAINING_TYPES = (
        (0, _('Not specified')),
        (1, _('Endurance')),
        (2, _('Muscular endurance')),
        (3, _('Anaerobic endurance')),
        (4, _('Technique')),
        (5, _('Power')),
        (6, _('Strength')),
        (7, _('Recovery'))
    )

    # Basic data
    user = models.ForeignKey(User)
    date = models.DateTimeField(_('timestamp'))
    sport = models.SmallIntegerField(_('sport'), choices=CORE_SPORTS + SPORTS, default=-1)
    description = models.CharField(_('Title'), max_length=100, blank=True)
    comments = models.TextField(_('comments'), blank=True)

    # Objectives
    primary_objective = models.PositiveSmallIntegerField(_('primary objective'), choices=TRAINING_TYPES,
                                                         null=True, blank=True)
    rating = models.PositiveSmallIntegerField(_('RPE'), null=True, default=6)

    # Summary
    elapsed = models.PositiveIntegerField(_('elapsed time'), null=True, default=None)
    moving = models.PositiveIntegerField(_('moving time'), null=True, default=None)
    total_distance = models.PositiveIntegerField(_('distance'), null=True, default=None)
    elevation_gain = models.PositiveIntegerField(_('elevation gain'), null=True, default=None)
    equipment = models.ForeignKey('Equipment', verbose_name=_('equipment'), null=True, blank=True, default=None)

    # Avg and max
    speed_avg = models.PositiveSmallIntegerField(_('average speed'), null=True, default=None)
    speed_max = models.PositiveSmallIntegerField(_('maximum speed'), null=True, default=None)
    hr_avg = models.PositiveSmallIntegerField(_('average heart rate'), null=True, default=None)
    hr_max = models.PositiveSmallIntegerField(_('maximum heart rate'), null=True, default=None)
    temperature_max = models.SmallIntegerField(_('maximum temperature'), null=True, default=None)
    temperature_avg = models.SmallIntegerField(_('average temperature'), null=True, default=None)

    # Zone data
    zones_elevation = JSONField(null=True, blank=True)
    zones_speed = JSONField(null=True, blank=True)
    zones_hr = JSONField(null=True, blank=True)
    zones_grade = JSONField(null=True, blank=True)
    zones_cadence = JSONField(null=True, blank=True)
    zones_temperature = JSONField(null=True, blank=True)

    # Full track
    track = models.LineStringField(dim=3, null=True, blank=True)
    time = SmallIntegerArrayField(null=True, blank=True)  # as delta
    distance = IntegerArrayField(null=True, blank=True)  # as delta, in cm
    heart_rate = SmallIntegerArrayField(null=True, blank=True)
    cadence = SmallIntegerArrayField(null=True, blank=True)
    temperature = SmallIntegerArrayField(null=True, blank=True)

    objects = models.GeoManager()

    def get_distance(self):
        if self.total_distance:
            return self.total_distance / 1000.0 * ureg.km
        else:
            return None

    def get_moving_time(self):
        if self.moving:
            time = self.moving
        else:
            time = self.elapsed

        return self.__seconds_to_time(time)

    def get_elevation_gain(self):
        return self.elevation_gain * ureg.meter

    def get_pace_speed_avg(self):
        if self.has_pace():
            min_km = 60 / (self.speed_avg / 100.0)
            seconds = int(min_km % 1 * 60)
            minutes = int(min_km % 60)
            hours = int(min_km // 60)
            return time(hours, minutes, seconds)
        else:
            return self.speed_avg / 100.0 * (ureg.km / ureg.hour)

    def has_pace(self):
        return self.sport in (1, 3, 4)

    def get_elapsed_time(self):
        return self.__seconds_to_time(self.elapsed)

    def get_rest(self):
        if not self.moving:
            return self.__seconds_to_time(0)

        return self.__seconds_to_time(self.elapsed - self.moving)

    def get_max_pace_speed(self):
        if not self.speed_max:
            return None

        if self.has_pace():
            min_km = 60 / (self.speed_max / 100.0)
            seconds = int(min_km % 1 * 60)
            minutes = int(min_km % 60)
            hours = int(min_km // 60)
            return time(hours, minutes, seconds)
        else:
            return self.speed_max / 100.0 * (ureg.km / ureg.hour)

    def get_avg_hr(self):
        return self.hr_avg

    def get_max_hr(self):
        return self.hr_max

    def get_times(self):
        return self.__calc_deltas(self.time)

    def get_distances(self):
        return (self.__calc_deltas(self.distance, lambda x: round(x / 100.0)), ureg.meter)

    def get_elevations(self):
        return (self.track.z, ureg.meter)

    def get_speeds(self):
        speeds = []
        for distance, time in zip(self.distance, self.time):
            if time == 0:
                speeds.append(0)
                continue

            speeds.append(distance / 100.0 / time)

        return (speeds, ureg.meter / ureg.second)

    def get_temperatre_avg(self):
        return self.temperature_avg * ureg.celsius

    def get_hr_avg(self):
        return self.hr_avg

    def get_hr_max(self):
        return self.hr_max

    def get_grades(self):
        distances = map(lambda x: round(x / 100.0), self.distance)
        elevation_gains = [0] + list(map(lambda x1, x2: x2 - x1, self.track.z[:-1], self.track.z[1:]))

        grades = map(lambda d, e: round(e / d * 100, 1) if d > 0 else 0, distances, elevation_gains)
        return grades

    def __calc_deltas(self, list_, l):
        entries = [list_[0]]
        for entry in list_:
            entries.append(entries[-1] + l(entry))

        return entries

    def dist(self):
        return list(map(lambda x: x / float(100), self.distance))

    def zones(self):
        return {
            'elevation': self.zones_elevation,
            'speed': self.zones_speed,
            'hr': self.zones_hr,
            'grade': self.zones_grade
        }

    def set_zones(self, **kwargs):
        _valid = ('elevation', 'speed', 'hr', 'grade')
        for key, value in kwargs:
            if key not in _valid:
                continue

            self.__setattr__(key, json.dumps(value))

    def __seconds_to_time(self, value):
        seconds = value % 60
        minutes = value // 60 % 60
        hours = value // 3600
        return time(hours, minutes, seconds)

    def __unicode__(self):
        return self.description if self.description else formats.date_format(self.date, 'SHORT_DATETIME_FORMAT')


class Equipment(models.Model):
    SPORTS = (
        (-1, 'Other'),
        (0, 'Bike'),
        (1, 'Shoes')
    )

    user = models.ForeignKey(User, default=None)

    name = models.CharField(_('name'), max_length=50, default='')
    sport = models.SmallIntegerField(_('sport'), choices=SPORTS, default=-1)
    comment = models.CharField(_('comment'), max_length=100, default='', blank=True, null=True)


    def __unicode__(self):
        return self.name
