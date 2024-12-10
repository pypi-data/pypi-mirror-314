import string
import random
import hashlib
from secrets import token_urlsafe
from django_axor_auth.configurator import config


def generate_backup_codes():
    """Generate backup codes for the user

    Returns:
        list: A list of backup codes
    """
    backup_codes = []
    for _ in range(config.TOTP_NUM_OF_BACKUP_CODES):
        backup_code = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=config.TOTP_BACKUP_CODE_LENGTH))
        backup_codes.append(backup_code)
    return backup_codes


def generate_token():
    # This token length can be of any size as sha256 is used
    # and saved in database as fixed 64 characters. At least
    # 64 characters key is recommended.
    return token_urlsafe(64)


# Hash Function for key
def hash_this(string):
    return hashlib.sha256(str(string).encode('utf-8')).hexdigest()


# Get Client IP Address
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Get User Agent
def getUserAgent(request):
    return request.META.get('HTTP_USER_AGENT')
