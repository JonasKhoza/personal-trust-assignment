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
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
             

class Relationship(models.Model):
    RELATIONSHIP_CHOICES = [
        ("husband", "Husband"),
        ("wife", "Wife"),
        ("father", "Father"),
        ("mother", "Mother"),
        ("son", "Son"),
        ("daughter", "Daughter"),
        ("sibling", "Sibling"),
    ]

    client_from = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="relationships_from")
    client_to = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="relationships_to")
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)

    class Meta:
        unique_together = ("client_from", "client_to")  # prevents duplicate relationships

    def save(self, *args, **kwargs):
        # 1. Save the current instance first
        super().save(*args, **kwargs)

        
        # use getattr to check if '_skip_inverse' was set on this instance
        if getattr(self, '_skip_inverse', False):
            return

      
        inverse_type = self.get_inverse_relationship()
        if inverse_type:
            # Check if inverse already exists
            if not Relationship.objects.filter(
                client_from=self.client_to, 
                client_to=self.client_from
            ).exists():
                
                # Create the inverse object but don't save it yet
                inverse_rel = Relationship(
                    client_from=self.client_to,
                    client_to=self.client_from,
                    relationship_type=inverse_type
                )
                
                # set the flag: This prevents the recursion
                inverse_rel._skip_inverse = True
                inverse_rel.save()

    def get_inverse_relationship(self):
        inverse_map = {
            "husband": "wife",
            "wife": "husband",
            "father": "son",
            "mother": "daughter",
            "son": "father",
            "daughter": "mother",
            "sibling": "sibling",
        }
        return inverse_map.get(self.relationship_type)
    
    def __str__(self):
        return f"{self.client_from} is {self.relationship_type} of {self.client_to}"

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
