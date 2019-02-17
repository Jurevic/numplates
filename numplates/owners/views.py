from rest_framework import viewsets

from .models import Owner
from .serializers import OwnerSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows number plate owners to be viewed or edited.
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
