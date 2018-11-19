# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.
#
#
def image_path(instance, filename):
    return os.path.join("img", "itemImages", filename)
class User(AbstractUser):
    CLINIC_MANAGER = 1
    WAREHOUSE_PERSONNEL = 2
    DISPATCHER = 3
    ADMIN = 4
    DEF_USER = 5
    ROLE_CHOICES = (
        (CLINIC_MANAGER, 'CM'),
        (WAREHOUSE_PERSONNEL, 'WP'),
        (DISPATCHER, 'DI'),
        (ADMIN, 'AD'),
    )
    name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(unique=True, max_length=200)
    email = models.EmailField(max_length=254, unique=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True)
    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return str(self.name)
class HospitalLocation(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)
class ClinicLocation(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)
    supplying_hospital = models.ForeignKey(HospitalLocation, on_delete=models.CASCADE, null=True)
    distance_from_supplying_hospital = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return str(self.name)
class InterClinicDistance(models.Model):
    location_a = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, null=True, related_name='location_a')
    location_b = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, null=True, related_name='location_b')
    distance = models.DecimalField(max_digits=4, decimal_places=2)
    def get_distance(a, b):
        return 0
class ClinicManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, null=True, blank=True)
# class User(models.Model):
#     name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200, blank=True)
#     email = models.EmailField(max_length=254, unique=True)
#     password = models.CharField(max_length=200)
#     ROLE_CHOICES = (
#         ('CLINIC_MANAGER', 'Clinic Manager'),
#         ('WAREHOUSE_PERSONNEL', 'Warehouse Personnel'),
#         ('DISPATCHER', 'Dispatcher'),
#     )
#     role = models.CharField(max_length=200,choices=ROLE_CHOICES,default='CLINIC_MANAGER')
#     # clinic_location = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, null=True)
#     def __str__(self):
#         return self.name
class Order(models.Model):
    total_weight = models.DecimalField(max_digits=5, decimal_places=2)
    STATUS_CHOICES = (
        ('QUEUED_FOR_PROCESSING', 'Queued for Processing'),
        ('PROCESSING_BY_WAREHOUSE', 'Processing by Warehouse'),
        ('QUEUED_FOR_DISPATCH', 'Queued for Dispatch'),
        ('DISPATCHED', 'Dispatched')
    )
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='QUEUED_FOR_PROCESSING')
    PRIORITIES = (
        ('1', 'High'),
        ('0', 'Medium'),
        ('-1', 'Low')
    )
    priority = models.CharField(max_length=200, choices=PRIORITIES, default=-1)
    dateOrdered = models.DateTimeField(default=datetime.now, blank=True)
    dateProcessed = models.DateTimeField(null=True, blank=True)
    dateDispatched = models.DateTimeField(null=True, blank=True)
    dateDelivered = models.DateTimeField(null=True, blank=True)
    ordering_clinic = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, null=True)
    supplying_hospital = models.ForeignKey(HospitalLocation, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Item, through='OrderedItem')
    def __str__(self):
        return 'Order Id: ' + str(self.pk)
class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)