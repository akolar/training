from django.test import TestCase

from utils.helpers import *  # noqa


class HelperTest(TestCase):
    def test_distance(self):
        p1 = [0, 0]
        p2 = [1, 1]

        self.assertAlmostEquals(point_distance(p1, p2), 157200, delta=50)
