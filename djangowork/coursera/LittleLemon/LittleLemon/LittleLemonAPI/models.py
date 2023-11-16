from django.db import models #imports models module from django database

# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self)-> str:
        return self.title

class MenuItem(models.Model): #defines a class that inherits from the "models.Model" class
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

class EmployeeList(models.Model):
    JOB_CHOICES = [
        ('bar', 'bar'),
        ('floor', 'floor' ),
        ('manager', 'manager'),
    ]
    name = models.CharField(max_length=255)
    age = models.DecimalField(max_digits=2,decimal_places=0)
    job_title = models.CharField(max_length=10, choices=JOB_CHOICES)