from django.core.context_processors import csrf


def request_context(request):
    """Automatically adds request.user when rendering a page."""

    d = {'user': request.user}
    d.update(csrf(request))

    return d
