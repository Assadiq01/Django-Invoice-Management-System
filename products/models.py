from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.full_name

class Product(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    title = models.TextField(max_length=200, null=True, default = None)
    date_created = models.DateField(null=True, blank=True)
    total = models.PositiveIntegerField(default=1)
    sub_total = models.PositiveIntegerField(default=1)
    deposit = models.PositiveIntegerField(default=1)
    balance1 = models.PositiveIntegerField(default=1)
    balance2 = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to='images', null=True)

    def __str__(self):
        return self.product.title

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(max_length=200)
    rate = models.DecimalField(max_length=12, decimal_places=2, max_digits = 12, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.product.description
