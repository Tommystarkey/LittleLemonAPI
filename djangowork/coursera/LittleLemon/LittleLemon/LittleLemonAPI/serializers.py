from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
#required to use serializers functions
from .models import EmployeeList, MenuItem, Category
from decimal import Decimal
import bleach

class CategorySerializer(serializers.ModelSerializer):
#defines Categoryserializer class that inherits from serializers.ModelSerializer
    class Meta:
    # defines the metadata
        model = Category
        #links to category model
        fields = ['id', 'slug', 'title']
        #defines the which fields to include

class MenuItemSerializer(serializers.ModelSerializer):
#defines MenuItemSerializer class that inherits from serializers.ModelSerializer
    stock = serializers.IntegerField(source='inventory')
    #creates new field and links it to an existing field with the scource argument
    price_after_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    #defines price after tax field "SerializerMethodField" allows inclusion of custom methods in serializers
    #(method_name= 'calculate_tax') specifys the method
    category = CategorySerializer(read_only=True)
    #defines category field, which is a read only field
    #includes the categorySerializer felds in the MenuItemSerializer fields
    #basically it display one table inside another
    category_id = serializers.IntegerField(write_only=True)
    #defines category_id field that is only used for deserialisation, such as creating and updating objects
    def validate(self, attrs):
        #attrs is a dictionary containing all the attributes (fields) that are being deserialized.
        #It represents the raw data received for the serializer.
        attrs['title'] = bleach.clean(attrs['title'])
        #sanitizes the 'title' attribute using bleach.clean. It ensures that the 'title' is cleaned from potentially harmful HTML content.
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
            #specifies that the minimum value for price should be 2
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
            #indicates the 'stock' field should get its value from the models 'inventory' field, minimum value = 0

        # Custom unique validation for 'title'
        existing_titles = MenuItem.objects.exclude(id=attrs.get('id')).filter(title=attrs['title'])
        #"MenuItem.objects" is the manager for the MenuItem model. The objects manager is the default manager created for every Django model, allowing you to perform queries on the database.
        #"exclude(id=attrs.get('id'))" excludes objects where the id is equal to the id attribute of the current instance being validated. This is crucial when updating an existing object because you don't want to consider the current object in the uniqueness check.
        #filters objects where the title is equal to the title attribute of the current instance being validated. This checks if there are other objects in the database with the same title
        if existing_titles.exists():
        # There are existing titles, meaning the title is not unique
            raise serializers.ValidationError('Title must be unique')
        
        return super().validate(attrs)
        #the super() function is used to call a method or access an attribute from the parent (or superclass) of a class
        #super().validate(attrs): Calls the validate method of the immediate superclass (serializers.ModelSerializer).
        #serializers.ModelSerializer internally calls the validate method of its superclass (serializers.Serializer).

    class Meta:
    #meta class is used to specify meta data about serialization proccess
        model = MenuItem
        #specifys which model to base serializer on
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        # #specifies which fields to include
    
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
    def validate_name(self, value):
    #defines function that takes self and value as a parameter
    #DRF naming convention requires "validate_<specific_field>" to specify field to be validated
        return bleach.clean(value)
        #returns the result of bleach.clean function that is applied to the input value
    
    class Meta:
    #specifies the metadata about the serialization progress
        model = EmployeeList
        #specifies what model the serializer is based on
        fields = ['id', 'name', 'age', 'job_title']
        #defines what fields should be included in the output
        validators = [
        #the singular UniqueValidator goes inside extra kwargs
            UniqueTogetherValidator(
            #This validator is used to ensure unique combinations of fields within the specified queryset.
                queryset=EmployeeList.objects.all(),
                #queryset argument to determine the scope of the uniqueness when validating the field
                fields=['id', 'name']
                #specifies the fields to apply UniqueTogetherValidator to
                ),
                ]
        extra_kwargs = {
        #atribute provide additional options for certain fields
        'age': {'min_value':0},
        #specifies that the minimum value for age should be02

        }