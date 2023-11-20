from rest_framework import serializers
#required to use serializers functions
from .models import EmployeeList, MenuItem, Category
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):#defines serializer class
    class Meta: # defines the metadata
        model = Category #links to category model
        fields = ['id', 'slug', 'title'] #defines the fields

class MenuItemSerializer(serializers.ModelSerializer):
    #by inheriting from serializer class you get a lot of serialization logic for free
    # automaticaly generates serializers from underlying model
    stock = serializers.IntegerField(source='inventory')
    #creates new field and links it to an existing field with the scource argument
    price_after_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
    #meta class is used to specify meta data about serialization proccess
        model = MenuItem
        #specifys which model to base serializer on
        fields = ["id", "title", 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        #specifies which fields to include

    
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)


class EmployeeListSerializer(serializers.ModelSerializer):
#'Modelserializer is a class that automatically generates serializers so you have to write less code
    class Meta:
    #specifies the metadata about the serialization progress
        model = EmployeeList
        #specifies what model the serializer is based on
        fields = ['id', 'name', 'age', 'job_title']
        #defines what fields should be included in the output