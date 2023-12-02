from django.db import models #imports models module from django database

# Create your models here.

# python manage.py shell
# from LittleLemonAPI.models import Category, MenuItem, EmployeeList
# all_menu_items = MenuItem.objects.all()
# for menu_item in all_menu_items:
    # print(
    #     menu_item.title,
    #     menu_item.price,
    #     menu_item.inventory,
    #     menu_item.category
    # )

###must be entered one line at a time with proper indentation ###



class Category(models.Model):
# creates new class that inherits from models.models
    slug = models.SlugField()
    #defines a field for storing slugs
    title = models.CharField(max_length=255)
    #defines a field for storing models

    def __str__(self)-> str:
        return self.title
    #when you convert an instance of the Category model to a string
    #using str() or print(),
    # the result should be the value of the title attribute.



class MenuItem(models.Model):
#defines a class that inherits from the "models.Model" class
    #defines fields of class MenuItem
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1) # 
    #defines model.ForeignKey arguments, the related model, on_DELETE and the default value

class EmployeeList(models.Model):

    
    JOB_CHOICES = [
        ('bar', 'bar'),
        ('floor', 'floor' ),
        ('manager', 'manager'),
        #establishes choices list
        #defined as key value pairs,
        #first value stored in the database
        #second value is the human readable representation for the view/endpoint

    ]
    #defines fields of class EmployeeList
    name = models.CharField(max_length=255)
    age = models.DecimalField(max_digits=2,decimal_places=0)
    job_title = models.CharField(max_length=10, choices=JOB_CHOICES)
    #defines choices option for job_title field