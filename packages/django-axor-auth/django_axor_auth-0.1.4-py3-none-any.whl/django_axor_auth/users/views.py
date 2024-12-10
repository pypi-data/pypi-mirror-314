import urllib.parse
from datetime import timedelta
from secrets import token_urlsafe

# JWT
import jwt
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django_axor_auth.configurator import config
from django_axor_auth.middlewares import is_web
from django_axor_auth.security.hashing import hash_this
from django_axor_auth.utils.error_handling.error_message import ErrorMessage
from .api import consume_active_email_verifications, email_exists, get_request_user, latest_unused_email_verification, \
    get_email_verification
from .permissions import IsAuthenticated
# User Imports
from .serializers import EmailSerializer, PasswordSerializer, UserSerializer, LoginSerializer, RegistrationSerializer, \
    VerifyEmailSerializer
# App Token Imports
from .users_app_tokens.api import create_app_token, get_last_token_session_details, delete_app_token, \
    delete_all_app_tokens, delete_all_app_tokens_except, get_all_active_app_tokens
from .users_app_tokens.utils import get_active_token
# Session Imports
from .users_sessions.api import create_session, delete_session, get_last_session_details, delete_all_sessions, \
    delete_all_sessions_except, get_all_active_sessions
from .users_sessions.utils import get_active_session
# TOTP Imports
from .users_totp.api import has_totp, authenticate_totp
# Email
from .users_utils.emailing.api import send_email_changed_email, send_password_changed_email, send_welcome_email, \
    send_verification_email as send_general_verification_email


@api_view(['POST'])
def register(request):
    # Check if registration is enabled
    if config.IS_REGISTRATION_ENABLED is False:
        return ErrorMessage(
            detail='Registration is disabled.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Registration disabled',
            code='RegistrationDisabled'
        ).to_response()
    # Validate request data and create user
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Send email verification
        user = serializer.validated_data
        send_verification_email(user, is_new_account=True)
        # login user
        try:
            return login(request._request)
        except Exception as e:
            # Return error message
            err_msg = ErrorMessage(
                detail=str(e),
                status=400,
                instance=request.build_absolute_uri(),
                title='Invalid information provided.',
                code='InvalidRegistrationInfo'
            )
            return err_msg.to_response()
    # Return error message
    errors = serializer.errors
    err_msg = ErrorMessage(
        detail=errors,
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid information provided.',
        code='InvalidRegistrationInfo'
    )
    return err_msg.to_response()


# Login user
# --------------------------------------------------------------------
@api_view(['POST'])
def login(request):
    # Validate request data
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Get user
        user = serializer.validated_data
        # Login user
        return finish_login(request, user)
    errors = serializer.errors
    err_msg = ErrorMessage(
        detail=errors,
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid credentials',
        code='LoginSerializerErrors'
    )
    return err_msg.to_response()


def magic_link_login(request, user):
    # Login user
    return finish_login(request, user)


