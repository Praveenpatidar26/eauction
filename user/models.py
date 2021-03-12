from django.db import models

# # Create your models here.
class Products(models.Model):
    Product_ID=models.AutoField(primary_key=True)
    Title=models.CharField(max_length=20)
    Category=models.CharField(max_length=10)
    SubCategory_name=models.CharField(max_length=10)
    Base_price=models.IntegerField()
    Description=models.CharField(max_length=100)
    Pic1=models.CharField(max_length=50)
    Pic2=models.CharField(max_length=50)
    Pic3=models.CharField(max_length=50)
    Pic4=models.CharField(max_length=50)
    User_ID=models.CharField(max_length=50)
    UStatus=models.IntegerField()
    Date=models.CharField(max_length=50)


class Payment(models.Model):
    Payment_ID=models.AutoField(primary_key=True)
    Product_ID=models.IntegerField()
    price=models.IntegerField()
    Uid=models.CharField(max_length=50)
    dt=models.CharField(max_length=30)