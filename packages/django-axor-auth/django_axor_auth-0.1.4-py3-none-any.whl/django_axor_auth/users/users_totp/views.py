from django.utils.encoding import force_str
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_axor_auth.users.permissions import IsAuthenticated
from django_axor_auth.users.users_utils.active_user import get_active_user
from django_axor_auth.utils.error_handling.error_message import ErrorMessage
from django_axor_auth.configurator import config
from .models import Totp


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def totp_init(request):
    # Get user
    user = get_active_user(request)
    # Create TOTP
    new_totp = Totp.objects.create_totp(user)
    if new_totp is None:
        return ErrorMessage(
            title='TOTP is already enabled',
            detail='You are attempting to setup TOTP but it is already enabled.',
            status=400,
            code='TOTPAlreadyEnabledOnInit',
            instance=request.build_absolute_uri()
        ).to_response()
    key, backup_codes, _ = new_totp
    return Response(data={
        'key': key,
        'backup_codes': backup_codes,
        'provision': f"otpauth://totp/{config.APP_NAME}:{user.email.replace('@','%40')}?secret={key}&issuer={config.APP_NAME}"
    }, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def totp_enable(request):
    """ Enable TOTP for the user after user initiates the TOTP.

    Request Parameters:
        code (str): 6 len OTP code only
    """
    token = force_str(request.data.get('code'))
    # If backup code is being used, then return 400 right away
    if len(token) > 6:
        return ErrorMessage(
            title='Invalid TOTP Token',
            detail='Please use a 6-digit TOTP token to enable TOTP. Backup codes cannot be used.',
            status=400,
            code='InvalidTOTPTokenTooLong',
            instance=request.build_absolute_uri()
        ).to_response()
    # Try to authenticate the user
    try:
        # Get user
        user = get_active_user(request)
        # If authenticated, totp object will be returned otherwise None
        totp = Totp.objects.authenticate(user, token)
        # Only enable if the status is initialized
        # Disabled totp's cannot be enabled again
        if totp:
            if totp.status == 'initialized':
                totp.status = 'enabled'
                totp.save()
            return Response(status=200)
        return ErrorMessage(
            title='Invalid TOTP Token',
            detail='The provided TOTP token is invalid. Please try again.',
            status=400,
            code='InvalidTOTPToken',
            instance=request.build_absolute_uri()
        ).to_response()
    except Totp.DoesNotExist:
        return ErrorMessage(
            title='TOTP not set',
            detail='You will need to start the TOTP setup process first.',
            status=400,
            code='TOTPNotSetup',
            instance=request.build_absolute_uri()
        ).to_response()


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def totp_disable(request):
    """ Disable TOTP for the user.

    Request Parameters:
        code (str): 6 len OTP code or 8 len backup code
    """
    # Get the token from request
    token = force_str(request.data.get('code'))
    # Try to authenticate the user
    totp = Totp.objects.authenticate(get_active_user(request), token)
    if totp:
        totp.status = 'disabled'
        totp.updated_at = now()
        totp.save()
        return Response(status=200)
    return ErrorMessage(
        title='Invalid TOTP Token',
        detail='The provided TOTP token or backup code is invalid. Please try again.',
        status=400,
        code='InvalidTOTPToken',
        instance=request.build_absolute_uri()
    ).to_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def totp_new_backup_codes(request):
    """
    Generate new backup codes for the user. Invalidates the old backup codes.
    """
    # Get the token from request
    token = force_str(request.data.get('code'))
    # Try to authenticate the user
    totp = Totp.objects.authenticate(get_active_user(request), token)
    if totp:
        # Create new backup codes
        backup_codes = Totp.objects.create_new_backup_codes(
            get_active_user(request))
        if backup_codes is None:
            return ErrorMessage(
                title='TOTP not set',
                detail='You will need to start the TOTP setup process first.',
                status=400,
                code='TOTPNotSetup',
                instance=request.build_absolute_uri()
            ).to_response()
        return Response(data={'backup_codes': backup_codes}, status=200)
    return ErrorMessage(
        title='Invalid TOTP Token',
        detail='The provided TOTP token or backup code is invalid. Please try again.',
        status=400,
        code='InvalidTOTPToken',
        instance=request.build_absolute_uri()
    ).to_response()
