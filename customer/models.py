from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


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


class Customer(models.Model):
    image = models.ImageField(
        upload_to="customer/images", default="customer/images/default.jpg"
    )
    phone = PhoneNumberField()
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.first_name + self.last_name


class CustomerAddress(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    house_no = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = CountryField()

    def __str__(self) -> str:
        return self.customer
