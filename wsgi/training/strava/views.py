import requests
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.conf import settings

from stravalib.client import Client

from strava.models import Strava


def connect(request):
    client = Client()
    callback = HttpRequest.build_absolute_uri(request, reverse('strava:callback'))

    url = client.authorization_url(client_id=STRAVA_ID, scope='view_private', redirect_uri=callback)
    return redirect(url)


def callback(request):
    client = Client()
    token = client.exchange_code_for_token(client_id=settings.STRAVA_ID, client_secret=settings.STRAVA_SECRET,
                                           code=request.GET['code'])

    try:
        strava = request.user.strava
        strava.token = token
        strava.granted = datetime.now()
    except Strava.DoesNotExist:
        strava = Strava(user=request.user, token=token)

    strava.save()

    return redirect(reverse('settings_account'))


def disconnect(request):
    response = requests.post('https://www.strava.com/oauth/deauthorize',
                             data={'access_token': request.user.strava.token})

    if response.status_code != 200:
        response = HttpResponse()
        response.status_code = 500
        return response

    request.user.strava.token = None
    request.user.strava.save()

    return redirect(reverse('settings_account'))
