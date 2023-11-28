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
    #defines price after tax field "SerializerMethodField" allows inclusion of custom methods in serializers
    #(method_name= 'calculate_tax') specifys the method
    category = CategorySerializer(read_only=True)
    #defines category field, which is a read only field
    #includes the categorySerializer felds in the MenuItemSerializer fields
    #basiacally it display one table inside another
    category_id = serializers.IntegerField(write_only=True)
    #defines category_id field that is only used for deserialisation, such as creating and updating objects
    class Meta:
    #meta class is used to specify meta data about serialization proccess
        model = MenuItem
        #specifys which model to base serializer on
        fields = ["id", "title", 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        #specifies which fields to include

    
    def calculate_tax(self, product:MenuItem):
    #defines calculate tax method
    #selfreferences instance of the class
    #product:MenuItem is a type hint indicating product is of type MenuItem but is not essential
        return round(product.price * Decimal(1.1), 2)
        #product.price accesses the price atribute of the product object
        #Decimal(1.1) creates a decimal object with the value of 1.1
        #using decimal avoids some errors than arise from floating point numbers due to binary arithmatic
    

class EmployeeListSerializer(serializers.ModelSerializer):
#'Modelserializer is a class that automatically generates serializers so you have to write less code
    class Meta:
    #specifies the metadata about the serialization progress
        model = EmployeeList
        #specifies what model the serializer is based on
        fields = ['id', 'name', 'age', 'job_title']
        #defines what fields should be included in the output