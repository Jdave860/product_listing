from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    class Meta:
        unique_together = ('supplier', 'code')  # Ensures unique product code per supplier

    def __str__(self):
        return self.name
