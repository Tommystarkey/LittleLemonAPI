from django.urls import path #required to use path function
from . import views #imports from the view file 

urlpatterns = [
    path('menu-items/', views.MenuItemsView.as_view()), 
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    #django framework expects a function based view, "as_view()" method is used to convert class based views to function based views
    #as_view inherits from the 'view' class which is a base class from django that doesn't require an import

]