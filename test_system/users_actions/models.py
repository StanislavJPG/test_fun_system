from django.contrib.auth.models import AbstractUser
from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=150)
    suite = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=150)


class User(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(max_length=255)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=255)
    website = models.CharField(max_length=200)

    class Meta:
        ordering = ('name', 'username', 'email', 'address')

    def __str__(self):
        return f'{self.username}'
