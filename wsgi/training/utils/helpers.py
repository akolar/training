import math


EARTH_RADIUS = 6371000

CONVERT_MS_KMH = 3.6
CONVERT_MS_MPH = 2.23693
CONVERT_KM_MILE = 0.62137
CONVERT_M_FT = 3.28084


def point_distance(p1, p2):
    """Calculates distance between two points.
    Arguments:
        p1, p2: Point in [x, y] format
    """

    dx = math.radians(p2[0] - p1[0])
    dy = math.radians(p2[1] - p1[1])

    x1 = math.radians(p1[0])
    x2 = math.radians(p2[0])

    a = math.sin(dy / 2) ** 2 + math.cos(x1) * math.cos(x2) * math.sin(dx / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(EARTH_RADIUS * c, 1)


def average(values):
    """Averages the values in an iterable.
        values: iterable containing numbers
    """

    return sum(values) / float(len(values))


def average_values(values, devide_by=1, avg_range=10, precision=2):
    """Averages values in specified range.
    Arguments:
        devide_by: devide each value by this numbers
        avg_range: number of previous values to average from
        precision: number of decimal places
    """

    if devide_by != 1:
        values = map(lambda x: float(x) / devide_by, values)

    if avg_range != 1:
        values = map(lambda x: average(values[0:x]) if x < avg_range else average(values[x - avg_range:x]),
                     range(1, len(values) + 1))

    return map(lambda x: round(x, precision), values)
