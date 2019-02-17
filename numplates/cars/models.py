from django.db import models


class Car(models.Model):
    model = models.CharField(null=False, max_length=100)
    image = models.ImageField(null=True)
