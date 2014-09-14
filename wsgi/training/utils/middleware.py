from django.http import QueryDict


class PutDeleteMiddleware(object):

    def process_request(self, request):
        if request.method in ('PUT', 'DELETE'):
            if request.method == 'PUT':
                request.PUT = QueryDict(request.body)
            elif request.method == 'DELETE':
                request.DELETE = QueryDict(request.body)

        return None
