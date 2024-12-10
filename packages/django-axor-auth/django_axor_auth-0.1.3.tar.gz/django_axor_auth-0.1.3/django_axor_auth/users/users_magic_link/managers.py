from django.db import models
from django.utils.timezone import now
from .utils import generateKey, getClientIP, getUserAgent, hash_this


class MagicLinkManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_magic_link(self, request, user):
        # create forgot password instance
        key = generateKey()
        fp = self.create(
            user=user,
            token=hash_this(key),
            source_ip=getClientIP(request),
            source_ua=getUserAgent(request),
            created_at=now()
        )
        return key, fp
