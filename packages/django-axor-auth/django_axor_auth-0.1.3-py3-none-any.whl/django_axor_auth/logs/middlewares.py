from django.utils.timezone import now
from datetime import timedelta
import json
from .models import ApiCallLog
from .log_response import LogResponse
from django_axor_auth.configurator import config
from django_axor_auth.users.api import get_request_user


class APILogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        # Don't run on non-API requests
        if not request.path.startswith(config.URI_PREFIX):
            return response

        # Don't log if logging is disabled
        if not config.ENABLE_LOGGING:
            return response

        # Dont log if only authenticated users are allowed to log
        if get_request_user(request) is None and config.LOG_ONLY_AUTHENTICATED:
            return response

        # Create log
        try:
            content = json.loads(response.content.decode('utf8'))
        except json.JSONDecodeError:
            # If response is not JSON or empty
            content = dict()

        log = None

        if response.status_code > 399 and config.LOG_4XX:
            if 'instance' in content:
                # Omit instance as it is from ErrorMessage class
                # instance also carries the URL that caused the error
                # but this information is already in model's URL column
                content.pop('instance')
            if 'status' in content:
                # Omit status as it is already in model's status column
                content.pop('status')
            log = LogResponse(status=response.status_code, message=content)
            # Delete old logs
            logs = ApiCallLog.objects.filter(
                status_code=response.status_code).order_by('created_at')
            retention_period = now() - timedelta(seconds=config.LOG_4XX_MAX_AGE)
            count = logs.count()
            if count > config.LOG_4XX_MAX_NUM:
                # Delete the diff and 10% more for breathing space
                num_to_delete = count - config.LOG_4XX_MAX_NUM
                num_to_delete = num_to_delete + int(config.LOG_4XX_MAX_NUM * 0.1)
                if num_to_delete < count:
                    logs.filter(
                        created_at__lt=logs[num_to_delete].created_at).delete()
            # Delete logs older than retention period
            logs.filter(created_at__lt=retention_period).delete()

        elif response.status_code > 199 and config.LOG_2XX:
            # Don't log login and signup requests
            if 'login' in request.path or 'signup' in request.path:
                return response
            log = LogResponse(status=response.status_code)
            # Delete the oldest logs if the limit is exceeded
            logs = ApiCallLog.objects.filter(
                status_code=response.status_code).order_by('created_at')
            retention_period = now() - timedelta(seconds=config.LOG_2XX_MAX_AGE)
            count = logs.count()
            if count > config.LOG_2XX_MAX_NUM:
                # Delete the diff and 10% more for breathing space
                num_to_delete = count - config.LOG_2XX_MAX_NUM
                num_to_delete = num_to_delete + int(config.LOG_2XX_MAX_NUM * 0.1)
                if num_to_delete < count:
                    logs.filter(
                        created_at__lt=logs[num_to_delete].created_at).delete()
            # Delete logs older than retention period
            logs.filter(created_at__lt=retention_period).delete()

        # Create log
        if log is not None:
            ApiCallLog.objects.create_log(
                request=request,
                response=log.serialize(),
            )

        return response
