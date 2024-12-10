import jwt
from django.conf import settings
from django.utils.encoding import force_str

from django_axor_auth.configurator import config
from .users_app_tokens.models import AppToken
from .users_sessions.models import Session
from .users_sessions.utils import getClientIP, getUserAgent


class ActiveUserMiddleware:
    """This reads the Cookie or Authorization header and authenticates the user.

    For Cookie-based authentication, `request.active_session` gets be attached to the request.

    For Authorization header-based authentication, `request.active_token` gets be attached to the request.

    To get the authenticated user, use `django-axor-auth.users.api.get_request_user(request)` method.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.COOKIE_NAME = config.AUTH_COOKIE_NAME

    def __call__(self, request):
        app_token = self.get_active_app_token(request)
        session = self.get_active_session(request)
        # Attach the session to the request
        request.active_token = app_token
        request.active_session = session

        response = self.get_response(request)
        return response

    def get_active_session(self, request):
        session = None
        # Check if auth token is present in cookies
        try:
            key = request.COOKIES.get(self.COOKIE_NAME)
            try:
                decoded_jwt_key = jwt.decode(
                    key, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.InvalidSignatureError:
                return None
            key = decoded_jwt_key.get('session_key')
            session = Session.objects.authenticate_session(
                key, getClientIP(request), getUserAgent(request))
            return session
        except (KeyError, Exception) as e:
            session = None
        return session

    def get_active_app_token(self, request):
        app_token = None
        # Check if auth token is present in header
        if app_token is None and 'Authorization' in request.headers:
            token = force_str(request.headers['Authorization'])
            if token is None:
                return None
            token = token.split(' ')[-1]  # Get the token from 'Bearer <token>'
            try:
                decoded_jwt_token = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=['HS256'])
                token = decoded_jwt_token.get('app_token')
                return AppToken.objects.authenticate_app_token(token, getUserAgent(request))
            except jwt.InvalidSignatureError:
                app_token = None
        return app_token
