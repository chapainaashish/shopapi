from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from product.models import Product


class Cart(models.Model):
    """
    A model to represent a user's cart

    Attributes:
        user (User): The user who owns the cart
        created_at (DateTimeField): The date and time when the cart was created
        updated_at (DateTimeField): The date and time when the cart was last updated
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        """Return total cart price"""

        return sum([item.quantity * item.product.price for item in self.items.all()])

    def __str__(self) -> str:
        return str(self.user) + str(self.created_at)


class CartItem(models.Model):
    """
    A model to represent item in cart

    Attributes:
    cart (Cart): associated cart with item
    product (Product): product that is added to the cart
    quantity (int): product quantity
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="carts",
        help_text="Select the product to add in cart",
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Enter the product quantity",
    )

    def unit_price(self):
        """Return cart item unit price"""
        return self.product.price

    def total_price(self):
        """Return cart item total price"""
        return self.product.price * self.quantity

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self) -> str:
        return str(self.cart) + str(self.product)
