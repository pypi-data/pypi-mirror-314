import uuid

import bcrypt
from django.db import models
from django.utils.timezone import now

from .managers import UserManager


class User(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    password = models.CharField(max_length=150)
    email = models.CharField(
        max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    timezone = models.CharField(max_length=150, default='America/Vancouver')
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'axor_users'
        ordering = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.email

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.save()

    def check_password(self, password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except Exception as e:
            return False


class VerifyEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=now)
    is_consumed = models.BooleanField(default=False)

    class Meta:
        db_table = 'axor_user_verify_email'
        ordering = ['created_at']

    def __str__(self):
        return f"id:{self.pk}, {self.user}, {self.created_at} (consumed: {self.is_consumed})"
