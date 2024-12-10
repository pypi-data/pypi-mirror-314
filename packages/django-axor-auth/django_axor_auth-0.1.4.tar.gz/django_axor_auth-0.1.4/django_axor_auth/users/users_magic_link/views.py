import urllib.parse

from django.utils.encoding import force_str
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_axor_auth.configurator import config
from django_axor_auth.users.api import get_user_by_email
from django_axor_auth.users.users_utils.emailing.api import send_magic_link_email
from django_axor_auth.users.views import magic_link_login
from django_axor_auth.utils.error_handling.error_message import ErrorMessage
from .models import MagicLink
from .utils import hash_this


@api_view(['POST'])
def request_magic_link(request):
    # Check if all required fields are provided
    if 'email' not in request.data:
        err = ErrorMessage(
            title='Email is required.',
            status=400,
            detail='Email is required.',
            instance=request.get_full_path(),
        )
        return err.to_response()
    email = force_str(request.data['email']).strip()
    user = get_user_by_email(email)
    # if user is not found, return
    if not user:
        return Response(status=204)
    # Create forgot password instance
    token, row = MagicLink.objects.create_magic_link(request, user)
    if token and row:
        # Send email with token
        uri = config.MAGIC_LINK_URL.replace('<token>', token)
        if uri.startswith('http'):
            url = uri
        else:
            url = urllib.parse.urljoin(config.FRONTEND_URL, uri)
        send_magic_link_email(
            email=row.user.email,
            url=url,
            first_name=row.user.first_name,
            subject='Sign in to ' + config.APP_NAME
        )
    # Send empty success response
    return Response(status=204)


@api_view(['POST'])
def consume_magic_link(request):
    # Check if token in request data
    if 'token' not in request.data:
        err = ErrorMessage(
            title='Token is required.',
            status=400,
            detail='Token is required.',
            instance=request.get_full_path(),
            code='TokenRequired'
        )
        return err.to_response()
    token = force_str(request.data['token']).strip()
    # Get magic link instance
    try:
        row = MagicLink.objects.select_related('user').get(token=hash_this(token))
        if row.check_valid():
            # login
            response = magic_link_login(request, row.user)
            if response.status_code >= 400:
                return response
            # Set magic link as used
            row.set_used()
            # if user email was not verified, verify it
            if not row.user.is_email_verified:
                row.user.is_email_verified = True
                row.user.save()
            return response
        else:
            err = ErrorMessage(
                title='Invalid token',
                status=400,
                detail='Invalid token.',
                instance=request.get_full_path(),
                code='InvalidToken'
            )
            return err.to_response()
    except MagicLink.DoesNotExist:
        err = ErrorMessage(
            title='Invalid token',
            status=400,
            detail='Invalid token.',
            instance=request.get_full_path(),
            code='InvalidToken'
        )
        return err.to_response()
