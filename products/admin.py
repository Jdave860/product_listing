from django.contrib import admin
from .models import Product, Supplier

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'supplier', 'price', 'in_stock')  # Fields to display in the list
    search_fields = ('name', 'supplier__name')  # Fields for search functionality
    list_filter = ('in_stock', 'supplier')  # Filters for the sidebar
    ordering = ('supplier', 'name') 

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  # Display these fields for Supplier
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier, SupplierAdmin)