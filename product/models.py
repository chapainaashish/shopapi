from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="product/images", default="product/images/default.jpg"
    )
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    description = models.TextField()
    date = models.DateField(auto_now=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return self.description