def finish_login(request, user):
    # Check if user hash TOTP enabled
    totp_row = has_totp(user)
    if totp_row is not None:
        # If totp code is not provided
        if 'code' not in request.data or (
                'code' in request.data and (request.data['code'] is None or request.data['code'] == '')):
            return ErrorMessage(
                detail="TOTP code is required.",
                status=401,
                instance=request.build_absolute_uri(),
                title='2FA code is required',
                code='TOTPRequired'
            ).to_response()
        # Authenticate TOTP
        if not authenticate_totp(user, force_str(request.data['code']), totp_row):
            return ErrorMessage(
                detail="Provided TOTP code or backup code is incorrect. Please try again.",
                status=401,
                instance=request.build_absolute_uri(),
                title='2FA code is incorrect',
                code='TOTPIncorrect'
            ).to_response()
    # Get last session details
    last_session = get_last_session_details(user)  # already serialized
    last_token_session = get_last_token_session_details(
        user)  # already serialized
    # Respond depending on the client
    if is_web(request):
        # Session based authentication
        key, session = create_session(user, request)
        # Add HTTPOnly cookie
        response = Response(data={
            "last_session": last_session,
            "last_token_session": last_token_session,
            "user": UserSerializer(user).data
        },
            status=200
        )
        response.set_cookie(
            key=config.AUTH_COOKIE_NAME,
            value=jwt.encode(
                {
                    "session_key": key
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            ),
            expires=session.expire_at,
            httponly=True,
            secure=config.AUTH_COOKIE_SECURE,
            samesite=config.AUTH_COOKIE_SAMESITE,
            domain=config.AUTH_COOKIE_DOMAIN
        )
        return response
    else:
        # Token based authentication
        token, app_token = create_app_token(user, request)
        # Respond with token and user data
        return Response(data={
            "last_session": last_session,
            "last_token_session": last_token_session,
            "user": UserSerializer(user).data,
            "app_token": dict(
                id=app_token.id,
                token=jwt.encode(
                    {
                        "app_token": token
                    },
                    settings.SECRET_KEY,
                    algorithm='HS256'
                ),
            )
        }, status=200)


# Delete user
# --------------------------------------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete session or token
    if is_web(request):
        delete_session(get_active_session(request).user,
                       get_active_session(request).id)
        response = Response(status=200)
        response.delete_cookie(
            key=config.AUTH_COOKIE_NAME,
            domain=config.AUTH_COOKIE_DOMAIN
        )
        return response
    else:
        delete_app_token(get_active_token(request).user,
                         get_active_token(request).id)
    # Return response
    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    # Session-based authentication
    if is_web(request):
        session = get_active_session(request)
        if session is not None:
            return Response(data=dict(
                user=UserSerializer(session.user).data
            ), status=200)
    # Token-based authentication
    app_token = get_active_token(request)
    if app_token is not None:
        return Response(data=UserSerializer(app_token.user).data, status=200)
    # No valid active session or token found
    return ErrorMessage(
        detail='No active session or token found.',
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid request',
        code='NoActiveSessionOrToken'
    ).to_response()


# Change Password, requires old password and new password
# --------------------------------------------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = get_request_user(request)
    # Check if old password and new password are provided
    if 'old_password' not in request.data or 'new_password' not in request.data:
        return ErrorMessage(
            detail='Old password and new password are required.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Insufficient data',
            code='OldNewPasswordRequired'
        ).to_response()
    old_password = force_str(request.data['old_password'])
    new_password = force_str(request.data['new_password'])
    # Check if old password is correct
    if LoginSerializer(data=dict(email=user.email, password=old_password)).is_valid():
        # Validate new password
        if PasswordSerializer(data=dict(password=new_password)).is_valid() is False:
            return ErrorMessage(
                detail='New password is invalid.',
                status=400,
                instance=request.build_absolute_uri(),
                title='Invalid new password',
                code='InvalidNewPassword'
            ).to_response()
        # Update password
        user.set_password(new_password)
        # Disable all existing sessions except current
        if is_web(request):
            delete_all_sessions_except(user, get_active_session(request).id)
            delete_all_app_tokens(user)
        else:
            delete_all_app_tokens_except(user, get_active_token(request).id)
            delete_all_sessions(user)
        # Send password change email
        send_password_changed_email(user.first_name, user.email)
        return Response(status=204)
    # Auth with old password failed
    return ErrorMessage(
        detail='Old password is incorrect.',
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid old password',
        code='InvalidOldPassword'
    ).to_response()


# Change Name, requires new name
# --------------------------------------------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_name(request):
    user = get_request_user(request)
    # Check if first name and last name are provided
    if 'first_name' not in request.data or 'last_name' not in request.data:
        return ErrorMessage(
            detail='First name and last name are required.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Insufficient data',
            code='FirstNameLastNameRequired'
        ).to_response()
    # Update name
    user.first_name = force_str(request.data['first_name'])
    user.last_name = force_str(request.data['last_name'])
    user.updated_at = now()
    user.save()
    return Response(data=UserSerializer(user).data, status=200)


# Change Email, requires new email, password
# --------------------------------------------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_email(request):
    user = get_request_user(request)
    # Check if email and password are provided
    if 'email' not in request.data or 'password' not in request.data:
        return ErrorMessage(
            detail='Email and password are required.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Insufficient data',
            code='EmailPasswordRequired'
        ).to_response()
    email = force_str(request.data['email']).strip()
    password = force_str(request.data['password'])
    # Check if it valid email
    if not EmailSerializer(data=dict(email=email)).is_valid():
        return ErrorMessage(
            detail='Email is invalid.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Invalid email',
            code='InvalidEmail'
        ).to_response()
    # Check if password is correct
    if not LoginSerializer(data=dict(email=user.email, password=password)).is_valid():
        return ErrorMessage(
            detail='Password is incorrect.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Invalid password',
            code='InvalidPassword'
        ).to_response()
    # Check if email is not the same
    if user.email == email:
        return ErrorMessage(
            detail='Email is the same.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Same email',
            code='SameEmail'
        ).to_response()
    # Check if email is not in use
    if email_exists(email):
        return ErrorMessage(
            detail='Email is already in use.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Email in use',
            code='EmailInUse'
        ).to_response()

    # Update email
    user.email = email
    user.is_email_verified = False
    user.updated_at = now()
    user.save()

    # Generate and send new email verification token
    sent = send_verification_email(user, is_email_changed=True)
    if sent:
        return Response(data=UserSerializer(user).data, status=200)
    return ErrorMessage(
        detail='Email changed but failed to send email with verification link. Please request a new verification link.',
        status=400,
        instance=request.build_absolute_uri(),
        title='Sending verification email failed',
        code='SendingVerificationEmailFailed'
    ).to_response()


# Verify email
# --------------------------------------------------------------------
@api_view(['POST'])
def verify_email(request):
    if 'token' not in request.data:
        return ErrorMessage(
            detail='Token is required.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Insufficient data',
            code='TokenRequired'
        ).to_response()
    token = force_str(request.data['token'])
    row = get_email_verification(hash_this(token))
    if row and not row.is_consumed and row.created_at > now() - timedelta(
            seconds=config.EMAIL_VERIFICATION_LINK_TIMEOUT):
        row.is_consumed = True
        row.save()
        row.user.is_email_verified = True
        row.user.save()
        return Response(status=204)
    elif row.user.is_email_verified:
        return Response(status=204)
    return ErrorMessage(
        title='Invalid token',
        detail='Token is invalid or expired.',
        status=400,
        instance=request.build_absolute_uri(),
        code='InvalidToken'
    ).to_response()


# Resend Verification Email if user is unverified
# --------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_verification_email(request):
    user = get_request_user(request)
    if user.is_email_verified:
        return ErrorMessage(
            detail='Email is already verified.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Email verified',
            code='EmailVerified'
        ).to_response()

    # Check if last email was sent at least xx seconds ago (config.EMAIL_VERIFICATION_LINK_TIMEOUT)
    latest_email_sent = latest_unused_email_verification(user)
    if latest_email_sent and latest_email_sent.created_at + timedelta(
            seconds=config.EMAIL_VERIFICATION_LINK_TIMEOUT) > now():
        time_to_wait = (latest_email_sent.created_at + timedelta(
            seconds=config.EMAIL_VERIFICATION_LINK_TIMEOUT) - now()).seconds // 60
        return ErrorMessage(
            detail=f'Email verification link was sent recently. Please wait {
            time_to_wait} minutes before requesting another link.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Email verification link sent recently',
            code='EmailVerificationLinkSentRecently'
        ).to_response()

    # Consume latest email verification
    if latest_email_sent:
        latest_email_sent.is_consumed = True
        latest_email_sent.save()

    # Generate and send new email verification token
    sent = send_verification_email(user)
    if sent:
        return Response(status=204)
    return ErrorMessage(
        detail='Failed to send email verification link.',
        status=400,
        instance=request.build_absolute_uri(),
        title='Email verification failed',
        code='EmailVerificationFailed'
    ).to_response()


