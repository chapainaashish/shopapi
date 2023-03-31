from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class Order(models.Model):
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "F"

    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_COMPLETE, "Complete"),
        (PAYMENT_FAILED, "Failed"),
    ]

    DELIVERY_PENDING = "P"
    DELIVERY_COMPLETE = "C"
    DELIVERY_FAILED = "F"

    DELIVERY_CHOICES = [
        (DELIVERY_PENDING, "Pending"),
        (DELIVERY_COMPLETE, "Complete"),
        (DELIVERY_FAILED, "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING
    )
    delivery = models.CharField(
        max_length=1, choices=DELIVERY_CHOICES, default=DELIVERY_PENDING
    )

    def __str__(self):
        return str(self.user) + str(self.placed_at)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.order
