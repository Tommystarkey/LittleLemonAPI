from rest_framework import generics #required for generic class based views
from .models import MenuItem #imports the model
from .serializers import MenuItemSerializer #imports the serializer

class MenuItemsView(generics.ListCreateAPIView): #defines class that inherits from generics class and its fuctionality
    queryset = MenuItem.objects.all() #the queryset is the list of objects that the view will operate on all ".all()" objects from that model
    serializer_class = MenuItemSerializer #specifies that the serializer should to used to convert "MenuItem" objects into suitable formats

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView): #defines class that inherits from generics class
    queryset = MenuItem.objects.all() #the queryset is the list of objects that the view will operate on all ".all()" objects from that model
    serializer_class = MenuItemSerializer  #specifies that the serializer should to used to convert "MenuItem" objects into suitable formats