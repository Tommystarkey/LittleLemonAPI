from django.urls import path, include #required to use path function
from rest_framework.routers import DefaultRouter
from . import views #imports from the view file 

router = DefaultRouter()
router.register(r'employee-list', views.EmployeeListViewSet)


### ALWAYS INCLUDE TRAILING SLASH TO AVOID HEADACHES ###
#//////////////////////////////////////////////////////#

urlpatterns = [
    # path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/', views.menu_items),
    #path function defines URL pattern for menuItems view
    
    path('menu-items/<int:id>/', views.single_item),
    #path function defines URL pattern for menuItems view,
    #with path converter that captures integer and stores it as id variable
    
    path('menu/', views.menu),
    #path function defines URL pattern for menu view

    path('welcome/', views.welcome),
    #path function defines URL pattern for welcome view

    path('employee-list/', views.EmployeeListViewSet.as_view({'get': 'list', 'post': 'create'})),
    #path function defines URL pattern for employeeList view,
    #as_view method call converts class based view to a function
    #indicates that GET and POST methods are allowed
   
    path('employee-list/<int:pk>/', views.EmployeeListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    #path function defines URL pattern for employeeList view,
    #with path converter that captures integer and stores it as pk variable
    #as_view method call converts class based view to a function
    #indicates that GET, PUT, PATCH and DELETE methods are allowed


    
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    #django framework expects a function based view, "as_view()" method is used to convert class based views to function based views
    #as_view inherits from the 'view' class which is a base class from django that doesn't require an import

]