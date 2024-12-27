from django.contrib import admin
from .models import Product, Review, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'condition', 'seller', 'created_at']
    list_filter = ['category', 'condition']
    search_fields = ['name', 'description']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['created_at', 'rating']
    search_fields = ['user__username', 'product__name', 'content']
