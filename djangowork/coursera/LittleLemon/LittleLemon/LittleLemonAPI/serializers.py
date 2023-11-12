from rest_framework import serializers #required to use serializers functions
from .models import MenuItem #imports the model

class MenuItemSerializer(serializers.ModelSerializer): #by inheriting from serializer class i get a lot of serialization logic for free, automaticaly generates serializers from underlying model
    class Meta: #meta class is used to specify meta data about serialization proccess
        model = MenuItem #specifys which model to base serializer on
        fields = ["id","title", 'price', 'inventory'] #specifies which fields to include