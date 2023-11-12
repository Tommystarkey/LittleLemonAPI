from django.db import models #imports models module from django database

# Create your models here.

class MenuItem(models.Model): #defines a class that inherits from the "models.Model" class
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()