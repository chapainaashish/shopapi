from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


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
        null=True,
        blank=True,
    )
    phone = PhoneNumberField(help_text="Enter your phone number")

    def __str__(self) -> str:
        return str(self.user.username)


class Address(models.Model):
    """
    A model representing a user's address.

    Attributes:
        user (User): associated user
        house_no (str):  user's house or apartment number
        street (str): user's street
        city (str): user's city or town
        postal_code (str): user's postal code or ZIP code
        country (country): user's country
        updated_at (datetime): date and time the address was updated
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    house_no = models.CharField(max_length=255, help_text="Enter the house no")
    street = models.CharField(max_length=255, help_text="Enter the street")
    city = models.CharField(max_length=255, help_text="Enter the city")
    postal_code = models.CharField(max_length=20, help_text="Enter the postal code")
    country = CountryField(help_text="Enter the country")
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{str(self.user.username)}_{str(self.id)}"
