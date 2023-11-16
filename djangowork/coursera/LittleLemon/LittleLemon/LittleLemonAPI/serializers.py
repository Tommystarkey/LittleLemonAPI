from rest_framework import serializers #required to use serializers functions
# from .models import MenuItem #imports the model
from .models import EmployeeList

# class MenuItemSerializer(serializers.ModelSerializer): #by inheriting from serializer class i get a lot of serialization logic for free, automaticaly generates serializers from underlying model
#     class Meta: #meta class is used to specify meta data about serialization proccess
#         model = MenuItem #specifys which model to base serializer on
#         fields = ["id","title", 'price', 'inventory'] #specifies which fields to include

class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()

class EmployeeListSerializer(serializers.ModelSerializer):#'Modelserializer is a class that automatically generates serializers so you have to write less code
    class Meta:#specifies the metadata about the serialization progress
        model = EmployeeList#specifies what model the serializer is based on
        fields = ['id', 'name', 'age', 'job_title']#defines what fields should be included in the output