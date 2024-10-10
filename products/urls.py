from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('buyer/products/', views.buyer_product_list, name='buyer_product_list'),
    path('supplier/products/', views.supplier_product_list, name='supplier_product_list'),
]
