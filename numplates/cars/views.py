from rest_framework import viewsets

from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cars to be viewed or edited.
    """
    queryset = Car.objects.all().order_by('-id')
    serializer_class = CarSerializer
