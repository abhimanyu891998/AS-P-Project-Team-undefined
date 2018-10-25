from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Customer)
admin.site.register(models.Item)
admin.site.register(models.Cart)