# Active user sessions, both session and token
# --------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_sessions(request):
    user = get_request_user(request)
    sessions = get_all_active_sessions(user, True)
    tokens = get_all_active_app_tokens(user, True)
    return Response(data=dict(
        sessions=sessions,
        tokens=tokens
    ), status=200)


# Close a session
# --------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_session(request):
    user = get_request_user(request)
    uid = force_str(request.data.get('id'))
    if delete_session(user, uid):
        return Response(status=204)
    elif delete_app_token(user, uid):
        return Response(status=204)
    else:
        return ErrorMessage(
            detail='Session or token not found.',
            status=400,
            instance=request.build_absolute_uri(),
            title='Session or token not found',
            code='SessionTokenNotFound'
        ).to_response()


# Closed all sessions except current
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_all_sessions_except_current(request):
    user = get_request_user(request)
    if is_web(request):
        delete_all_sessions_except(user, get_active_session(request).id)
    else:
        delete_all_app_tokens_except(user, get_active_token(request).id)
    return Response(status=204)


# --------------------------------------------------------------------

def send_verification_email(user, is_new_account=False, is_email_changed=False) -> bool:
    # Generate and send email verification token
    verify_token = token_urlsafe(42)
    verify_serializer = VerifyEmailSerializer(data=dict(
        user=user.id,
        token=hash_this(verify_token),
        created_at=now()
    ))
    if verify_serializer.is_valid():
        # Delete previous verification tokens
        consume_active_email_verifications(user)
        # Save new
        verify_serializer.save()
        # Send email
        uri = config.EMAIL_VERIFICATION_LINK.replace("<token>", verify_token)
        verification_url = urllib.parse.urljoin(config.FRONTEND_URL, uri)
        if is_new_account:
            send_welcome_email(user.first_name, verification_url, user.email)
        elif is_email_changed:
            send_email_changed_email(user.first_name, verification_url, user.email)
        else:
            send_general_verification_email(user.first_name, verification_url, user.email)
        return True
    return False
