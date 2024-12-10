import json
from django.http import JsonResponse
from django.conf import settings
from ..utils.error_handling.error_message import ErrorMessage
from ..configurator import config


class ValidateJsonMiddleware:
    """Check if the request body data is valid JSON.

    This only works for POST, PUT, and PATCH requests. If the request body
    is not a valid JSON, the request is halted and an error message is
    given as response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Run on API requests only
        if request.path.startswith(config.URI_PREFIX) and request.content_type == 'application/json':
            if not self.validate_json_payload(request):
                error = ErrorMessage(
                    detail='Invalid JSON payload.',
                    status=400,
                    instance=request.build_absolute_uri(),
                    title='Invalid data provided'
                )
                return JsonResponse(
                    error.serialize(),
                    status=400)

        response = self.get_response(request)
        return response

    def validate_json_payload(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request.data = json.loads(request.body)
                return True
            except json.JSONDecodeError:
                return False
        return True


class VerifyRequestOriginMiddleware:
    """ Verifies if a request origin is allowed to make requests.

    For an origin to make request, it has to be in settings.ALLOW_ORIGINS list.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Run on API requests only
        if request.path.startswith(config.URI_PREFIX):
            # If Token authentication is used that means
            # the API is accessed by a non-web application.
            # In that case, we don't need to check the origin.
            # OTHERWISE check the origin header!
            if request.active_token is None:
                if not self.validate_origin_header(request):
                    error = ErrorMessage(
                        detail='You are not authorized to perform this action.',
                        status=400,
                        instance=request.build_absolute_uri(),
                        title='Action not allowed.'
                    )
                    return JsonResponse(
                        error.serialize(),
                        status=400)

        response = self.get_response(request)
        return response

    def validate_origin_header(self, request):
        # If DEBUG is True, allow all origins
        if settings.DEBUG:
            return True
        # If ALLOW_ORIGINS is set to '*', allow all origins
        if len(settings.ALLOW_ORIGINS) > 0 and settings.ALLOW_ORIGINS[0] == '*':
            return True
        # Check if the request origin is in ALLOW_ORIGINS
        if request.headers.get('Origin') in settings.ALLOW_ORIGINS:
            return True
        return False
