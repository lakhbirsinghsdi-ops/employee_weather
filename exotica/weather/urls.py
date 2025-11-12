from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("signup",views.sign_up),
    path("login",views.log_in),

    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path("employee/del/<int:id>/", views.employee_delete, name="employee_delete"),
    path("employee/edit/<int:id>/", views.employee_edit, name="employee_edit    "),


]