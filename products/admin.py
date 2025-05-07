from django.contrib import admin
from .models import Product, Customer, Basket, BasketItem, Purchase

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'address')
    search_fields = ('user__username', 'user__email', 'phone')

class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('customer__user__username',)
    inlines = [BasketItemInline]

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'product', 'quantity')
    list_filter = ('basket__status',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'purchase_date', 'total_amount')
    list_filter = ('purchase_date',)
    search_fields = ('basket__customer__user__username',)
