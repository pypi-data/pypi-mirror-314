from django.db import models
from django.utils.timezone import now
from .managers import LogManager


class ApiCallLog(models.Model):
    # API URL that the user is trying to access
    url = models.TextField()
    # Response brief for success or error
    # Example: {"status": 200, "message": "Success"}
    # Use LogResponse.serialize() to serialize useful information
    message = models.JSONField(null=True, blank=True)
    # Active session when user is performing the action
    # For login and signup, session_id is None. Instead,
    # 'context' column will have 'user' key.
    status_code = models.IntegerField()
    session_id = models.UUIDField(null=True, blank=True)
    app_token_id = models.UUIDField(null=True, blank=True)
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'axor_api_call_logs'
        ordering = ['-created_at']

    objects = LogManager()

    def __str__(self):
        return 'ID ' + str(self.pk)
