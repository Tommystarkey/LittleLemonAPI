from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from . models import MenuItem, EmployeeList
from . serializers import MenuItemSerializer
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from django.core.paginator import Paginator, EmptyPage


from rest_framework import viewsets
from . serializers import EmployeeListSerializer

class MenuItemsViewSet(viewsets.ModelViewSet):
#defines class as a subclass of 'viewsets.ModelViewSet', a base class that provides CRUD operations 
    queryset = MenuItem.objects.all().order_by('id')
    #queryset: This attribute defines the initial queryset of 'MenuItem' objects that will be used by the view.
    #In this case, it fetches all 'MenuItem' objects and orders them by their id.
    serializer_class = MenuItemSerializer
    #specifies the serializer class that should be used to convert MenuItem instances to and from JSON.
    ordering_fields=['price', 'inventory']
    #specifies the fields on which the queryset can be ordered.
    search_fields=['title', 'category__title']
    #defines the fields on which the view can perform a search.
    #The default lookup_field value for searching in DRF is icontains, which is case insensitive

    #pagination for viewsets is dealt with in settings.py file


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
        #'request' is an object of class HttpRequest
        #'query_params' is an attribute of 'request' object that holds the query parameters
        #'.get('category')' This is a method call on the dictionary-like object request.query_params.
        #'category_name' is assigned the value of the 'category' parameter from the query parameters of the HTTP request.
        to_price = request.query_params.get('to_price')
        #'request' is an object of class HttpRequest
        #'query_params' is an attribute of 'request' object that holds the query parameters
        #'.get('to_price')' This is a method call on the dictionary-like object request.query_params.
        #'to_price' is assigned the value of the 'to_price' parameter from the query parameters of the HTTP request.
        search = request.query_params.get('search')
        #'request' is an object of class HttpRequest
        #'query_params' is an attribute of 'request' object that holds the query parameters
        #'.get('search')' This is a method call on the dictionary-like object request.query_params.
        #'to_price' is assigned the value of the 'search' parameter from the query parameters of the HTTP request.
        ordering = request.query_params.get('ordering')
        #'request' is an object of class HttpRequest
        #'query_params' is an attribute of 'request' object that holds the query parameters
        #'.get('ordering')' This is a method call on the dictionary-like object request.query_params.
        #'ordering' is assigned the value of the 'ordering' parameter from the query parameters of the HTTP request.
        perpage = request.query_params.get('perpage', default=2)
        #These lines retrieve the values of the perpage and page query parameters from the request.
        page = request.query_params.get('page', default=1)
        #If the parameter is not present in the request, it defaults to the specified values (2 for perpage and 1 for page).

        ###filterers###   
        if category_name:
            #checks that the 'category' parameter was present in the request.
            items = items.filter(category__title=category_name)
            #ilters the 'items' queryset to include only items whose related category's title matches the 'category_name'   "/?category=SomeCategory"       
            #.filter is a method from django ORM
            # double underscore is used to traverse relationships
        if to_price:
        #checks that the 'to_price' parameter was present in the request.
            items = items.filter(price__lte=to_price)
            #filters the 'items' queryset to include only items with a price less than or equal to the specified 'to_price  "/?to_price=50"
            #.filter is a method from django ORM
            #lte = less then or equal to  
        if search:
            #checks that the 'search' parameter was present in the request.
            items = items.filter(title__istartswith=search)
            #filters the 'items' queryset to include only items whose title starts with the specified 'search' string   "/?search=SomeTitle"
            #.filter is a method from django ORM
            #can use " (title__icontains=search) " to seach if the string is anywhere in the title
            #remove the " i " to make the search case sensative

        ###orderer###
        if ordering:
        #checks that the 'ordering' parameter was present in the request.
            items = items.order_by(ordering)  
            #orders by price    "/?ordering=price"
            #items: This is the queryset of MenuItem objects that has been filtered based on various conditions earlier in the code.
            #.order_by(ordering): This is a method provided by Django's ORM that is used to specify the ordering of the queryset

        paginator = Paginator(items,per_page=perpage)
        #initializes paginator object that takes "items" and per_page as args
        try:
            items = paginator.page(number=page)
            #The try block is used to catch any exceptions that might be raised during the attempt.
            #If the requested page is within the valid range (i.e., it exists), the items variable is updated to contain the items on the specified page
        except EmptyPage:
        #If the requested page is beyond the available pages (i.e., it's an empty page), it raises an EmptyPage exception.
            items = []
            #When the items array is empty due to the EmptyPage exception being caught
            #the subsequent code that initializes the Paginator object will use the default values for perpage and page
        
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


