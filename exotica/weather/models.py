from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    phone_number = models.CharField(max_length=15,null=True)  
    password=models.CharField(max_length=15)
    designation=models.CharField(max_length=20,default="Developer")
    salary = models.DecimalField(max_digits=10,decimal_places=1,default=10000) 
