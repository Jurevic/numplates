from django.conf import settings
from rest_framework import serializers
from uuid import uuid4

from .models import Car
from .tasks import load_image


class MediaImageField(serializers.URLField):
    def to_representation(self, value):
        return settings.BASE_URL + settings.MEDIA_URL + value


class CarSerializer(serializers.ModelSerializer):
    image_url = MediaImageField(required=False)

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
