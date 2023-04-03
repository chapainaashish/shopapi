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
    """
    A model to represents user's profile

    Attributes:
        user (User): associated user
        image (image): user profile image
        phone (phone): user phone number
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="customer/images",
        default="customer/images/default.jpg",
        help_text="Enter your image",
    )
    phone = PhoneNumberField(help_text="Enter your phone number")

    def __str__(self) -> str:
        return self.first_name + self.last_name


class Address(models.Model):
    """
    A model representing a user's address.

    Attributes:
        user (User): associated user
        address_type (char): address type, it can be
            - "B" Billing
            - "S" Shipping
        house_no (str):  user's house or apartment number
        street (str): user's street
        city (str): user's city or town
        postal_code (str): user's postal code or ZIP code
        country (country): user's country
        updated_at (datetime): date and time the address was updated
    """

    BILLING = "B"
    SHIPPING = "S"
    ADDRESS_CHOICES = [(BILLING, "Billing"), (SHIPPING, "Shipping")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(
        max_length=1, choices=ADDRESS_CHOICES, help_text="Select address type"
    )
    house_no = models.CharField(max_length=255, help_text="Enter the house no")
    street = models.CharField(max_length=255, help_text="Enter the street")
    city = models.CharField(max_length=255, help_text="Enter the city")
    postal_code = models.CharField(max_length=20, help_text="Enter the postal code")
    country = CountryField(help_text="Enter the country")
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.customer
