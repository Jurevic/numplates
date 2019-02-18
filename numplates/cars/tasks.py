from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
import os
from urllib import request, error


@shared_task(name='load_car_image')
def load_image(file_name, url):
    absolute_path = os.path.join(
        settings.MEDIA_ROOT,
        file_name,
    )
    try:
        request.urlretrieve(url, absolute_path)
    except error.HTTPError:
        # Image cannot be downloaded, skip it
        pass
