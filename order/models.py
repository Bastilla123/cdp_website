from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, default="")
    subtitle = models.CharField(max_length=255, blank=False, null=False, default="")
    description = models.TextField(blank=True, null=True, default=None)
    arbeitspreis = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    basisprice = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    vertragslaufzeit = models.IntegerField(default=1)
    kuendigungsfrist = models.IntegerField(default=24)

    def __str__(self):
        return self.title

class order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user_link = models.ForeignKey(
        User, related_name="order_user_link", on_delete=models.CASCADE, blank = False, null = False, default = 0)
    product_link = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank = False, null = False, default = 0)
    expected_consumption = models.IntegerField(default=6)

# class CustomerInfo(models.Model):
#     firstname = models.CharField(max_length=255)
#     lastname = models.CharField(max_length=255)
#
#     street = models.CharField(max_length=255)
#     housenumber = models.CharField(max_length=255)
#     zip = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     birthday = models.DateField(_("Birthday"), default=date.today)
#     phone = models.CharField(max_length=255)
#     iban = models.CharField(max_length=34)



