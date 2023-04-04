import random
import string

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    """
    A model representing a product category

    Attributes:
        name (str): name of the category
        description (str, optional): description of the category.
        created_at (date): date when category was created.
        updated_at (date): date when category was last updated.
    """

    name = models.CharField(max_length=255, help_text="Enter the category name")
    description = models.TextField(
        blank=True, null=True, help_text="Enter the category description"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    """
    A model representing a product

    Attributes:
        upc (str): 12 character unique product code
        name (str): name of the product
        image (str): image file of the product
        description (str, optional): description of the product
        price (Decimal): price of the product
        quantity (int): quantity of the product in stock
        category (Category):  category to which the product belongs
        created_at (date): date when the product was created
        updated_at (date): date when the product was last updated
    """

    upc = models.CharField(max_length=12, unique=True, blank=True)
    name = models.CharField(max_length=255, help_text="Enter the product name")
    image = models.ImageField(
        upload_to="product/images",
        default="product/images/default.jpg",
        help_text="Enter the product image",
    )
    description = models.TextField(
        blank=True, null=True, help_text="Enter the product description"
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Enter the product price"
    )
    quantity = models.PositiveIntegerField(
        help_text="Enter the product quantity",
        validators=[MinValueValidator(1)],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        help_text="Select the product category",
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        """Override the default save method to generate a unique UPC code"""
        self.upc = self.generate_upc()
        super(Product, self).save(*args, **kwargs)

    def generate_upc(self) -> str:
        """Generate a random 12-character string of uppercase letters and digits"""
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """
    A model representing a review of a product

    Attributes:
        user (User): user of the review
        product (Product): product that is reviewed
        description (str): description of the review
        created_at (datetime): date and time when the review was created
        updated_at (datetime): date and time when the review was last updated
        rating (int): rating given by the user to the product, between 1 and 5
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    description = models.TextField(help_text="Enter the description of the review")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Enter the rating of the product between 1 and 5",
    )

    def __str__(self) -> str:
        return self.description

    class Meta:
        unique_together = ("user", "product")
