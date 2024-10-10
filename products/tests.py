from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from . models import Product, Supplier

# Create your tests here.
class SupplierProductListTests(TestCase):
    
    def setUp(self):
        # Create supplier and products
        self.supplier_user = User.objects.create_user(username='supplier1', password='testpass')
        self.supplier = Supplier.objects.create(user=self.supplier_user, name='Supplier 1')

        #Create Cheaper products
        self.product1 = Product.objects.create(name="Product1", code="P001", price=50, supplier=self.supplier, in_stock=True)
        self.product2 = Product.objects.create(name="Product2", code="P002", price=30, supplier=self.supplier, in_stock=True)

        # Create another supplier and cheaper products
        self.other_supplier_user = User.objects.create(username='supplier2', password='testpass2')
        self.other_supplier = Supplier.objects.create(user=self.other_supplier_user, name='Supplier 2')
        self.cheaper_product = Product.objects.create(name="Cheaper Product", code="P002", price=25, supplier=self.other_supplier, in_stock=True)


    def test_supplier_can_access_own_products(self):
        self.client.login(username='supplier1', password='testpass')
        response = self.client.get(reverse('supplier_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product1') # Ensure product is in response
        self.assertContains(response, 'Product2')

    def test_cheaper_analogs_displayed(self):
        self.client.login(username='supplier1', password='testpass')
        response = self.client.get(reverse('supplier_product_list'))
        self.assertContains(response, 'Cheaper Product')  # Ensure cheaper analog appears

    def test_access_denied_to_buyers(self):
        buyer_user = User.objects.create_user(username='buyer1', password='testpass')
        self.client.login(username='buyer1', password='testpass')
        response = self.client.get(reverse('supplier_product_list')) 
        self.assertEqual(response.status_code, 403)  # Buyers should not access supplier products


class BuyerProductListTests(TestCase):
    def setUp(self):
        # Create a buyer user
        self.buyer_user = User.objects.create_user(username='buyer1', password='testpass')

        # Create suppliers and products
        self.supplier = Supplier.objects.create(user=User.objects.create_user(username='supplier1', password='testpass1'), name="Supplier 1")
        self.product1 = Product.objects.create(name="Product1", code="P001", price=50, supplier=self.supplier, in_stock=True)

        self.supplier2 = Supplier.objects.create(user=User.objects.create_user(username='supplier2', password='testpass2'), name="Supplier 2")
        self.product2 = Product.objects.create(name="Product2", code="P002", price=30, supplier=self.supplier2, in_stock=True)
    
    def test_buyer_can_access_product_list(self):
        self.client.login(username='buyer1', password='testpass')
        response = self.client.get(reverse('buyer_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product1')
        self.assertContains(response, 'Product2')
    
    def test_access_denied_to_suppliers(self):
        self.client.login(username='supplier1', password='testpass1')
        response = self.client.get(reverse('buyer_product_list'))
        self.assertEqual(response.status_code, 403)  # Suppliers should not access buyer products
    
class AccessControlTests(TestCase):
    def test_login_required_for_buyer_product_list(self):
        response = self.client.get(reverse('buyer_product_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('buyer_product_list')}") # Check if redirect to login
    
    def test_login_required_for_supplier_product_list(self):
        response = self.client.get(reverse('supplier_product_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('supplier_product_list')}")  # Check if redirect to login

class ProductModelTests(TestCase):
    def test_product_creation(self):
        supplier = Supplier.objects.create(name='Supplier 1', user=User.objects.create_user(username='supplier', password='testpass'))
        product = Product.objects.create(name="Product1", code="P001", price=100, supplier=supplier, in_stock=True)
        self.assertEqual(str(product), "Product1")  # Check if product name is correct