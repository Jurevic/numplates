from rest_framework import serializers

from .models import NumPlate


class NumPlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumPlate
        fields = (
            'id',
            'number',
        )
