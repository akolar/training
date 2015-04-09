import os
import calendar
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.timezone import now
from django.db.models import Sum, Count, Max, Avg

from activities.forms import UploadForm, EditForm, ManualUploadForm
from activities.models import Activity


ORDER_KEYS = {
    'date': '-date',
    'title': 'description',
    'sport': 'sport',
    'distance': 'total_distance',
    'elevation': 'elevation_gain',
    'time': 'moving',
    'speed': 'speed_avg',
    'hr': 'hr_avg',
    'temperature': 'temperature_avg',
    'rpe': 'rating'
}


def handle_uploads(files):
    """Uploads the file to server and returns path of uploaded file."""

    saved = {}

    upload_full_path = os.path.join(settings.MEDIA_ROOT, 'fit_files')

    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    for key, upload in files.iteritems():
        while os.path.exists(os.path.join(upload_full_path, upload.name)):
            upload.name = '_' + upload.name
        with open(os.path.join(upload_full_path, upload.name), 'wb') as dest:
            for chunk in upload.chunks():
                dest.write(chunk)
        saved[key] = os.path.join(upload_full_path, upload.name)

    return saved


@csrf_protect
@login_required
@require_http_methods(['GET', 'POST'])
def upload(request):
    """Renders the upload form and handles the upload of files."""

    template = {}

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            fit = handle_uploads(request.FILES)['fit_file']
            id_ = form.save(request.user, fit)

            if id_:
                return redirect('activities:view', id_=id_)
            else:
                return redirect('activities:view-all-status', status='failed')

        template['form'] = form
    else:
        template['form'] = UploadForm()

    return render(request, 'activities/upload.html', template)


@csrf_protect
@login_required
@require_http_methods(['GET', 'POST'])
def manual_entry(request):
    """Renders the form for manual uploads and handles resposes."""

    template = {}

    if request.method == 'POST':
        form = ManualUploadForm(request.POST, request.FILES)

        if form.is_valid():
            id_ = form.save(request.user)

            if id_:
                return redirect('activities:view', id_=id_)
            else:
                return redirect('activities:view-all-status', status='failed')

        template['form'] = form
    else:
        template['form'] = ManualUploadForm()

    template['form'].fields['elapsed'].widget = forms.HiddenInput()
    return render(request, 'activities/manual-ul.html', template)


@csrf_protect
@login_required
@require_http_methods(['GET', 'POST'])
def edit(request, id_):
    """Renders the form for editing existing activities and handles received responses.
    Arguments:
        id_: id of the activity
    """

    activity = Activity.objects.get(user=request.user, id=id_)
    template = {'activity': activity}

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=activity)

        if form.is_valid():
            form.save()
            return redirect('activities:view', id_=id_)

        template['form'] = form
    else:
        template['form'] = EditForm(instance=activity)

    return render(request, 'activities/edit.html', template)


@login_required
def delete(request, id_):
    """Deletes an activity from server.
    Arguments:
        id_: id of the activity
    """

    Activity.objects.get(user=request.user, id=id_).delete()
    return redirect('activities:view-all')


