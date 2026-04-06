from django.db import models
from django.core.exceptions import ValidationError

import re

class Client(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    id_number = models.CharField(max_length=250, unique=True, error_messages={"id_number": "A user with ID already exists."})

    def clean(self):
        """Validate SA ID number"""
        if not self.is_valid_sa_id():
            raise ValidationError({"id_number": "Invalid South African ID number."})
        
    def is_valid_sa_id(self):
        """
            Validate SA ID using Luhn Algorithm
        """
        id_num = self.id_number.strip()

        if not re.fullmatch(r"\d{13}", id_num):
            return False
        
        #Luhn check
        reverse_id_gigits = [int(d) for d in reversed(id_num)]
       
        total = 0

        for i, digit in enumerate(reverse_id_gigits):
            if i % 2 == 1:  # every second digit
                doubled_digit = digit * 2
                if doubled_digit > 9:
                    doubled_digit -= 9
                total += doubled_digit
            else:
                total += digit
        return (total % 10) == 0


             




class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    address_type_choices = (
        (0, "Physical"),
        (1, "Postal"),
    )
    address_type = models.IntegerField(
        choices=address_type_choices,
        default=0,
    )
    street = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
    )
    street_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    unit_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    building = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    area = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    province = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )
