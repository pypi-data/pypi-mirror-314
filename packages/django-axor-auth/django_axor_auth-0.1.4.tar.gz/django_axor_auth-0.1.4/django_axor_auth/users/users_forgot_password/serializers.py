from django.utils.encoding import force_str
from rest_framework import serializers
from .models import ForgotPassword
from .utils import hash_this


class HealthyForgotPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        err = 'Link or instance is no longer valid. Please request a new one.'
        # Check if key is provided
        if 'token' not in data:
            raise serializers.ValidationError('Token is not present.')
        try:
            fp = ForgotPassword.objects.select_related('user').get(token=hash_this(force_str(data['token'])))
            # Check if fp is valid
            if not fp.check_valid():
                raise serializers.ValidationError(err)
        except ForgotPassword.DoesNotExist:
            raise serializers.ValidationError(err)
        return fp
