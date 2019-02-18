from django.contrib import admin

from.models import NumPlate


class NumPlateAdmin(admin.ModelAdmin):
    fields = ['number', 'owner', 'car']


admin.site.register(NumPlate, NumPlateAdmin)
