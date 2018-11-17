# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from . import models
from .models import *
from django.contrib.auth.admin import UserAdmin
from . models import User

admin.site.register(User, UserAdmin)


admin.site.register(Category)
admin.site.register(Item)
# admin.site.register(User)
admin.site.register(HospitalLocation)
admin.site.register(ClinicLocation)
admin.site.register(InterClinicDistance)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(ClinicManager)

