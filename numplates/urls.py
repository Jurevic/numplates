"""numplates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework import routers

from numplates.cars import views as car_views
from numplates.numplates import views as num_plate_views
from numplates.owners import views as owner_views


router = routers.DefaultRouter()
router.register(r'cars', car_views.CarViewSet)
router.register(r'numplates', num_plate_views.NumPlateViewSet)
router.register(r'owners', owner_views.OwnerViewSet)

urlpatterns = [
    path('', lambda request: redirect('/api/v1/')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
