from rest_framework import serializers
from uuid import uuid4

from .models import Car
from .tasks import load_image


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'model',
            'image_url',
        )

    def create(self, validated_data):
        image_url = validated_data.get('image_url')
        if image_url:
            validated_data['image_url'] = self._load_image(image_url)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        image_url = validated_data.get('image_url')
        if image_url:
            validated_data['image_url'] = self._load_image(image_url)

        return super().update(instance, validated_data)

    @staticmethod
    def _load_image(image_url):
        extension = image_url.split('.')[-1]
        file_name = '.'.join([str(uuid4()), extension])
        load_image.apply_async((file_name, image_url))

        return file_name
