from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . models import MenuItem, EmployeeList, Category
from . serializers import MenuItemSerializer, CategorySerializer
from rest_framework import status

from rest_framework import viewsets
from . serializers import EmployeeListSerializer


@api_view(['GET'])
def menu_items(request):
    #item and serialized item are variables
    if request.method == 'GET':
    #when client makes URL request, django proccesses request and creates HttpRequest object
    #which is passed as a parameter to the view function
    # the boolean checks if request.method attribute contains HTTP methods used in the request is == 'GET
        items = MenuItem.objects.select_related('category').all()
        ###this line querys the database###
        #specifies model
        ##object is a a manager responsible for database queries
        #select_related is used to perform SQL join to retrieve related category objects
        #.all() fetches all MenuItems from the database 
        #stores queried objects in items variable      
        serialized_item = MenuItemSerializer(items, many=True)
        ###this line serializes the queried MenuItem objects###
        #creates an instance of MenuItemSerializer and initializes it with the quieried menu_items objects (items)
        #many=True,indicates that you are serializing multiple objects (a queryset)        
        return Response(serialized_item.data)
        #returns the serialized data###
        #.data is where the serialized data is stored
       
    if request.method == 'POST':
    #when client makes URL request, django proccesses request and creates HttpRequest object
    #which is passed as a parameter to the view function
    # the boolean checks if request.method attribute contains HTTP methods used in the request is == 'POST'
        serialized_item = MenuItemSerializer(data=request.data)
        #creates an instance of the MenuItemSerializer and initializes it with the incoming request
        serialized_item.is_valid(raise_exception=True)
        #is_valid mehod calls on the serializer to check if the data provided is valid,
        #if its not valid an error is raised thanks to "raise_exception=True"
        serialized_item.save()
        #saves the serialized data to the database
        #he save method is responsible for creating a new instance of the model or updating an existing one with the serialized data.
        return Response(serialized_item.data, status.HTTP_201_CREATED)
        #returns response woth the serialized data and a HTTP status code



@api_view(['GET', 'POST'])
#decorator is used to define function based view that can handle HTTP methods
def single_item(request, id):
    #defines single_item view that takes a request object with an id parameter
    item = get_object_or_404(MenuItem,pk=id)
    #used to retrieve a single instance of menuitem
    serialized_item = MenuItemSerializer(item)
    #specifies what serializer to use with item is a parameter
    return Response(serialized_item.data)
    #'serialized_item.data' represents serialized form of menuitem in a suitible format ie 'JSON'



#class based view does not require 'api_view' decorator
class EmployeeListViewSet(viewsets.ModelViewSet):
    #inherits from viewsets.modelviewset
    queryset = EmployeeList.objects.all()
    #'queryset specifys which instances of the model are availible for this view
    serializer_class = EmployeeListSerializer
    #specifies which serializer to use


