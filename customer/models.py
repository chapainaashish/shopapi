from django.db import models


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
    discount = models.DecimalField(max_digits=2, decimal_places=2)


class Customer(models.Model):
    image = models.ImageField(upload_to="customer/images", default="")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    joined_date = models.DateField(auto_now_add=True)
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    house_no = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
