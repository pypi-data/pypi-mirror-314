from typing import Optional

from django_axor_auth.middlewares import is_web
from .models import User, VerifyEmail
from .serializers import UserSerializer
# App Token Imports
from .users_app_tokens.utils import get_active_token
# Session Imports
from .users_sessions.utils import get_active_session


def get_user_by_email(email) -> Optional[User]:
    """
    Get active User object

    Args:
        email (str): User email

    Returns: User or None
    """
    try:
        account = User.objects.get(email=email, is_active=True)
        return account
    except User.DoesNotExist:
        return None


def get_request_user(request) -> User | None:
    """Get the authenticated user from the request.
    This method should only be used if authentication decorator is used in the view to confirm that user is logged in.

    Args:
        request (_type_): _description_

    Returns:
        User: _description_
    """
    if is_web(request):
        # Check if session is active
        session = get_active_session(request)
        if session is not None:
            return session.user
    # if session-based auth is not used then it has to be app token
    app_token = get_active_token(request)
    return app_token.user if app_token is not None else None


def is_cookie_session(request) -> bool:
    """
    Check if cookie based session is being used
    """
    return is_web(request)


def is_token_session(request) -> bool:
    """
    Check if token based session is being used
    """
    return not is_web(request)


def add_user(email, password, first_name, last_name, created_by=None, serialized=False) -> User | Exception:
    """
    Add a new User

    Args:
        email (str): User email
        password (str): User password
        first_name (str): User first name
        last_name (str): User last name
        created_by (User, optional): User object. Defaults to None.
        serialized (bool, optional): Return serialized User. Defaults to False.

    Returns: User or None
    """
    try:
        account = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            created_by=created_by
        )
        if serialized:
            return UserSerializer(data=account).data
        else:
            return account
    except Exception as e:
        raise Exception(e)


def email_exists(email) -> bool:
    """
    Check if email exists

    Args:
        email (str): User email

    Returns: bool
    """
    return User.objects.filter(email=email).exists()


def change_password(user, new_password) -> User | Exception:
    """
    Change user password

    Args:
        user (User): User object
        new_password (str): New password

    Returns: User or Exception
    """
    try:
        user.set_password(new_password)
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def change_email(user, new_email) -> User | Exception:
    """
    Change user email

    Args:
        user (User): User object
        new_email (str): New email

    Returns: User or Exception
    """
    try:
        user.email = new_email
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def change_name(user, new_first_name, new_last_name) -> User | Exception:
    """
    Change user's first and last name

    Args:
        user (User): User object
        new_first_name (str): New first name
        new_last_name (str): New last name

    Returns: User or Exception
    """
    try:
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def disable_user(user: User) -> User | Exception:
    """
    Disable user

    Args:
        user (User): User object

    Returns: User or Exception
    """
    try:
        user.is_active = False
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def enable_user(user) -> User | Exception:
    """
    Enable user

    Args:
        user (User): User object

    Returns: User or Exception
    """
    try:
        user.is_active = True
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def delete_user(user) -> User | Exception:
    """
    Delete user

    Args:
        user (User): User object

    Returns: User or Exception
    """
    try:
        user.delete()
        return user
    except Exception as e:
        raise Exception(e)


# Email Verification

def latest_unused_email_verification(user) -> VerifyEmail | None:
    """
    Get latest email verification

    Args:
        user (User): User object

    Returns: VerifyEmail
    """
    try:
        return VerifyEmail.objects.filter(user=user, is_consumed=False).latest('created_at')
    except Exception as e:
        return None


def get_email_verification(token) -> VerifyEmail | None:
    """
    Get email verification

    Args:
        token (str): Verification token

    Returns: VerifyEmail
    """
    try:
        return VerifyEmail.objects.select_related('user').get(token=token)
    except Exception as e:
        return None


def consume_active_email_verifications(user) -> bool:
    """
    Consume active email verification

    Args:
        user (User): User object

    Returns: bool
    """
    try:
        VerifyEmail.objects.filter(
            user=user, is_consumed=False).update(is_consumed=True)
        return True
    except Exception as e:
        return False
