from django.db import models

from customer.models import Customer


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="product/images", default="product/images/default.jpg"
    )
    # slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
