from django.db import models


class NumPlate(models.Model):
    number = models.CharField(null=False, max_length=10)
