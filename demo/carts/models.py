from django.db import models


# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField()
    status = models.CharField(max_length=10)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'{self.time} ({self.status})'
