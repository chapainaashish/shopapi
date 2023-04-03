from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from product.models import Product


class Order(models.Model):
    """
    A model to represent an order placed by a user

    Attributes:
        user (User): user who placed the order
        created_at (datetime): date and time when the order was created
        updated_at (datetime): date and time when the order was last updated
        delivery (char): status of the order delivery, can be one of:
            - "P" (pending)
            - "C" (complete)
            - "F" (failed)
    """

    DELIVERY_PENDING = "P"
    DELIVERY_COMPLETE = "C"
    DELIVERY_FAILED = "F"

    DELIVERY_CHOICES = [
        (DELIVERY_PENDING, "Pending"),
        (DELIVERY_COMPLETE, "Complete"),
        (DELIVERY_FAILED, "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery = models.CharField(
        max_length=1, choices=DELIVERY_CHOICES, default=DELIVERY_PENDING
    )

    def __str__(self):
        return str(self.user) + str(self.placed_at)


class OrderItem(models.Model):
    """
    A model to represent an item in an order

    Attributes:
        order (Order): order this item belongs to
        product (Product): product being ordered
        ordered_price (decimal): price of the product when it was ordered
        quantity (int): quantity of the product being ordered
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    ordered_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Enter the product quantity",
    )

    def __str__(self) -> str:
        return self.order

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the default save method to set ordered_price to product_price when the product is being ordered
        """
        if not self.id:
            self.ordered_price = self.product.price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    A model to represent payment of an order

    Attributes:
        order (Order): order that this payment is associated with
        updated_at (datetime): date and time when the payment was last updated
        status (char): status of the payment, can be one of:
            - "P" (pending)
            - "C" (complete)
            - "F" (failed)
    """

    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "F"
    
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_COMPLETE, "Complete"),
        (PAYMENT_FAILED, "Failed"),
    ]
    order = models.OneToOneField(
        Order, on_delete=models.PROTECT, related_name="payment"
    )
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING
    )
