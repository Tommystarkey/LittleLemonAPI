from django.urls import path, include #required to use path function
from rest_framework.routers import DefaultRouter
from . import views #imports from the view file 

router = DefaultRouter()
router.register(r'employee-list', views.EmployeeListViewSet)

urlpatterns = [
    # path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/', views.menu_items),
    path('menu-items/<int:id>/', views.single_item),
    path('employee-list/', views.EmployeeListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('employee-list/<int:pk>/', views.EmployeeListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
 
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    #django framework expects a function based view, "as_view()" method is used to convert class based views to function based views
    #as_view inherits from the 'view' class which is a base class from django that doesn't require an import

]