from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required()
def settings(request):
    template = RequestContext(request)
    return render_to_response('health/settings.html', template)
