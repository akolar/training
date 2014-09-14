from django.core.context_processors import csrf


def request_context(request):
    d = {'user': request.user}
    d.update(csrf(request))

    return d
