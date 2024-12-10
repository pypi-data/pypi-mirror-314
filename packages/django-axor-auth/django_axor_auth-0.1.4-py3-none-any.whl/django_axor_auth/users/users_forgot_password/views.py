import urllib
from datetime import timedelta

from django.utils.encoding import force_str
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_axor_auth.configurator import config
from django_axor_auth.users.api import get_user_by_email
from django_axor_auth.users.serializers import PasswordSerializer
from django_axor_auth.users.users_utils.emailing.api import send_forgot_password_email, send_password_changed_email
from django_axor_auth.utils.error_handling.error_message import ErrorMessage
from .models import ForgotPassword
from .serializers import HealthyForgotPasswordSerializer
from .utils import getClientIP


@api_view(['POST'])
def forgot_password(request):
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
    # if last request was made in lockout window, return
    last_fp = ForgotPassword.objects.filter(user=user).order_by('-created_at').first()
    if last_fp and last_fp.created_at > now() - timedelta(seconds=config.FORGET_PASSWORD_LOCKOUT_TIME):
        return Response(status=204)
    # Create forgot password instance
    token, fp = ForgotPassword.objects.create_forgot_password(request, user)
    if token and fp:
        # Send email with token
        uri = config.FORGET_PASSWORD_LINK.replace('<token>', token)
        url = urllib.parse.urljoin(config.FRONTEND_URL, uri)
        send_forgot_password_email(
            email=fp.user.email,
            reset_url=url,
            first_name=fp.user.first_name,
            subject='Reset your password',
            ip=getClientIP(request),
        )
    # Send empty success response
    return Response(status=204)


@api_view(['POST'])
def check_health(request):
    token = force_str(request.data['token'])
    serializer = HealthyForgotPasswordSerializer(data={'token': token})
    if not serializer.is_valid():
        err = ErrorMessage(
            title='Invalid Request',
            status=400,
            detail=serializer.errors,
            instance=request.get_full_path(),
        )
        return err.to_response()
    # Send empty success response
    return Response(status=204)


def _check_health(token):
    serializer = HealthyForgotPasswordSerializer(data={'token': token})
    if not serializer.is_valid():
        return False
    return True


@api_view(['POST'])
def reset_password(request):
    # Check if password is provided
    if 'password' not in request.data:
        err = ErrorMessage(
            title='Password Required',
            status=400,
            detail='Password is required.',
            instance=request.get_full_path(),
            code="InsufficientData"
        )
        return err.to_response()
    token = force_str(request.data['token'])
    # Check if key is valid
    serializer = HealthyForgotPasswordSerializer(data={'token': token})
    if not serializer.is_valid():
        err = ErrorMessage(
            title='Invalid Request',
            status=400,
            detail=serializer.errors,
            instance=request.get_full_path(),
            code="HealthCheckFailed"
        )
        return err.to_response()
    fp = serializer.validated_data
    # Validate password
    serializer = PasswordSerializer(data=request.data)
    if serializer.is_valid():
        # Set new password
        fp.user.set_password(force_str(request.data['password']))
        fp.user.save()
        # Set fp as used
        fp.set_used()
        # Send notification email to user
        send_password_changed_email(
            email=fp.user.email,
            first_name=fp.user.first_name,
            subject='Password Changed'
        )
        # Send empty success response
        return Response(status=204)
    else:
        err = ErrorMessage(
            title='Encountered Error',
            status=400,
            detail=serializer.errors,
            instance=request.get_full_path(),
        )
        return err.to_response()
