from django.core.mail import send_mail

from django_axor_auth.users.users_utils.emailing.templates.email_changed import email_changed_template
from django_axor_auth.users.users_utils.emailing.templates.resend_verification_email import email_verification_template
from .templates.new_user_account import new_user_account_template
from .templates.forgot_password import forgot_password_template
from .templates.reset_password_success import reset_password_success_template
from .templates.magic_link import magic_link_template
from django_axor_auth.utils.emailing.helper import getEmailConnection
from django_axor_auth.configurator import config


def send_welcome_email(first_name: str, verification_url: str, email: str):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = new_user_account_template(first_name, verification_url)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nPlease verify your email by clicking the link below.\n\n{
                verification_url}"
            return send_mail(subject='Welcome to ' + config.APP_NAME,
                             message=message,
                             html_message=template,
                             from_email=config.SMTP_DEFAULT_SEND_FROM,
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_forgot_password_email(first_name: str, reset_url: str, email: str, ip: str, subject='Reset your password'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `ip` (str): IP address of the user requesting password reset.
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = forgot_password_template(first_name, reset_url, ip, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nPlease reset your password by clicking the link below.\n\n{reset_url}"
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config.SMTP_DEFAULT_SEND_FROM,
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_password_changed_email(first_name: str, email: str, subject='Password was changed'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = reset_password_success_template(first_name, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {
                first_name},\n\nYour password was successfully changed. If you did not make this change, please contact our support immediately."
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config.SMTP_DEFAULT_SEND_FROM,
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_email_changed_email(first_name: str, verification_url: str, email: str, subject='Email Changed Successfully!'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = email_changed_template(first_name, verification_url, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nPlease verify your new email by clicking the link below.\n\n{
                verification_url}"
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config.SMTP_DEFAULT_SEND_FROM,
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_magic_link_email(first_name: str, url: str, email: str, subject='Sign in with Magic Link'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `subject` (str, optional): Email subject.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = magic_link_template(first_name, url, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nYour magic link is ready!\n\n{url}"
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config.SMTP_DEFAULT_SEND_FROM,
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_verification_email(first_name: str, verification_url: str, email: str, subject='Verify your email'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = email_verification_template(first_name, verification_url)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nPlease verify your email by clicking the link below.\n\n{
                verification_url}"
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config.SMTP_DEFAULT_SEND_FROM,
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0
