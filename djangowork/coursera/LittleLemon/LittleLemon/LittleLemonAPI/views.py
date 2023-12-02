from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from . models import MenuItem, EmployeeList, Category
from . serializers import MenuItemSerializer, CategorySerializer
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework_csv.renderers import CSVRenderer


from rest_framework import viewsets
from . serializers import EmployeeListSerializer


@api_view(['GET', 'POST'])
# @renderer_classes([CSVRenderer])
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
        
        category_name = request.query_params.get('category')
        #This line retrieves the value of the 'category' parameter from the request's query parameters.
        #uses the query_params attribute of the request object to access the query parameters from a GET request
        #The get method is then used to retrieve the value of a specific parameter
        to_price = request.query_params.get('to_price')
        #retrieves the value of the 'to_price' parameter from the request's query parameters
        #The get method is used, and the value is assigned to the to_price variable
        search = request.query_params.get('search')
        #retrieves the value of the 'search' parameter from the request's query parameters
        #The get method is used, and the value is assigned to the search variable as an argument.
        if category_name:
            #checks that the 'category' parameter was present in the request.
            items = items.filter(category__title=category_name)
            #.filter is a method from django ORM
            # double underscore is used to traverse relationships
        if to_price:
            #checks that the 'to_price' parameter was present in the request.
            items = items.filter(price__lte=to_price)
            #.filter is a method from django ORM
            #lte = less then or equal to
        if search:
            #checks that the 'search' parameter was present in the request.
            items = items.filter(title__istartswith=search)
            #.filter is a method from django ORM
            #can use " (title__icontains=search) " to seach if the string is anywhere in the title
            #remove the " i " to make the search case sensative            
        
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
        #returns response with the serialized data and a HTTP status code



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


@api_view()
#decorator from DRF that converts a regular function-based view into an API view
@renderer_classes ([TemplateHTMLRenderer])
#decorator that specifies the renderer classes to be used for rendering the response.
#TemplateHTMLRenderer indicatesthe response should be rendered as HTML
def menu(request):
#main function for the view which takes a django request object as a parameter
    items = MenuItem.objects.select_related('category').all()
    #queries the data base for all MenuItem objects and stores them in "items" variable
    serialized_item = MenuItemSerializer(items, many=True)
    #serializes the retrieved MenuItem objects
    #many=Trueindicates the serializer should handle multiple objects
    return Response({'data':serialized_item.data}, template_name='menu-item.html')
    #{'data': serialized_item.data} is a dictionary where the key is 'data',
    #and the value is the serialized representation of the data obtained from the serialized_item.data attribute. 
    #template_name='menu-item.html specifies the HTML template to use to display the data

@api_view(['GET'])
#decorator that specifies the accepted HTTP mehods for the view
@renderer_classes([StaticHTMLRenderer])
#decorator indicating the renderer classes to be used for the response
def welcome(request):
#main function for the view that takes adjango request as a parameter
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></boy></html>'
    #creates a simple HTML string and stores it in data variable
    return Response(data)
    #returns HTTP response with the data HTML string



#class based view does not require 'api_view' decorator
class EmployeeListViewSet(viewsets.ModelViewSet):
    #inherits from viewsets.modelviewset
    queryset = EmployeeList.objects.all()
    #'queryset specifys which instances of the model are availible for this view
    serializer_class = EmployeeListSerializer
    #specifies which serializer to use


