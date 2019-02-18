from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
import os
from urllib import request, error


@shared_task(name='load_car_image')
def load_image(name, url):
    file_name = os.path.join(
        settings.MEDIA_ROOT,
        str(name) + '.' + url.split('.')[-1],
    )
    try:
        request.urlretrieve(url, file_name)
    except error.HTTPError:
        # Image cannot be downloaded, skip it
        pass
