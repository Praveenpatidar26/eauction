from django.db import models

# Create your models here.
class Category(models.Model):
    Category_ID=models.AutoField(primary_key=True)
    Category_name=models.CharField(max_length=30,unique=True)
    Category_file=models.CharField(max_length=100)

class SubCategory(models.Model):
    SubCategory_ID=models.AutoField(primary_key=True)
    Category_name=models.CharField(max_length=30)
    SubCategory_name=models.CharField(max_length=30,unique=True)
    SubCategory_file=models.CharField(max_length=100)