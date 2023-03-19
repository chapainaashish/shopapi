from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

"""
class Membership(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]

    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    discount = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        return self.membership
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)

"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="customer/images", default="customer/images/default.jpg"
    )
    phone = PhoneNumberField()

    def __str__(self) -> str:
        return self.first_name + self.last_name


class Address(models.Model):
    BILLING = "B"
    SHIPPING = "S"
    ADDRESS_CHOICES = [(BILLING, "Billing"), (SHIPPING, "Shipping")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    house_no = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = CountryField()

    def __str__(self) -> str:
        return self.customer
