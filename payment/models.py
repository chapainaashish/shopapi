from django.db import models

from order.models import Order


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
        Order, on_delete=models.CASCADE, related_name="payment", primary_key=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING
    )

    def amount(self):
        """Return total sum payment"""
        return self.order.total_price
    
    def user(self):
        """Return payment user"""
        return self.order.user

    def __str__(self) -> str:
        return f"{str(self.order)}_{str(self.status)}"
