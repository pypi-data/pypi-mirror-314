import json
from django.utils.timezone import now
from django.db import models
from django_axor_auth.users.users_sessions.utils import get_active_session
from django_axor_auth.users.users_app_tokens.utils import get_active_token


class LogManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_log(self, request, response):
        """Create a Log entry in the database

        Args:
            request: HTTP request object
            response (dict): Response in format of LogResponse.serialize()
            user (User, optional): User who is performing the action. Defaults to logged-in user or None.
        """
        status_code = response['status_code']
        response.pop('status_code', None)
        session = get_active_session(request)
        app_token = get_active_token(request)
        message = json.dumps(response['log_message'] if hasattr(
            response, 'log_message') else response)
        log = self.model(
            url=request.get_full_path(),
            status_code=status_code,
            message=message,
            session_id=session.id if session is not None else None,
            app_token_id=app_token.id if app_token is not None else None,
            source_ip=getClientIP(request),
            created_at=now()
        )
        log.save()


# Get Client IP Address
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
