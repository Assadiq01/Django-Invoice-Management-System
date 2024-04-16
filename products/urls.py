from django.urls import path

from .views import (
    ProductCreate,
    delete_image, delete_variant,
    create_customer, customer_detail, 
    customer_list,
    customer_product_list,
    product_detail, delete_product,
    EditCustomerProductsView
)

app_name = 'products'  # 3rd

urlpatterns = [
    path('customers/', customer_list, name='customer_list'),
    path('create-customer/', create_customer, name='create_customer'),
    path('customers/<int:customer_id>/', customer_detail, name='customer_details'),

    path('customer_products/<int:customer_id>/', customer_product_list, name='customer_product_list'),
    path('create_product/<int:customer_id>/', ProductCreate.as_view(), name='create_product'),
    path('edit_customer_products/<int:pk>/', EditCustomerProductsView.as_view(), name='edit_customer_products'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
    path('<int:pk>/delete/', delete_product, name='delete_product'),
]
 