@login_required
def view(request, id_):
    """Renders the activity with given id.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    template = {
        'activity': activity,
    }

    return render(request, 'activities/view.html', template)


def _summarize(activities, si_units=True):
    total_time = 0
    total_distance = 0
    count = 0

    for day in activities:
        for activity in day:
            count += 1
            total_time += activity.moving
            total_distance += activity.total_distance

    time = '{}:{:02d}'.format(total_time // 3600, total_time // 60 % 60)
    distance = total_distance / 1000.0 if si_units else total_distance / 1609.0
    dist_str = '{:.1f} {}'.format(distance, 'km' if si_units else 'mi')

    return {'time': time, 'distance': dist_str, 'n': count}


@login_required
def overview(request):
    """Renders the overview of all activities."""

    print request.LANGUAGE_CODE

    now_ = now()

    start = now_ - timedelta(days=(now_.weekday() + 21))
    weekly = []
    for i in range(28):
        date_ = start + timedelta(days=i)
        weekly.append({
            'activities': Activity.objects.filter(user=request.user, date__year=date_.year,
                                                  date__month=date_.month, date__day=date_.day),
            'day': date_.day
        })

    summaries = []
    days = []
    for i in range(4):
        set_ = weekly[(i * 7):(i * 7 + 7)]
        days.append(set_)

        arr = map(lambda x: x['activities'], set_)
        summaries.append(_summarize(arr, request.user.details.si_units))

    year_start = datetime(now_.year, 1, 1)
    month_start = datetime(now_.year, now_.month, 1)
    week_start_inaccurate = start + timedelta(days=21)
    week_start = datetime(week_start_inaccurate.year, week_start_inaccurate.month, week_start_inaccurate.day)
    month_last = calendar.monthrange(now_.year, now_.month)[1]

    ach_year = (Activity.objects.filter(date__gte=year_start, user=request.user)
                                .aggregate(distance=Sum('total_distance'), time=Sum('moving')))
    ach_month = (Activity.objects.filter(date__gte=month_start, user=request.user)
                                 .aggregate(distance=Sum('total_distance'), time=Sum('moving')))
    ach_week = (Activity.objects.filter(date__gte=week_start, user=request.user)
                                .aggregate(distance=Sum('total_distance'), time=Sum('moving')))

    weekly_progress = request.user.goals.weekly_progress(ach_week['distance'], ach_week['time'])
    monthly_progress = request.user.goals.monthly_progress(ach_month['distance'], ach_month['time'])
    yearly_progress = request.user.goals.yearly_progress(ach_year['distance'], ach_year['time'])

    day_of_year = now_.timetuple().tm_yday
    week_multi = ((week_start + timedelta(days=7) - now_.replace(tzinfo=None)).days + 1) / 7.0
    month_multi = now_.day / float(month_last)
    year_multi = day_of_year / 365.0

    template = {
        'weekly': [{'summary': summaries[i], 'days': days[i]} for i in range(4)],
        'weekly_progress': weekly_progress,
        'week_expected': weekly_progress * (7 / week_multi) if week_multi else weekly_progress / 7,
        'monthly_progress': monthly_progress,
        'month_expected': (monthly_progress / float(now_.day) * (month_last * (1 - month_multi)) if month_multi
                           else monthly_progress / month_last),
        'yearly_progress': yearly_progress,
        'year_expected': (yearly_progress / day_of_year * (365 * (1 - year_multi)) if year_multi
                          else yearly_progress / 365),
    }

    return render(request, 'activities/overview.html', template)


@login_required
@csrf_protect
def summary(request):
    """Renders the summary of all activities."""

    return render(request, 'activities/summary.html', {})


@login_required
def charts(request, id_):
    """Renders charts for given activity.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    template = {
        'activity': activity,
    }

    return render(request, 'activities/charts.html', template)


@login_required
def zones(request, id_):
    """Renders zones for given activity.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    template = {
        'activity': activity,
    }

    return render(request, 'activities/zones.html', template)


@login_required
def splits(request, id_):
    """Renders splits for given activity.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    template = {
        'activity': activity,
    }

    return render(request, 'activities/splits.html', template)


@login_required
def map_(request, id_):
    """Renders the big map for given activity.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    template = {
        'activity': activity,
    }

    return render(request, 'activities/map.html', template)


@login_required
def view_all(request, key='date', inverted='', page=1, status=None):
    """Displays all activity the user has uploaded.
    Arguments:
        key: column used for sorting of data
        inverted: invert the default ASC?DESC selection
        page: selected page; must be in range [1..n], where n <= (total activities / 30)
        status: upload status; only when redirected from upload page
    """

    inv_ = bool(inverted)
    key = ORDER_KEYS[key]
    order_key = key if not inverted else '-' + key.replace('-', '')

    page = int(page)

    objects = Activity.objects.filter(user=request.user).order_by(order_key)

    n_pages = objects.count() // 25 + 1
    template = {
        'activities': objects[(page - 1) * 25:page * 25],
        'pages_list': __get_pagination_indexes(n_pages, page),
        'current_page': page,
        'order': {
            'key': key,
            'inverted': inv_
        },
        'status': status
    }
    return render(request, 'activities/view-all.html', template)


@login_required
def ochart(request, id_):
    """Returns JSON data for the overview chart.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)
    distances, d_units = activity.get_distances()
    elevations, e_units = activity.get_elevations()
    speeds, s_units = activity.get_speeds()
    avg_speeds = _average_values(speeds)

    json = [
        zip(distances, elevations),
        zip(distances, avg_speeds)
    ]

    return JsonResponse(json, safe=False)


