from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(['PUT'])
def set(request, target):
    """Sets user's goal.
    Arguments:
        target: target in ['week', 'month', 'year']
    """

    objective = request.PUT.get('objective')
    value = request.PUT.get('value')
    if objective not in ['distance', 'time']:
        return JsonResponse({'success': False})

    try:
        goals = request.user.goals
        setattr(goals, '{}ly_{}'.format(target, objective), int(value))
        goals.save()
    except Exception:
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})
