from django.db import models

# Create your models here.

class Product(models.Model):
    # product ID será o ID automático do Django
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
