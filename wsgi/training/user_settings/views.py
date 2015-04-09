import re

from django.shortcuts import render_to_response, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from activities.forms import EquipmentForm
from activities.models import Equipment


@login_required
def index(request):
    """Renders the settings' index page."""

    return render_to_response('settings/index.html', context_instance=RequestContext(request))


@login_required
def about(request):
    """Renders the About form."""

    return render_to_response('settings/me.html', context_instance=RequestContext(request))


@login_required
def equipment(request):
    """Renders the list of all equipment."""

    template = {
        'other': Equipment.objects.filter(user=request.user, sport=-1),
        'bike': Equipment.objects.filter(user=request.user, sport=0),
        'shoes': Equipment.objects.filter(user=request.user, sport=1)
    }

    return render(request, 'settings/equipment.html', template)


@login_required
def account(request):
    """Renders the account settings."""

    return render_to_response('settings/account.html', context_instance=RequestContext(request))


@require_http_methods(['PUT'])
@login_required
def settings_save(request, key):
    """Saves the sent data to database.
    Arguments:
        key: target column
    """

    def __get_gender(value):
        if value == 'male':
            return True
        elif value == 'female':
            return False

        return None

    def __get_units(value):
        return value == 'metric'

    def __validate_email(value):
        return re.match('[^@]+@[^@]+\.[^@]+', value) is not None

    value = request.PUT.get('value')
    if not value and key in ('name', 'gender', 'height', 'email'):
        return JsonResponse({'success': False})

    user = request.user

    if key == 'name':
        value = value.strip()
        parts = value.split(' ')
        user.first_name = ' '.join(parts[:-1]) if len(parts) > 1 else parts[0]
        user.last_name = parts[-1] if len(parts) > 1 else ''
        user.save()

    elif key == 'gender':
        user.details.gender = __get_gender(value)
        user.details.save()

    elif key == 'height':
        height = int(value) if value else None
        user.athlete.height = height
        user.athlete.save()

    elif key == 'mhr':
        mhr = int(value) if value else None
        user.athlete.max_hr = mhr
        user.athlete.save()

    elif key == 'lthr':
        lthr = int(value) if value else None
        user.athlete.lt_hr = lthr
        user.athlete.save()

    elif key == 'mp':
        mp = int(value) if value else None
        user.athlete.max_power = mp
        user.athlete.save()

    elif key == 'ftp':
        ftp = int(value) if value else None
        user.athlete.lt_power = ftp
        user.athlete.save()

    elif key == 'email' and __validate_email(value):
        user.email = value
        user.save()

    elif key == 'email':
        return JsonResponse({'success': False})

    elif key == 'password':
        current = request.PUT.get('current')
        new = request.PUT.get('new1')
        new2 = request.PUT.get('new2')

        if not request.user.check_password(current):
            return JsonResponse({'success': False, 'reason': 'invalid-current'})
        elif new != new2:
            return JsonResponse({'success': False, 'reason': 'do-not-match'})

        user.set_password(new)
        user.save()

    elif key == 'units':
        user.details.si_units = __get_units(value)
        multi = 1.609 if user.details.si_units else (1 / 1.609)
        user.goals.weekly_distance *= multi
        user.goals.monthly_distance *= multi
        user.goals.yearly_distance *= multi
        user.details.save()
        user.goals.save()

    else:
        raise Http404()

    return JsonResponse({'success': True})


@require_http_methods(['POST'])
@login_required
def avatar_save(request):
    """Uploads the avatar."""

    try:
        request.user.details.avatar = request.FILES['avatar']
        request.user.details.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})


@require_http_methods(['GET', 'POST'])
@login_required
@csrf_protect
def equipment_add(request, type_, id_=None):
    """Adds an equipment."""

    template = {}

    if request.method == 'POST':
        form = EquipmentForm(request.POST)

        if form.is_valid():
            form.save(request.user, id_)
            return redirect('settings_equipment')

        template['form'] = form
    elif id_:
        template['form'] = EquipmentForm(instance=Equipment.objects.get(pk=id_))
    else:
        template['form'] = EquipmentForm()

    return render(request, 'settings/equipment_add.html', template)