@login_required
def map_data(request, id_):
    """Returns JSON data for map display.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    return JsonResponse(zip(activity.track.x, activity.track.y), safe=False)


@login_required
def chart_data(request, id_, data_type):
    """Returns JSON object for the display of all detailed charts
    Arguments:
        id_: id of the activity
        data_type: column for which data should be summarized
    ."""

    if data_type not in ['speed', 'elevation', 'hr', 'cadence', 'temperature', 'grade']:
        raise Http404()

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    if data_type == 'elevation':
        y = activity.track.z
    elif data_type == 'speed':
        y = _average_values(activity.get_speeds()[0])
    elif data_type == 'hr':
        y = _average_values(activity.heart_rate, interval=30, precision=0)
    elif data_type == 'cadence':
        y = _average_values(activity.cadence, interval=15, precision=0)
    elif data_type == 'temperature':
        y = _average_values(activity.temperature, precision=1)
    else:
        y = _average_values(activity.get_grades(), interval=45, precision=1)

    if y:
        return JsonResponse(zip(activity.get_distances()[0], y), safe=False)
    else:
        return JsonResponse({'success': False})


@login_required
def zones_data(request, id_, data_type):
    """Returns JSON data for the display of zones.
    Arguments:
        id_: id of the activity
        data_type: column for which data should be summarized
    """

    if data_type not in ['speed', 'elevation', 'hr', 'cadence', 'temperature', 'grade']:
        raise Http404()

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    if data_type == 'elevation':
        y = activity.zones_elevation
    elif data_type == 'speed':
        y = activity.zones_speed
    elif data_type == 'hr':
        y = activity.zones_hr
    elif data_type == 'cadence':
        y = activity.zones_cadence
    elif data_type == 'temperature':
        y = activity.zones_temperature
    else:
        y = activity.zones_grade

    if y:
        data = [(float(k), v) for k, v in y.iteritems()]
        data = sorted(data, key=lambda x: x[0])
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'success': False})


@login_required
def track(request, id_):
    """Returns JSON with all track points.
    Arguments:
        id_: id of the activity
    """

    activity = get_object_or_404(Activity, pk=id_, user=request.user)

    return JsonResponse({'distance': activity.distance, 'time': activity.time,
                         'elevation': activity.track.z, 'hr': activity.heart_rate, 'cad': activity.cadence},
                        safe=False)


@login_required
def period_summary(request, period):
    """Returns JSON containing summarized data for given period.
    Arguments:
        period: period in ['week', 'month', 'year']
    """

    end = now()
    end_midnight = end - timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)

    if period == 'week':
        start = end_midnight - timedelta(days=end.weekday())
    elif period == 'month':
        start = end_midnight - timedelta(days=end.day)
    else:
        start = datetime(end.year, 1, 1)

    qs = Activity.objects.filter(date__range=[start, end], user=request.user)
    summary = qs.aggregate(
        n_activities=Count('id'),
        longest=Max('moving'),
        avg_duration=Avg('moving'),
        total_time=Sum('moving'),
        farthest=Max('total_distance'),
        avg_distance=Avg('total_distance'),
        total_distance=Sum('total_distance'),
        max_speed=Max('speed_max'),
        elev_gain=Sum('elevation_gain'),
        avg_rpe=Avg('rating')
    )

    n_rides = Activity.objects.filter(date__range=[start, end], user=request.user, sport=0).count()
    n_runs = Activity.objects.filter(date__range=[start, end], user=request.user, sport__in=[1, 2, 3, 4]).count()
    n_other = summary['n_activities'] - (n_runs + n_rides)

    summary.update({'n_runs': n_runs, 'n_rides': n_rides, 'n_other': n_other,
                    'avg_speed': (summary['total_distance'] / float(summary['total_time'])
                                  if summary['total_time'] else 0)})
    return JsonResponse(summary, safe=False)


@login_required
def week_chart(request):
    """Returns JSON data for creation of the weekly chart."""
    now_ = now().replace(hour=0, minute=0, second=0)
    start = now_ - timedelta(days=now_.weekday() + 7 * 12)  # 12 weeks
    activities = Activity.objects.filter(date__gte=start, user=request.user).order_by('date')

    return JsonResponse(_summarize_by_period(activities, start), safe=False)


def _summarize_by_period(activities, start, period=7):
    max_ = start + timedelta(days=period)
    data = {'distance': [], 'time': [], 'rating': [], 'n': []}

    for activity in activities:
        if activity.date > max_:
            while activity.date > max_:
                max_ += timedelta(days=period)

                data['distance'].append(0)
                data['time'].append(0)
                data['rating'].append(0)
                data['n'].append(0)

        data['distance'][-1] += activity.total_distance if activity.total_distance else 0
        data['time'][-1] += activity.moving if activity.moving else 0
        data['rating'][-1] += activity.rating * activity.moving // 60 if activity.rating and activity.moving else 0
        data['n'][-1] += 1

    return data


def __get_pagination_indexes(n_pages, current):
    if n_pages < 10:
        return range(1, n_pages + 1)
    elif current < 4:
        return range(1, 10)
    elif current > n_pages + 4:
        return range(n_pages - 9, n_pages + 1)
    else:
        return range(current - 4, current + 5)


def _average_values(values, interval=120, precision=2):
    div = float(interval)

    averages = [values[0]]
    for i, value in enumerate(values[1:], 1):
        if i > interval:
            averages.append(round(sum(values[i - interval:i]) / div, precision))
        else:
            averages.append(round(sum(values[0:i]) / float(i), precision))

    return averages
