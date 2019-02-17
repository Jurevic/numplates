from django.db import models

from numplates.cars.models import Car
from numplates.owners.models import Owner


class NumPlate(models.Model):
    number = models.CharField(null=False, max_length=10, unique=True)

    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True)

    car = models.ForeignKey(Car, on_delete=models.PROTECT, null=True)
