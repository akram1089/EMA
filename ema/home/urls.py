from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

employee_list = EmployeeViewSet.as_view({
    'get': 'list',        # GET all employees
    'post': 'create'      # POST (create) a new employee
})

employee_detail = EmployeeViewSet.as_view({
    'get': 'retrieve',    # GET a single employee by ID
    'put': 'update',      # PUT (update) an existing employee
    'delete': 'destroy'   # DELETE an employee
})

urlpatterns = [

]

urlpatterns = [
    path('', views.home,name="home"),
    path('all_emp', views.all_emp,name="all_emp"),
    path('api/employees/', employee_list, name="employee-list"),
    path('api/employees/<int:pk>/', employee_detail, name="employee-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


