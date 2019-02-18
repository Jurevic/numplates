from django.contrib import admin

from.models import Car


class CarAdmin(admin.ModelAdmin):
    fields = ['model', 'image_url']


admin.site.register(Car, CarAdmin)
