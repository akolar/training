from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from stravalib.client import Client
import requests

from activities.models import Activity
from strava.models import Strava


class Command(BaseCommand):
    args = ''
    help = 'Fetch new activities from Strava'

    def handle(self, *args, **options):
        users = User.objects.filter(strava__isnull=False)

        for user in users:
            client = Client(user.strava.token)
            activities = client.get_activities(after=user.strava.granted)

            for activity in activities:
                id_ = activity.id

                if id_ not in user.strava.fetched:
                    self.__fetch_activity(client, id_)
                    # user.strava.fetched.append(id_)

            user.strava.save()

    def __fetch_activity(self, client, id_):
        activity = client.get_activity(id_)
        print activity.map.polyline
