from rest_framework import viewsets

from .models import NumPlate
from .serializers import NumPlateSerializer


class NumPlateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows number plates to be viewed or edited.
    """
    queryset = NumPlate.objects.all().order_by('-id')
    serializer_class = NumPlateSerializer
