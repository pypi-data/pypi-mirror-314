from django_axor_auth.configurator import config


class HeaderRequestedByMiddleware:
    """Check for HTTP_X_REQUESTED_BY header and set request.requested_by accordingly.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Run on API requests only
        if request.path.startswith(config.URI_PREFIX):
            # If 'X-Requested-By' header is present and not set to 'web'
            # then token based authentication is used. In such case,
            # provide 'Authorization' header with token.
            if 'HTTP_X_REQUESTED_BY' in request.META:
                request.requested_by = request.META['HTTP_X_REQUESTED_BY']
            else:
                request.requested_by = 'web'

        response = self.get_response(request)
        return response


def is_web(request):
    return request.requested_by == 'web'
