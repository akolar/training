import re

from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods


@login_required
def index(request):
    return render_to_response('settings/index.html',
                              context_instance=RequestContext(request))


@login_required
def about(request):
    return render_to_response('settings/me.html',
                              context_instance=RequestContext(request))


@login_required
def equipment(request):
    return render_to_response('settings/equipment.html',
                              context_instance=RequestContext(request))


@login_required
def account(request):
    return render_to_response('settings/account.html',
                              context_instance=RequestContext(request))


@require_http_methods(['PUT'])
@login_required
def settings_save(request, key):
    def __get_gender(value):
        if value == 'male':
            return True
        elif value == 'female':
            return False

        return None

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
            return JsonResponse({'success': False,
                                 'reason': 'invalid-current'})
        elif new != new2:
            return JsonResponse({'success': False,
                                 'reason': 'do-not-match'})

        user.set_password(new)
        user.save()

    else:
        raise Http404()

    return JsonResponse({'success': True})


@require_http_methods(['POST'])
@login_required
def avatar_save(request):
    try:
        request.user.details.avatar = request.FILES['avatar']
        request.user.details.save()
        return JsonResponse({'success': True})
    except Exception as e:
        print e
        return JsonResponse({'success': False})
