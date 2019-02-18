from rest_framework import serializers
import re

from .models import NumPlate


class NumPlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumPlate
        fields = (
            'id',
            'number',
            'owner',
            'car',
        )

    def validate_number(self, value):
        if not re.match(r'^[A-Z]{3}[0-9]{3}$', value):
            raise serializers.ValidationError(
                'Invalid Lithuanian car number, valid format is "AAA000"'
            )

        return value
