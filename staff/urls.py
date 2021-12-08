from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [path('', login_required(views.EmployeesListView.as_view()), name='employees_list'),
path('add', login_required(views.EmployeesCreatorView.as_view()), name='employee_creator'),]