from rest_framework import serializers

from .models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = (
            'id',
            'first_name',
            'last_name',
        )

    def validate_first_name(self, value):
        if not str(value)[0].isupper():
            raise serializers.ValidationError(
                'First name should start with a capital letter'
            )

        return value

    def validate_last_name(self, value):
        if not str(value)[0].isupper():
            raise serializers.ValidationError(
                'Last name should start with a capital letter'
            )

        return value
