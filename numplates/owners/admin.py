from django.contrib import admin

from.models import Owner


class OwnerAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name']


admin.site.register(Owner, OwnerAdmin)
