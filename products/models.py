from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)