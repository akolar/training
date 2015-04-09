from django.http import QueryDict


class PutDeleteMiddleware(object):
    """Provides the ability to use request.PUT or request.DELETE."""

    def process_request(self, request):
        """Adds the passed data to request object."""

        if request.method in ('PUT', 'DELETE'):
            if request.method == 'PUT':
                request.PUT = QueryDict(request.body)
            elif request.method == 'DELETE':
                request.DELETE = QueryDict(request.body)

        return None
