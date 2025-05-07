from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    # product ID será o ID automático do Django
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}"

class Basket(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('completed', 'Completed'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='baskets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Basket #{self.id} - {self.customer.user.username} - {self.status}"
    
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def item_price(self):
        return self.product.price * self.quantity

class Purchase(models.Model):
    basket = models.OneToOneField(Basket, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Purchase #{self.id} - {self.basket.customer.user.username} - {self.purchase_date.strftime('%Y-%m-%d')}"
