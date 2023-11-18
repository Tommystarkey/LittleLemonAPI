# from rest_framework import generics #required for generic class based views
# from .models import MenuItem #imports the model
# from .serializers import MenuItemSerializer #imports the serializer

# class MenuItemsView(generics.ListCreateAPIView): #defines class that inherits from generics class and its fuctionality
#     queryset = MenuItem.objects.all() #the queryset is the list of objects that the view will operate on all ".all()" objects from that model
#     serializer_class = MenuItemSerializer #specifies that the serializer should to used to convert "MenuItem" objects into suitable formats

# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView): #defines class that inherits from generics class
#     queryset = MenuItem.objects.all() #the queryset is the list of objects that the view will operate on all ".all()" objects from that model
#     serializer_class = MenuItemSerializer  #specifies that the serializer should to used to convert "MenuItem" objects into suitable formats

from rest_framework.response import Response
from rest_framework.decorators import api_view
from . models import MenuItem, EmployeeList, Category
from . serializers import MenuItemSerializer, EmployeeListSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

@api_view(['GET'])
def menu_items(request):
    #item and serialized item are variables
    items = MenuItem.objects.select_related('category').all()
    #specifies model
    ##object is a a manager responsible for database queries
    #select_related allows access to related models
    serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
    #specifies the correct serializer
    #many=True,indicates that you are serializing multiple objects (a queryset)
    #context part passes the URLpattern to the serializer required for the hyperlink to work
    return Response(serialized_item.data)#returns the serialized data,
    #'serialized_item.data' represents serialized form of menuitem in a suitible format ie 'JSON'

@api_view(['GET'])
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


